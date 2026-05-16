import streamlit as st
from streamlit_option_menu import option_menu

from services.pdf_service import extract_text_from_pdf
from services.analysis_service import analyze_resume

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #040816,
        #0a1026,
        #111827
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #050816;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Cards */
.card {
    background: rgba(17,24,39,0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 25px;
    margin-bottom: 20px;
}

/* Score */
.score {
    font-size: 80px;
    font-weight: 700;
    color: #00f5a0;
}

/* Small Labels */
.label {
    color: #9ca3af;
    font-size: 15px;
}

/* Role Tags */
.role-tag {
    display:inline-block;
    padding:10px 18px;
    margin:8px;
    border-radius:30px;
    background:rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.08);
}

/* Section */
.section-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    # 🚀 AI Resume Analyzer
    ### Smart ATS Resume Review
    """)

    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Analysis", "Suggestions"],
        icons=["house", "bar-chart", "lightbulb"],
        default_index=0
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

# =====================================================
# ANALYZE
# =====================================================

data = None

if uploaded_file:

    resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing Resume..."):
        data = analyze_resume(resume_text)

# =====================================================
# NO FILE
# =====================================================

if not data:

    st.markdown("""
    <br><br><br>

    <center>

    <h1 style="font-size:90px;">🚀</h1>

    <h1 style="font-size:60px;">
    AI Resume Analyzer
    </h1>

    <p style="color:#9ca3af;font-size:20px;">
    Upload your resume and get professional ATS analysis
    </p>

    </center>
    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

elif selected == "Dashboard":

    score = float(data["score"])

    if score > 10:
        score = score / 10

    score = round(score, 1)

    ats = int(score * 10)

    st.markdown("""
    <div class="section-title">
    Dashboard 👋
    </div>

    <p class="label">
    Here's your resume analysis overview
    </p>
    """, unsafe_allow_html=True)

    # =================================================
    # TOP SECTION
    # =================================================

    col1, col2, col3 = st.columns([1.5,1,1])

    with col1:

        st.markdown(f"""
        <div class="card">

        <h2>Resume Score</h2>

        <div class="score">
        {score}/10
        </div>

        <h3 style="color:#00f5a0;">
        ★ Excellent
        </h3>

        <p>
        You're in the top 20% of candidates 🔥
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.metric(
            "ATS Score",
            f"{ats}%"
        )

        st.progress(ats)

    with col3:

        st.markdown("""
        <div class="card">

        <h3>Score Breakdown</h3>

        ✅ Content Quality <br><br>
        📄 Structure <br><br>
        💻 Skills Match <br><br>
        🏆 Experience <br><br>
        🚀 Achievements

        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # SUMMARY SECTION
    # =================================================

    col4, col5, col6, col7 = st.columns(4)

    with col4:

        st.markdown("""
        <div class="card">
        <h2>📝 Summary</h2>
        """, unsafe_allow_html=True)

        st.write(data["summary"])

        st.markdown("</div>", unsafe_allow_html=True)

    with col5:

        st.markdown("""
        <div class="card">
        <h2>💪 Strengths</h2>
        """, unsafe_allow_html=True)

        for s in data["strengths"]:
            st.success(s)

        st.markdown("</div>", unsafe_allow_html=True)

    with col6:

        st.markdown("""
        <div class="card">
        <h2>⚠️ Weaknesses</h2>
        """, unsafe_allow_html=True)

        for w in data["weaknesses"]:
            st.error(w)

        st.markdown("</div>", unsafe_allow_html=True)

    with col7:

        st.markdown("""
        <div class="card">
        <h2>💡 Suggestions</h2>
        """, unsafe_allow_html=True)

        for s in data["suggestions"]:
            st.info(s)

        st.markdown("</div>", unsafe_allow_html=True)

    # =================================================
    # ROLES
    # =================================================

    st.markdown("""
    <div class="card">

    <h2>🎯 Recommended Roles</h2>

    """, unsafe_allow_html=True)

    role_html = ""

    for role in data["recommended_roles"]:

        role_html += f"""
        <span class="role-tag">
        🚀 {role}
        </span>
        """

    st.markdown(role_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS PAGE
# =====================================================

elif selected == "Analysis":

    st.markdown("""
    <div class="section-title">
    Resume Analysis 📊
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💪 Strengths")

        for s in data["strengths"]:
            st.success(s)

    with col2:

        st.subheader("⚠️ Weaknesses")

        for w in data["weaknesses"]:
            st.error(w)

# =====================================================
# SUGGESTIONS PAGE
# =====================================================

elif selected == "Suggestions":

    st.markdown("""
    <div class="section-title">
    AI Suggestions 💡
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Improvement Suggestions")

    for s in data["suggestions"]:
        st.info(s)

    st.subheader("🎯 Recommended Roles")

    cols = st.columns(2)

    for index, role in enumerate(data["recommended_roles"]):

        with cols[index % 2]:
            st.success(role)