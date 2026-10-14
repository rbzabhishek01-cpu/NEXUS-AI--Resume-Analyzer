import io
import re
from datetime import datetime

import streamlit as st

# Optional file readers are imported only when needed.
st.set_page_config(
    page_title="NEXUS AI | Resume Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- PREMIUM UI -----------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root { color-scheme: dark; }
    html, body, [class*="css"] { font-family: Inter, sans-serif; }
    .stApp {
        background:
          radial-gradient(circle at 10% 0%, rgba(91, 33, 182, .25), transparent 30%),
          radial-gradient(circle at 90% 10%, rgba(14, 165, 233, .16), transparent 28%),
          #080b16;
        color: #f3f4ff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10152b 0%, #0b1020 100%);
        border-right: 1px solid rgba(94,231,255,.15);
    }
    [data-testid="stSidebar"] * { color: #e5e7eb; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }
    .nexus-brand { color:#5ee7ff; font-weight:800; letter-spacing:3px; font-size: .85rem; }
    .hero-card {
        padding: 2rem 2.2rem; border-radius: 24px;
        background: linear-gradient(125deg, rgba(30,41,90,.95), rgba(42,20,92,.92));
        border: 1px solid rgba(94,231,255,.35);
        box-shadow: 0 20px 70px rgba(0,0,0,.25);
        margin-bottom: 1.5rem;
    }
    .hero-kicker { color:#67e8f9; font-size:.78rem; font-weight:800; letter-spacing:2px; }
    .hero-title { font-size:clamp(2rem, 4vw, 3.4rem); line-height:1.1; font-weight:800; margin:.65rem 0; color:#fff; }
    .hero-title span { color:#a78bfa; }
    .hero-copy { color:#cbd5e1; font-size:1.02rem; line-height:1.75; max-width:800px; }
    .panel {
        background: rgba(17,22,42,.82); border:1px solid rgba(148,163,184,.18);
        border-radius:18px; padding:1.2rem 1.3rem; margin-bottom:1rem;
    }
    .panel-title { font-size:1.05rem; font-weight:750; color:#f8fafc; margin-bottom:.3rem; }
    .muted { color:#94a3b8; font-size:.9rem; }
    .metric-card {
        padding:1.1rem; border-radius:16px; min-height:105px;
        background:linear-gradient(145deg, rgba(30,41,75,.95), rgba(17,22,42,.95));
        border:1px solid rgba(94,231,255,.2);
    }
    .metric-label { color:#a5b4fc; font-size:.8rem; font-weight:700; letter-spacing:.5px; }
    .metric-value { color:#fff; font-size:1.8rem; font-weight:800; margin-top:.35rem; }
    .tag {
        display:inline-block; padding:.3rem .65rem; margin:.2rem .25rem .2rem 0;
        border-radius:999px; background:rgba(94,231,255,.1);
        color:#a5f3fc; border:1px solid rgba(94,231,255,.24); font-size:.8rem;
    }
    .tag-missing { background:rgba(251,113,133,.1); color:#fda4af; border-color:rgba(251,113,133,.25); }
    div.stButton > button, div.stDownloadButton > button {
        border:0; border-radius:12px; font-weight:750; min-height:2.8rem;
        background:linear-gradient(90deg,#7c3aed,#2563eb); color:white;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        border:0; color:white; filter:brightness(1.12);
    }
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div {
        background-color:#11162a !important; color:#f8fafc !important;
        border-color:rgba(148,163,184,.25) !important; border-radius:10px !important;
    }
    hr { border-color:rgba(148,163,184,.16); }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- HELPERS ---------------------------------------
COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "mysql",
    "postgresql", "mongodb", "html", "css", "react", "node.js", "express",
    "django", "flask", "fastapi", "streamlit", "spring boot", "git", "github",
    "docker", "kubernetes", "aws", "azure", "gcp", "rest api", "api",
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "data analysis",
    "data structures", "algorithms", "dsa", "oop", "linux", "communication",
    "problem solving", "agile", "power bi", "excel", "tableau",
]

def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT uploads."""
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    raise ValueError("Please upload a PDF, DOCX, or TXT file.")

def find_skills(text):
    lower = text.lower()
    found = []
    for skill in COMMON_SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lower):
            found.append(skill)
    return sorted(set(found), key=str.lower)

def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0
    return round(len(set(resume_skills) & set(job_skills)) / len(set(job_skills)) * 100)

def make_report(resume_text, resume_skills, job_text, job_skills, match):
    matched = sorted(set(resume_skills) & set(job_skills), key=str.lower)
    missing = sorted(set(job_skills) - set(resume_skills), key=str.lower)
    lines = [
        "NEXUS AI | RESUME INTELLIGENCE REPORT",
        f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        "",
        f"Resume characters analyzed: {len(resume_text)}",
        f"Resume skills detected: {len(resume_skills)}",
        f"Target-job skills detected: {len(job_skills)}",
        f"Skill match score: {match}%",
        "",
        "MATCHED SKILLS",
        ", ".join(matched) if matched else "No matching skills detected.",
        "",
        "SKILLS TO CONSIDER ADDING (only if you genuinely have them)",
        ", ".join(missing) if missing else "No missing skills detected from the keyword list.",
        "",
        "RECOMMENDATIONS",
        "- Tailor your resume summary to the target role.",
        "- Add measurable outcomes to project and work-experience bullets.",
        "- Include relevant skills only when you can confidently explain them.",
        "- Keep formatting consistent and proofread before applying.",
        "",
        "Note: This is a keyword-based helper, not a hiring decision or guarantee.",
    ]
    return "\n".join(lines)

# ----------------------------- SIDEBAR ---------------------------------------
with st.sidebar:
    st.markdown('<div class="nexus-brand">✦ NEXUS AI</div>', unsafe_allow_html=True)
    st.markdown("## Resume Intelligence")
    st.caption("Your career workspace")
    page = st.radio(
        "WORKSPACE",
        ["Resume Analysis", "Skill Intelligence", "Job Compatibility", "About"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("### Analysis settings")
    show_tips = st.toggle("Show improvement tips", value=True)
    st.caption("Your uploaded resume is processed in this app session. Avoid uploading sensitive information you do not need analyzed.")

# ----------------------------- HERO ------------------------------------------
st.markdown(
    """
    <div class="hero-card">
      <div class="hero-kicker">✦ NEXT-GEN CAREER INTELLIGENCE</div>
      <div class="hero-title">Make your resume<br><span>impossible to ignore.</span></div>
      <div class="hero-copy">Analyze your skills, compare your resume with a target role,
      and discover practical ways to improve your next application — all in one workspace.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- INPUTS ----------------------------------------
left, right = st.columns([1.05, 1], gap="large")
with left:
    st.markdown('<div class="panel"><div class="panel-title">📄 Resume workspace</div><div class="muted">Upload your current resume to begin.</div></div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"], help="Supported formats: PDF, DOCX, TXT")
with right:
    st.markdown('<div class="panel"><div class="panel-title">🎯 Target opportunity</div><div class="muted">Paste a job description for a more useful comparison.</div></div>', unsafe_allow_html=True)
    job_title = st.text_input("Target role", placeholder="e.g. Python Backend Developer")
    job_description = st.text_area("Job description", height=140, placeholder="Paste the job requirements here…")

resume_text = ""
resume_skills = []
job_skills = []
if resume_file is not None:
    try:
        resume_text = extract_text(resume_file)
        resume_skills = find_skills(resume_text)
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")
if job_description.strip():
    job_skills = find_skills(job_description)
match_score = calculate_match(resume_skills, job_skills)

# ----------------------------- PAGE CONTENT ----------------------------------
if page == "About":
    st.markdown("## About NEXUS AI")
    st.write("NEXUS AI is a resume review helper built with Python and Streamlit. It extracts text from supported resume files, detects common skill keywords, and compares them with a pasted job description.")
    st.info("The analysis is keyword-based and does not replace human review. Never add skills to your resume unless you actually have them.")
elif page == "Resume Analysis":
    st.markdown("## 01 / Resume analysis")
    if resume_file is None:
        st.info("Upload a resume above to start the analysis.")
    else:
        word_count = len(re.findall(r"\b[\w+#.]+\b", resume_text))
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">WORDS EXTRACTED</div><div class="metric-value">{word_count:,}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">SKILLS DETECTED</div><div class="metric-value">{len(resume_skills)}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">TEXT CHARACTERS</div><div class="metric-value">{len(resume_text):,}</div></div>', unsafe_allow_html=True)
        st.markdown("### Detected skills")
        if resume_skills:
            st.markdown("".join(f'<span class="tag">{s}</span>' for s in resume_skills), unsafe_allow_html=True)
        else:
            st.warning("No common skills were detected. If this is a scanned PDF, text extraction may not work; try a text-based PDF or DOCX.")
        with st.expander("Preview extracted resume text"):
            st.text(resume_text[:8000] or "No text extracted.")
        if show_tips:
            st.markdown("### Resume improvement checklist")
            st.write("- Start bullets with action verbs and explain the result.")
            st.write("- Quantify outcomes where possible (time saved, users served, accuracy, revenue, etc.).")
            st.write("- Keep project descriptions specific: problem, tools used, and result.")
            st.write("- Use a clean, consistent layout and check spelling.")
elif page == "Skill Intelligence":
    st.markdown("## 02 / Skill intelligence")
    if resume_file is None:
        st.info("Upload a resume to see your detected skills.")
    else:
        st.metric("Detected skill keywords", len(resume_skills))
        if resume_skills:
            st.markdown("".join(f'<span class="tag">{s}</span>' for s in resume_skills), unsafe_allow_html=True)
        else:
            st.warning("No listed skill keywords found in the extracted text.")
        st.caption("Keyword detection is a simple starting point; it may miss synonyms and context.")
elif page == "Job Compatibility":
    st.markdown("## 03 / Job compatibility")
    if resume_file is None:
        st.info("Upload a resume first.")
    elif not job_description.strip():
        st.info("Paste the target job description in the panel above.")
    else:
        st.markdown(f"### {job_title.strip() or 'Target role'}")
        st.progress(match_score / 100, text=f"Keyword match score: {match_score}%")
        matched = sorted(set(resume_skills) & set(job_skills), key=str.lower)
        missing = sorted(set(job_skills) - set(resume_skills), key=str.lower)
        a, b = st.columns(2)
        with a:
            st.markdown("#### ✅ Skills detected in both")
            if matched:
                st.markdown("".join(f'<span class="tag">{s}</span>' for s in matched), unsafe_allow_html=True)
            else:
                st.write("No keyword overlap detected yet.")
        with b:
            st.markdown("#### 🔎 Job keywords not found in resume")
            if missing:
                st.markdown("".join(f'<span class="tag tag-missing">{s}</span>' for s in missing), unsafe_allow_html=True)
            else:
                st.write("No missing keywords from this simple list.")
        st.caption("This score compares detected keywords only. It is not a prediction of interview or hiring success.")
        report = make_report(resume_text, resume_skills, job_description, job_skills, match_score)
        st.download_button("⬇ Download analysis report", data=report, file_name="nexus_resume_report.txt", mime="text/plain", use_container_width=True)

st.divider()
st.markdown(
    '<div style="text-align:center;color:#64748b;font-size:.82rem;padding:1rem 0;">✦ NEXUS AI · Built with Python & Streamlit · Analyze smarter. Improve continuously. Grow your career.</div>',
    unsafe_allow_html=True,
)
