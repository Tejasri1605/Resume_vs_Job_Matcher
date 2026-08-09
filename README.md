# Resume Job Matcher 🤖📄

An intelligent tool built to analyze and match your resume with job descriptions from uploaded documents or LinkedIn job URLs, powered by Google Gemini API, OCR, Selenium, Streamlit, and Prefect for effective workflow orchestration and monitoring.

## 🔧 Features

- Document Analysis: Analyze resumes and job descriptions from PDF or image files.
- LinkedIn Scraping: Fetch and analyze LinkedIn job postings via URLs.
- AI Matching: Leverage Google Gemini API to assess compatibility between resumes and job descriptions.
- Interactive UI: User-friendly interface powered by Streamlit.
- Workflow Management: Monitor and orchestrate tasks using Prefect.

## 🚀 Getting Started

### 📂 Project Structure

```
resume_job_matcher/
├── data/
├── src/
│   ├── config.py
│   ├── gemini_analyzer.py
│   ├── ocr_utils.py
│   ├── prefect_flow.py
│   ├── scraping_utils.py
│   ├── streamlit_app.py
│   └── temp_files/
├── .env
├── README.md
└── requirements.txt
```

### 📦 Installation

#### Step 1: Clone Repository

```
git clone <repository_url>
cd resume_job_matcher
```

#### Step 2: Set Up Environment
Create a virtual environment and install dependencies:

```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### ⚙️ Configuration

Create a .env file in the project root with the following variables:

```
GEMINI_API_KEY="your_gemini_api_key_here"
CHROMEDRIVER_PATH="your_chromedriver_path_here"
```

- GEMINI_API_KEY: Obtain your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
- CHROMEDRIVER_PATH: Download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/) and specify the local path.

### 🚗 Running the Application

Navigate to the ```src``` folder and run the Streamlit app:

```
cd src
streamlit run streamlit_app.py
```

A Streamlit window will open in your browser. From there, you can:

- Upload your resume (PDF or image).
- Provide a job description either as a file upload or a LinkedIn URL.
- Click "✨ Analyze Now" to get your analysis results.

### 🛠️ Technical Components

- config.py: Manages environment configurations.
- scraping_utils.py: Scrapes job descriptions from LinkedIn URLs using Selenium.
- gemini_analyzer.py: Interacts with Google Gemini API to compare resumes and job descriptions.
- prefect_flow.py: Orchestrates asynchronous workflow and task management with Prefect.
- streamlit_app.py: Provides the user interface via Streamlit.

Contributions, issues, and feature requests are welcome!

### 📝 License

This project is licensed under the MIT License.
