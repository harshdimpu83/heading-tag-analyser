"""
Heading Tag Analyser - Streamlit App
Enter a website URL and see all H1, H2, H3, H4, H5, H6 tags with counts.
"""

import streamlit as st
import os

from heading_analyzer_core import fetch_headings, get_total_headings, HEADING_TAGS

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Heading Tag Analyser",
    page_icon="🏷️",
    layout="wide"
)

# ============================================================================
# PASSWORD PROTECTION
# ============================================================================

def check_password():
    """Returns True if user entered correct password"""
    query_params = st.query_params

    def password_entered():
        if st.session_state["password"] == os.getenv("APP_PASSWORD", "heading2026"):
            st.session_state["password_correct"] = True
            st.query_params["auth"] = "true"
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if query_params.get("auth") == "true":
        st.session_state["password_correct"] = True
        return True

    if "password_correct" not in st.session_state:
        st.text_input(
            "🔒 Enter Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.info("Enter your password to access the Heading Tag Analyser")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "🔒 Enter Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Incorrect password")
        return False
    return True


if not check_password():
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.title("🏷️ Heading Tag Analyser")
st.caption("Enter any website URL to see how many H1, H2, H3, H4, H5, H6 headings it has")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ℹ️ How to Use")
    st.info("""
    1. Paste a website URL below
    2. Click **Analyse Headings**
    3. See the count and text of every heading tag on the page

    **Tips:**
    - Works with or without `https://`
    - H1 should ideally appear only once per page (SEO best practice)
    - H2s are main sections, H3s are subsections
    """)

    st.markdown("---")
    st.markdown("### 📖 What are heading tags?")
    st.markdown("""
    Heading tags structure a webpage's content:
    - **H1** — Page title (should be unique)
    - **H2** — Main sections
    - **H3** — Subsections
    - **H4–H6** — Deeper structure
    """)

# ============================================================================
# URL INPUT
# ============================================================================

st.markdown("### Enter Website URL")

url_input = st.text_input(
    "Website URL",
    placeholder="https://example.com",
    help="Paste the full URL of any webpage"
)

analyse_clicked = st.button("🔍 Analyse Headings", type="primary", disabled=not url_input.strip())

# ============================================================================
# RUN ANALYSIS
# ============================================================================

if analyse_clicked and url_input.strip():
    with st.spinner(f"Fetching {url_input.strip()}..."):
        result = fetch_headings(url_input.strip())
    st.session_state["last_result"] = result
    st.rerun()

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

if "last_result" in st.session_state:
    result = st.session_state["last_result"]

    st.markdown("---")
    st.markdown("### 📊 Results")

    if not result["success"]:
        st.error(f"❌ {result['error']}")
        st.stop()

    headings = result["headings"]
    total = get_total_headings(headings)

    st.success(f"✅ Found **{total} heading tag(s)** on `{result['url']}`")

    # ── Summary count table ──────────────────────────────────────────────────
    st.markdown("#### Heading Count Summary")

    cols = st.columns(6)
    tag_colors = {
        "h1": "#FF4B4B",
        "h2": "#FF8C00",
        "h3": "#FFD700",
        "h4": "#32CD32",
        "h5": "#1E90FF",
        "h6": "#9370DB",
    }

    for i, tag in enumerate(HEADING_TAGS):
        count = len(headings[tag])
        color = tag_colors[tag]
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: {color}22;
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 16px;
                    text-align: center;
                ">
                    <div style="font-size: 28px; font-weight: bold; color: {color};">{count}</div>
                    <div style="font-size: 16px; font-weight: 600;">{tag.upper()}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SEO note for H1 ─────────────────────────────────────────────────────
    h1_count = len(headings["h1"])
    if h1_count == 0:
        st.warning("⚠️ No H1 found. Every page should have exactly one H1 for good SEO.")
    elif h1_count > 1:
        st.warning(f"⚠️ {h1_count} H1 tags found. Best practice is to have only 1 H1 per page.")
    else:
        st.success("✅ H1 count is perfect — exactly 1.")

    # ── Heading texts breakdown ──────────────────────────────────────────────
    st.markdown("#### Heading Texts")

    any_found = False
    for tag in HEADING_TAGS:
        texts = headings[tag]
        if not texts:
            continue
        any_found = True
        color = tag_colors[tag]
        with st.expander(f"{tag.upper()} — {len(texts)} found", expanded=(tag == "h1")):
            for i, text in enumerate(texts, 1):
                st.markdown(
                    f'<span style="color:{color}; font-weight:600;">#{i}</span> {text}',
                    unsafe_allow_html=True,
                )

    if not any_found:
        st.info("No heading tags found on this page.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("Heading Tag Analyser | Kashtbhanjan Digital | Deploy: Render")
