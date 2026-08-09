import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import os
import re

from prefect import task, flow, get_run_logger, runtime
from prefect.client.orchestration import get_client
from prefect.client.schemas.objects import Artifact

import ocr_utils
import scraping_utils
import gemini_analyzer


# ---------------- Utility ----------------
def sanitize_artifact_key(input_string: str) -> str:
    sanitized = input_string.lower()
    if sanitized.startswith("http"):
        try:
            from urllib.parse import urlparse
            path_parts = [p for p in urlparse(sanitized).path.split("/") if p]
            sanitized = "-".join(path_parts[-2:]) if path_parts else "linkedin-url"
        except Exception:
            sanitized = "linkedin-url"
    sanitized = re.sub(r"[^a-z0-9-]+", "-", sanitized)
    return sanitized.strip("-")[:50] or "sanitized-key"


# ---------------- Tasks ----------------
@task(name="Extract Text from PDF")
def pdf_text_task(file_path: str) -> str:
    logger = get_run_logger()
    try:
        text = ocr_utils.extract_text_from_file(file_path)
        if not text.strip():
            raise ValueError("PDF text extraction returned empty text.")
        return text
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise


@task(name="Scrape Job Description")
async def scrape_task(url: str) -> str:
    logger = get_run_logger()
    text = await scraping_utils.scrape_linkedin_job_description(url)
    if not text.strip():
        raise ValueError("Scraped JD text is empty.")
    return text



@task(name="Analyze with Gemini")
async def analyze_task(resume_text: str, jd_text: str) -> dict:
    return gemini_analyzer.analyze_resume_jd(resume_text, jd_text)[0]


# ---------------- Flow ----------------
@flow(name="Resume Analyzer Flow")
async def resume_analyzer_flow(resume_path: str, jd_input) -> dict:
    logger = get_run_logger()
    flow_run_id = runtime.flow_run.id if runtime.flow_run else None

    # -------- Resume --------
    resume_basename = os.path.basename(resume_path)
    resume_text = pdf_text_task(resume_path)

    # -------- JD Detection --------
    jd_text = None
    jd_source_display = ""

    if isinstance(jd_input, str) and jd_input.strip().startswith("http"):
        jd_source_display = jd_input
        jd_text = await scrape_task(jd_input.strip())


    elif isinstance(jd_input, str) and os.path.exists(jd_input):
        jd_source_display = os.path.basename(jd_input)
        jd_text = pdf_text_task(jd_input)

    elif isinstance(jd_input, str):
        # 🔥 NEW: Direct TEXT input
        jd_source_display = "Pasted Text"
        jd_text = jd_input.strip()

    else:
        return {"error": "Invalid Job Description input."}

    # -------- Validation --------
    if not resume_text.strip():
        return {"error": "Resume text is empty after extraction."}

    if not jd_text.strip():
        return {"error": "Job Description text is empty."}

    # -------- Artifacts --------
    try:
        input_artifact = Artifact(
            key="input-sources",
            type="markdown",
            data=f"- Resume: `{resume_basename}`\n- JD Source: `{jd_source_display}`",
            flow_run_id=flow_run_id,
        )
        async with get_client() as client:
            await client.create_artifact(input_artifact)
    except Exception:
        pass

    # -------- Gemini Analysis --------
    try:
        result = await analyze_task(resume_text, jd_text)
        return result
    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        return {"error": "Gemini analysis failed. Check logs."}
