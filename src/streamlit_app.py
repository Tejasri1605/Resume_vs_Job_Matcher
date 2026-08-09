import asyncio
import os
from datetime import datetime

import streamlit as st
import config
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Resume Analyzer AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== CSS =====================
def apply_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            background-attachment: fixed;
            color: #e5e7eb;
        }

        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        header, footer {visibility: hidden;}

        h1, h2, h3 {
            color: white;
        }

        .hero {
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        .hero-title {
            font-size: 64px;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 3s ease-in-out infinite;
            letter-spacing: -1px;
        }

        @keyframes glow {
            0%, 100% {
                filter: drop-shadow(0 0 20px rgba(59,130,246,0.5));
            }
            50% {
                filter: drop-shadow(0 0 40px rgba(139,92,246,0.7));
            }
        }

        .hero-subtitle {
            font-size: 20px;
            color: #cbd5e1;
            max-width: 700px;
            margin-bottom: 50px;
            line-height: 1.6;
            animation: fadeInUp 1s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .stButton {
            display: flex;
            justify-content: center;
        }

        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border-radius: 16px;
            padding: 20px 60px;
            font-size: 20px;
            font-weight: 700;
            border: none;
            box-shadow: 
                0 10px 40px rgba(59, 130, 246, 0.4),
                0 0 60px rgba(139, 92, 246, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }

        .stButton > button:hover {
            transform: translateY(-4px) scale(1.05);
            box-shadow: 
                0 20px 60px rgba(59, 130, 246, 0.6),
                0 0 80px rgba(139, 92, 246, 0.5);
        }

        .stButton > button:active {
            transform: translateY(-2px) scale(1.02);
        }

        .feature-badges {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 40px;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 10px 24px;
            font-size: 14px;
            color: #cbd5e1;
            transition: all 0.3s ease;
        }

        .badge:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(139, 92, 246, 0.5);
            transform: translateY(-2px);
        }

        .glass {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 1px rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .stTextInput input,
        .stTextArea textarea {
            background-color: rgba(30, 41, 59, 0.9) !important;
            color: white !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: rgba(139, 92, 246, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        }

        .stTextInput label,
        .stTextArea label,
        .stFileUploader label,
        .stRadio label {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }

        .streamlit-expanderHeader {
            background-color: rgba(30, 41, 59, 0.8);
            color: white !important;
            font-weight: 600 !important;
            border-radius: 10px;
        }

        .stFileUploader > div {
            background-color: rgba(30, 41, 59, 0.6) !important;
            border: 2px dashed rgba(139, 92, 246, 0.4) !important;
            border-radius: 12px;
        }

        .stRadio > div {
            gap: 20px;
        }

        .stRadio > div label {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
        }

        .stSuccess, .stWarning {
            background-color: rgba(30, 41, 59, 0.7) !important;
            border-radius: 12px !important;
        }

        .stMarkdown {
            color: #e2e8f0 !important;
        }

        .stApp h2, .stApp h3 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        .footer-text {
            text-align: center;
            color: #64748b;
            margin-top: 60px;
            font-size: 14px;
            animation: fadeInUp 1.5s ease-out;
        }

        .footer-text span {
            margin: 0 8px;
            color: #8b5cf6;
            font-weight: 600;
        }

        .improvement-card {
            background: rgba(30, 41, 59, 0.5);
            border-left: 4px solid #8b5cf6;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        }

        .improvement-title {
            color: #a78bfa;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .skill-badge {
            display: inline-block;
            background: rgba(139, 92, 246, 0.2);
            border: 1px solid rgba(139, 92, 246, 0.4);
            border-radius: 20px;
            padding: 6px 14px;
            margin: 4px;
            font-size: 13px;
            color: #e9d5ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


apply_css()

# ===================== SESSION STATE =====================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# ===================== BACKEND =====================
try:
    from prefect_flow import resume_analyzer_flow
except Exception as e:
    st.error(f"Backend error: {e}")
    st.stop()

if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "mock":
    st.error("GEMINI_API_KEY not configured")
    st.stop()

TEMP_DIR = "temp_files"


def save_file(upload):
    os.makedirs(TEMP_DIR, exist_ok=True)
    path = os.path.join(
        TEMP_DIR, datetime.now().strftime("%Y%m%d_%H%M%S_") + upload.name
    )
    with open(path, "wb") as f:
        f.write(upload.getbuffer())
    return path


def cleanup(path):
    if path and os.path.exists(path):
        os.remove(path)


def create_ats_breakdown_chart(scores):
    """Create detailed ATS score breakdown"""
    categories = list(scores.keys())
    values = list(scores.values())
    colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.2)', width=2)
            ),
            text=[f"{v}%" for v in values],
            textposition='outside',
            textfont=dict(color='white', size=14, family='Inter')
        )
    ])
    
    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.8)',
        plot_bgcolor='rgba(15, 23, 42, 0.8)',
        font=dict(color='white', family='Inter'),
        height=400,
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(showgrid=False),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    return fig


def create_comparison_radar(resume_skills, required_skills):
    """Create radar chart comparing resume vs required skills"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(resume_skills.values()),
        theta=list(resume_skills.keys()),
        fill='toself',
        name='Your Resume',
        line=dict(color='#8b5cf6', width=2),
        fillcolor='rgba(139, 92, 246, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=list(required_skills.values()),
        theta=list(required_skills.keys()),
        fill='toself',
        name='Required',
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            bgcolor='rgba(15, 23, 42, 0.8)'
        ),
        paper_bgcolor='rgba(15, 23, 42, 0.8)',
        font=dict(color='white', family='Inter'),
        height=450,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5)
    )
    
    return fig


def gauge(score):
    """Create animated gauge chart"""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            number={"suffix": "%", "font": {"size": 50, "color": "white"}},
            delta={'reference': 75, 'increasing': {'color': "#10b981"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#8b5cf6", "thickness": 0.8},
                "bgcolor": "#0f172a",
                "borderwidth": 2,
                "bordercolor": "rgba(139, 92, 246, 0.3)",
                "steps": [
                    {"range": [0, 50], "color": "rgba(239, 68, 68, 0.2)"},
                    {"range": [50, 75], "color": "rgba(245, 158, 11, 0.2)"},
                    {"range": [75, 100], "color": "rgba(34, 197, 94, 0.2)"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="#0f172a",
        font={"color": "white", "family": "Inter"},
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)


# ===================== HOME PAGE =====================
if st.session_state.page == "home":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">📄 Resume Analyzer AI</div>
            <div class="hero-subtitle">
                Transform your job search with AI-powered resume analysis. Get instant match scores, 
                identify missing skills, and unlock your career potential with Google Gemini.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        if st.button("🚀 Explore Now"):
            st.session_state.page = "analyzer"
            st.rerun()

    st.markdown(
        """
        <div class="feature-badges">
            <div class="badge">✨ AI-Powered</div>
            <div class="badge">⚡ Instant Analysis</div>
            <div class="badge">🎯 Skill Matching</div>
            <div class="badge">📊 Visual Insights</div>
            <div class="badge">🚀 ATS Optimization</div>
            <div class="badge">💡 Smart Suggestions</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='footer-text'>Built with<span>Streamlit</span>·<span>Prefect</span>·<span>Gemini AI</span></p>",
        unsafe_allow_html=True,
    )


# ===================== ANALYZER PAGE =====================
elif st.session_state.page == "analyzer":
    col_back, col_history = st.columns([1, 5])
    with col_back:
        if st.button("⬅ Back"):
            st.session_state.page = "home"
            st.rerun()
    
    with col_history:
        if len(st.session_state.analysis_history) > 0:
            st.info(f"📊 Analysis History: {len(st.session_state.analysis_history)} resumes analyzed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📄 Resume vs Job Description Analyzer")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        resume = st.file_uploader("Upload Resume (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        jd_type = st.radio("Job Description Input", ["Text", "PDF", "LinkedIn URL"], horizontal=True)

        jd_text = jd_file = jd_url = None
        if jd_type == "Text":
            jd_text = st.text_area("Paste Job Description", height=220)
        elif jd_type == "PDF":
            jd_file = st.file_uploader("Upload JD PDF", type=["pdf"])
        else:
            jd_url = st.text_input("LinkedIn Job URL")
        st.markdown("</div>", unsafe_allow_html=True)

    ready = resume and (
        (jd_type == "Text" and jd_text)
        or (jd_type == "PDF" and jd_file)
        or (jd_type == "LinkedIn URL" and jd_url.startswith("http"))
    )

    if st.button("✨ Analyze Now", disabled=not ready):
        rp = jp = None
        try:
            with st.spinner("🔍 Running AI analysis..."):
                rp = save_file(resume)

                if jd_type == "Text":
                    jd_input = jd_text
                elif jd_type == "PDF":
                    jp = save_file(jd_file)
                    jd_input = jp
                else:
                    jd_input = jd_url

                result = asyncio.run(
                    resume_analyzer_flow(resume_path=rp, jd_input=jd_input)
                )
                
                # Save to history
                st.session_state.analysis_history.append({
                    'date': datetime.now(),
                    'score': result.get("percentage", 0),
                    'resume_name': resume.name
                })

            score = result.get("percentage", 0)
            
            # Animated success message
            if score >= 80:
                st.balloons()
                st.success("🎉 Excellent Match! You're a strong candidate!")
            elif score >= 60:
                st.success("👍 Good Match! A few improvements will make you perfect!")
            else:
                st.warning("💪 Room for Improvement! Let's optimize your resume!")
            
            st.markdown("---")
            
            # Main Score Gauge
            st.subheader("🎯 Overall Match Score")
            gauge(score)

            # ATS Score Breakdown
            st.markdown("---")
            st.subheader("📊 Detailed ATS Score Breakdown")
            
            # Simulate ATS breakdown scores (in real app, get from AI)
            ats_scores = {
                'Keywords': min(score + 5, 100),
                'Skills': score,
                'Experience': max(score - 10, 0),
                'Format': 85,
                'Education': max(score - 5, 0)
            }
            
            col_chart1, col_chart2 = st.columns([2, 1])
            
            with col_chart1:
                st.plotly_chart(create_ats_breakdown_chart(ats_scores), use_container_width=True)
            
            with col_chart2:
                st.markdown('<div class="glass">', unsafe_allow_html=True)
                for category, value in ats_scores.items():
                    color = "#10b981" if value >= 75 else "#f59e0b" if value >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="margin: 10px 0;">
                        <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 4px;">{category}</div>
                        <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: {color}; width: {value}%; height: 100%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Skills Radar Comparison
            st.markdown("---")
            st.subheader("🎯 Skills Match Analysis")
            
            # Simulate skill comparison (in real app, extract from AI)
            resume_skills = {
                'Technical': 75,
                'Leadership': 60,
                'Communication': 80,
                'Problem Solving': 70,
                'Domain Knowledge': 65
            }
            
            required_skills = {
                'Technical': 90,
                'Leadership': 70,
                'Communication': 85,
                'Problem Solving': 80,
                'Domain Knowledge': 75
            }
            
            st.plotly_chart(create_comparison_radar(resume_skills, required_skills), use_container_width=True)

            # Summary Sections
            st.markdown("---")
            col_sum1, col_sum2 = st.columns(2)
            
            with col_sum1:
                with st.expander("📄 Resume Summary", expanded=False):
                    st.markdown(result.get("resume_summary", "N/A"))
            
            with col_sum2:
                with st.expander("🧾 Job Description Summary", expanded=False):
                    st.markdown(result.get("jd_summary", "N/A"))

            # Matches and Missing Skills
            st.markdown("---")
            colA, colB = st.columns(2)
            
            with colA:
                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.markdown("### ✅ Matching Strengths")
                st.markdown(result.get("matches", "N/A"))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with colB:
                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.markdown("### ⚠️ Missing Skills")
                st.markdown(result.get("misses", "N/A"))
                st.markdown('</div>', unsafe_allow_html=True)

            # AI-Powered Improvement Suggestions
            st.markdown("---")
            st.subheader("💡 AI-Powered Improvement Suggestions")
            
            suggestions = [
                {
                    "title": "Add Quantifiable Achievements",
                    "detail": "Replace 'Managed team' with 'Led team of 8 engineers, increasing productivity by 35%'",
                    "priority": "High"
                },
                {
                    "title": "Include Missing Keywords",
                    "detail": "Add: Agile, Scrum, CI/CD, Docker, Kubernetes to match job requirements",
                    "priority": "High"
                },
                {
                    "title": "Strengthen Action Verbs",
                    "detail": "Replace weak verbs: 'Worked on' → 'Architected', 'Helped with' → 'Spearheaded'",
                    "priority": "Medium"
                },
                {
                    "title": "Optimize Formatting",
                    "detail": "Use simple, ATS-friendly formatting. Avoid tables, text boxes, and images",
                    "priority": "Medium"
                }
            ]
            
            for sug in suggestions:
                priority_color = "#ef4444" if sug["priority"] == "High" else "#f59e0b"
                st.markdown(f"""
                <div class="improvement-card">
                    <div class="improvement-title">
                        {sug["title"]} 
                        <span style="color: {priority_color}; font-size: 12px; margin-left: 10px;">
                            [{sug["priority"]} Priority]
                        </span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 14px;">{sug["detail"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Skill Gap Analysis with Learning Resources
            st.markdown("---")
            st.subheader("📚 Skill Gap & Learning Path")
            
            skill_gaps = [
                {"skill": "Docker", "time": "2-3 weeks", "courses": "Docker Mastery (Udemy)", "priority": "High"},
                {"skill": "Kubernetes", "time": "3-4 weeks", "courses": "Kubernetes for Beginners (Coursera)", "priority": "High"},
                {"skill": "AWS Certification", "time": "6-8 weeks", "courses": "AWS Solutions Architect (A Cloud Guru)", "priority": "Medium"}
            ]
            
            for gap in skill_gaps:
                st.markdown(f"""
                <div class="glass" style="margin: 15px 0; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="skill-badge">{gap["skill"]}</span>
                        <span style="color: {'#ef4444' if gap['priority'] == 'High' else '#f59e0b'}; font-weight: 600;">
                            {gap["priority"]} Priority
                        </span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 14px;">
                        ⏱️ Estimated Time: <strong>{gap["time"]}</strong><br>
                        📖 Recommended: <strong>{gap["courses"]}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Interview Preparation Section
            st.markdown("---")
            st.subheader("🎤 Interview Preparation")
            
            with st.expander("💬 Likely Interview Questions", expanded=False):
                questions = [
                    "Tell me about a time you led a challenging project",
                    "How do you handle tight deadlines and pressure?",
                    "Describe your experience with [key skill from JD]",
                    "What's your approach to problem-solving in a team?"
                ]
                for i, q in enumerate(questions, 1):
                    st.markdown(f"**{i}.** {q}")
            
            with st.expander("⚡ Your STAR Method Talking Points", expanded=False):
                st.markdown("""
                Based on your resume:
                - **Situation**: Led team during product launch
                - **Task**: Reduce deployment time by 40%
                - **Action**: Implemented CI/CD pipeline using Jenkins
                - **Result**: Decreased release cycle from 2 weeks to 3 days
                """)

            # Why This Score Section
            st.markdown("---")
            st.subheader("🧠 Understanding Your Score")
            st.markdown(f"""
            <div class="glass">
                <p style="color: #e2e8f0; line-height: 1.8;">
                    Your resume matches <strong style="color: #8b5cf6;">{score}%</strong> of the job requirements.
                </p>
                <ul style="color: #cbd5e1; line-height: 1.8;">
                    <li>✅ Strong alignment with key requirements</li>
                    <li>⚠️ Some skills or experiences need strengthening</li>
                    <li>📈 Implementing our suggestions could boost your score significantly</li>
                    <li>🎯 Industry benchmark for this role: 75-80%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            cleanup(rp)
            cleanup(jp)

    st.markdown(
        "<p class='footer-text'>",
        unsafe_allow_html=True,
    )