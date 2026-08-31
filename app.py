"""
app.py

Main Streamlit application file. This is the entry point of Plant Doctor AI.
"""

import streamlit as st
from api import identify_plant, generate_care_guide, identify_plant_from_text
from utils import get_top_matches

st.set_page_config(
    page_title="Plant Doctor AI",
    page_icon="🌿",
    layout="wide"
)

# ----- Custom Styling -----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,500&family=Karla:wght@400;500;600;700&display=swap');

    html, body,
    .stApp,
    section[data-testid="stMain"],
    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }

    .stApp {
        background-color: #FAF7F0;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFDF9;
        border-right: 1px solid #ECE4D3;
    }

    .sidebar-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2D3B2D;
        margin-bottom: 1.5rem;
    }

    .sidebar-section-label {
        font-family: 'Karla', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        color: #9CA69D;
        font-weight: 700;
        margin: 1.2rem 0 0.6rem 0;
        text-transform: uppercase;
    }

    .recent-item {
        font-family: 'Karla', sans-serif;
        font-size: 0.9rem;
        color: #4A5A4C;
        padding: 0.35rem 0;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: #2D3B2D !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-family: 'Karla', sans-serif !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #3D4E3D !important;
    }

    .hero-heading {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 600;
        color: #2D3B2D;
        text-align: center;
        margin-bottom: 0.6rem;
    }

    .hero-heading em {
        color: #8A8F5C;
        font-style: italic;
    }

    .hero-subtext {
        font-family: 'Karla', sans-serif;
        color: #6B7566;
        text-align: center;
        font-size: 1.05rem;
        max-width: 520px;
        margin: 0 auto 2.4rem auto;
        line-height: 1.5;
    }

    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #ECE4D3;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        display: flex;
        align-items: flex-start;
        gap: 0.9rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(45, 59, 45, 0.05);
    }

    .feature-card.disabled {
        opacity: 0.55;
    }

    .feature-icon {
        font-size: 1.6rem;
        line-height: 1;
    }

    .feature-title {
        font-family: 'Karla', sans-serif;
        font-weight: 700;
        color: #2D3B2D;
        font-size: 1rem;
        margin-bottom: 0.15rem;
    }

    .feature-desc {
        font-family: 'Karla', sans-serif;
        color: #8A9389;
        font-size: 0.85rem;
    }

    .coming-soon-badge {
        display: inline-block;
        font-size: 0.65rem;
        font-family: 'Karla', sans-serif;
        font-weight: 700;
        color: #B08A5C;
        background-color: #F5EBDC;
        padding: 0.1rem 0.5rem;
        border-radius: 20px;
        margin-left: 0.4rem;
        vertical-align: middle;
    }

    div[data-testid="stPopoverBody"] .stButton > button {
        border-radius: 12px !important;
        width: 100% !important;
        background-color: #FFFFFF !important;
        color: #2D3B2D !important;
        border: 1px solid #ECE4D3 !important;
        justify-content: flex-start !important;
        text-align: left !important;
        font-weight: 500 !important;
    }

    /* =====================================================================
       SEARCH BAR
       Uses Streamlit's official container "key" feature (st.container(key=...))
       which produces a stable, real CSS class (.st-key-searchbar) that works
       identically on localhost AND on Streamlit Cloud -- unlike fragile
       CSS hacks based on DOM position or :has() tricks.

       Layout is forced into one row (flex-wrap: nowrap) at every screen size,
       so it never stacks or breaks onto multiple lines on mobile.
       ===================================================================== */

    .st-key-searchbar > div {
        background-color: #FFFFFF;
        border: 2px solid #E4DCC8;
        border-radius: 28px;
        box-shadow: 0 1px 4px rgba(45, 59, 45, 0.06);
        padding: 0.25rem;
    }

    .st-key-searchbar [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
    }

    /* Camera column: small, fixed width, never grows or shrinks */
    .st-key-searchbar [data-testid="stColumn"]:nth-child(1) {
        flex: 0 0 2.8rem !important;
        width: 2.8rem !important;
        max-width: 2.8rem !important;
    }

    /* Text input column: takes all remaining space */
    .st-key-searchbar [data-testid="stColumn"]:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* Send column: small, fixed width, never grows or shrinks */
    .st-key-searchbar [data-testid="stColumn"]:nth-child(3) {
        flex: 0 0 2.8rem !important;
        width: 2.8rem !important;
        max-width: 2.8rem !important;
    }

    /* Camera button: circular, transparent, centered emoji, no chevron */
    .st-key-searchbar div[data-testid="stPopover"] > button {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        border-radius: 50% !important;
        width: 2.6rem !important;
        height: 2.6rem !important;
        min-width: 2.6rem !important;
        max-width: 2.6rem !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Streamlit auto-adds a dropdown chevron SVG to popover buttons --
       hide it so the camera button is a clean, uniform circle like Send */
    .st-key-searchbar div[data-testid="stPopover"] > button svg {
        display: none !important;
    }

    .st-key-searchbar div[data-testid="stPopover"] > button p {
        margin: 0 !important;
        line-height: 1 !important;
        font-size: 1.1rem !important;
    }

    /* Text input: borderless, blends into the pill container */
    .st-key-searchbar .stTextInput > div > div > input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0.6rem 0.4rem !important;
        font-size: 0.95rem !important;
        font-family: 'Karla', sans-serif !important;
    }

    /* Send button: identical circular size/shape to the camera button */
    .st-key-searchbar .stButton > button {
        background-color: #2D3B2D !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50% !important;
        width: 2.6rem !important;
        height: 2.6rem !important;
        min-width: 2.6rem !important;
        max-width: 2.6rem !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.1rem !important;
    }

    .st-key-searchbar .stButton > button p {
        margin: 0 !important;
        line-height: 1 !important;
    }

    /* Mobile: shrink everything slightly so it comfortably fits narrow screens,
       but keep the exact same one-line layout and matching button sizes */
    @media (max-width: 600px) {
        .st-key-searchbar [data-testid="stColumn"]:nth-child(1),
        .st-key-searchbar [data-testid="stColumn"]:nth-child(3) {
            flex: 0 0 2.3rem !important;
            width: 2.3rem !important;
            max-width: 2.3rem !important;
        }

        .st-key-searchbar div[data-testid="stPopover"] > button,
        .st-key-searchbar .stButton > button {
            width: 2.1rem !important;
            height: 2.1rem !important;
            min-width: 2.1rem !important;
            max-width: 2.1rem !important;
            font-size: 0.95rem !important;
        }

        .st-key-searchbar .stTextInput > div > div > input {
            font-size: 0.82rem !important;
            padding: 0.5rem 0.3rem !important;
        }

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    .result-header {
        background-color: #FFFFFF;
        border: 1px solid #ECE4D3;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .result-plant-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #2D3B2D;
    }

    .result-scientific-name {
        font-family: 'Karla', sans-serif;
        font-style: italic;
        color: #8A9389;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .confidence-badge {
        display: inline-block;
        background-color: #EAF2EC;
        color: #4A7856;
        font-family: 'Karla', sans-serif;
        font-weight: 600;
        font-size: 0.8rem;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
    }

    .care-item {
        background-color: #FFFFFF;
        border: 1px solid #ECE4D3;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }

    .care-label {
        font-family: 'Karla', sans-serif;
        font-weight: 700;
        color: #2D3B2D;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }

    .care-value {
        font-family: 'Karla', sans-serif;
        color: #5C6B5D;
        font-size: 0.9rem;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ----- Session State Setup -----
defaults = {
    "screen": "home",
    "history": [],
    "identification_results": None,
    "confirmed_plant": None,
    "care_guide": None,
    "search_query": "",
    "search_attempted": False,
    "search_error": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_diagnosis_state():
    """Clears everything related to an in-progress identification,
    so the user can start a fresh diagnosis."""
    st.session_state.identification_results = None
    st.session_state.confirmed_plant = None
    st.session_state.care_guide = None
    st.session_state.search_attempted = False
    st.session_state.search_error = None


# ----- Sidebar -----
def show_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🌿 Plant Doctor AI</div>', unsafe_allow_html=True)

        if st.button("➕  New Diagnosis", use_container_width=True):
            reset_diagnosis_state()
            st.session_state.screen = "home"
            st.rerun()

        st.markdown('<div class="sidebar-section-label">Recent Enquiries</div>', unsafe_allow_html=True)

        if st.session_state.history:
            for item in reversed(st.session_state.history[-5:]):
                st.markdown(f'<div class="recent-item">• {item}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="recent-item" style="color:#B7BEB8;">No enquiries yet</div>', unsafe_allow_html=True)


# ----- Home Screen -----
def show_home_screen():
    st.markdown(
        '<div class="hero-heading">Help your garden <em>thrive.</em></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtext">Instant plant identification and professional, '
        'AI-generated care guides — in English, Urdu, or Roman Urdu.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌿</div>
            <div>
                <div class="feature-title">Identify Plant</div>
                <div class="feature-desc">Snap or upload a photo of any species</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div>
                <div class="feature-title">Search by Name</div>
                <div class="feature-desc">English, Urdu, or Roman Urdu</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="feature-card disabled">
            <div class="feature-icon">🩺</div>
            <div>
                <div class="feature-title">Diagnose Health<span class="coming-soon-badge">Coming Soon</span></div>
                <div class="feature-desc">Analyze spots, wilting, or pests</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card disabled">
            <div class="feature-icon">🔔</div>
            <div>
                <div class="feature-title">Watering Reminders<span class="coming-soon-badge">Coming Soon</span></div>
                <div class="feature-desc">Never forget to water again</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    with st.container(key="searchbar"):
        col_camera, col_input, col_send = st.columns([1, 6, 1], vertical_alignment="center")

        with col_camera:
            with st.popover("📷", use_container_width=True):
                st.markdown("**Add a photo**")
                if st.button("📷  Take a Photo", use_container_width=True):
                    reset_diagnosis_state()
                    st.session_state.screen = "camera"
                    st.rerun()
                if st.button("📁  Upload from Gallery", use_container_width=True):
                    reset_diagnosis_state()
                    st.session_state.screen = "upload"
                    st.rerun()

        with col_input:
            user_query = st.text_input(
                "Search",
                placeholder="Ask about a plant — Rose, gulab...",
                label_visibility="collapsed"
            )

        with col_send:
            search_clicked = st.button("🔍", use_container_width=True)

    if (search_clicked or user_query) and user_query.strip():
        reset_diagnosis_state()
        st.session_state.search_query = user_query.strip()
        st.session_state.screen = "search_results"
        st.rerun()


# ----- Reusable: Care Guide Display -----
def display_care_guide(common_name, scientific_name, confidence, care_guide):
    """
    Renders a plant's identity + full AI-generated care guide in styled cards.
    Reused by the Upload, Camera, and Search Results screens.
    """
    confidence_html = (
        f'<span class="confidence-badge">{confidence}% match</span>'
        if confidence is not None else ""
    )

    st.markdown(f"""
    <div class="result-header">
        <div class="result-plant-name">🌿 {common_name}</div>
        <div class="result-scientific-name">{scientific_name}</div>
        {confidence_html}
    </div>
    """, unsafe_allow_html=True)

    field_display = {
        "water_requirement": ("💧", "Water"),
        "sunlight": ("☀️", "Sunlight"),
        "soil_type": ("🌱", "Soil Type"),
        "temperature": ("🌡️", "Temperature"),
        "fertilizer": ("🪴", "Fertilizer"),
        "pruning_tips": ("✂️", "Pruning Tips"),
        "common_diseases": ("🐛", "Common Diseases"),
        "toxicity": ("⚠️", "Toxicity"),
        "flowering_season": ("🌼", "Flowering Season"),
        "humidity": ("🫧", "Humidity"),
        "best_growing_conditions": ("📍", "Best Growing Conditions"),
        "interesting_fact": ("💡", "Interesting Fact"),
    }

    for key, (icon, label) in field_display.items():
        value = care_guide.get(key, "N/A")
        st.markdown(f"""
        <div class="care-item">
            <div class="care-label">{icon} {label}</div>
            <div class="care-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    guide_text_lines = [
        f"PLANT DOCTOR AI - CARE GUIDE",
        f"=" * 40,
        f"Plant: {common_name}",
        f"Scientific Name: {scientific_name}",
        ""
    ]
    for key, (icon, label) in field_display.items():
        value = care_guide.get(key, "N/A")
        guide_text_lines.append(f"{label}: {value}")

    guide_text = "\n".join(guide_text_lines)

    st.download_button(
        label="⬇️ Download Guide",
        data=guide_text,
        file_name=f"{common_name.replace(' ', '_')}_care_guide.txt",
        mime="text/plain",
        use_container_width=True
    )


# ----- Shared: Image Identification Flow (used by Upload and Camera) -----
def handle_image_identification(image_file):
    """
    Shared logic for identifying a plant from ANY image source
    (uploaded file or camera photo) and generating its care guide.
    """

    if st.session_state.confirmed_plant and st.session_state.care_guide:
        plant = st.session_state.confirmed_plant
        display_care_guide(
            plant["common_name"],
            plant["scientific_name"],
            plant.get("confidence_percent"),
            st.session_state.care_guide
        )
        return

    if st.session_state.identification_results is None:
        if st.button("🔍 Identify This Plant", use_container_width=True):
            with st.spinner("Identifying your plant... this may take a few seconds"):
                result = identify_plant(image_file)

            if not result["success"]:
                st.error(result["error"])
            elif not result["results"]:
                st.warning("We couldn't identify this plant. Try a clearer photo.")
            else:
                st.session_state.identification_results = get_top_matches(result["results"], top_n=3)
                st.rerun()
        return

    matches = st.session_state.identification_results
    top_match = matches[0]

    st.write("")
    if top_match["confidence_percent"] >= 50:
        st.success(f"We're fairly confident this is **{top_match['common_name']}** ({top_match['confidence_percent']}% match)")
    else:
        st.info("We're not fully sure -- please pick the correct match below:")

    for i, match in enumerate(matches):
        col_info, col_btn = st.columns([4, 1], vertical_alignment="center")
        with col_info:
            st.write(f"**{match['common_name']}** — *{match['scientific_name']}* ({match['confidence_percent']}%)")
        with col_btn:
            if st.button("Select", key=f"select_match_{i}", use_container_width=True):
                st.session_state.confirmed_plant = match
                st.rerun()

    if st.session_state.confirmed_plant and not st.session_state.care_guide:
        plant = st.session_state.confirmed_plant
        with st.spinner(f"Generating a care guide for {plant['common_name']}..."):
            guide_result = generate_care_guide(plant["common_name"], plant["scientific_name"])

        if guide_result["success"]:
            st.session_state.care_guide = guide_result["care_guide"]
            st.session_state.history.append(plant["common_name"])
            st.rerun()
        else:
            st.error(guide_result["error"])


# ----- Upload Screen -----
def show_upload_screen():
    st.markdown('<div class="hero-heading" style="font-size:1.8rem;">📁 Upload a Photo</div>', unsafe_allow_html=True)
    st.write("")

    if st.session_state.confirmed_plant and st.session_state.care_guide:
        handle_image_identification(None)
        return

    uploaded_file = st.file_uploader(
        "Upload a clear photo of the plant (leaf, flower, or whole plant)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        return

    st.image(uploaded_file, caption="Your uploaded photo", width=300)
    handle_image_identification(uploaded_file)


# ----- Camera Screen -----
def show_camera_screen():
    st.markdown('<div class="hero-heading" style="font-size:1.8rem;">📷 Take a Photo</div>', unsafe_allow_html=True)
    st.write("")

    if st.session_state.confirmed_plant and st.session_state.care_guide:
        handle_image_identification(None)
        return

    camera_photo = st.camera_input("Take a photo of the plant")

    if camera_photo is None:
        return

    handle_image_identification(camera_photo)


# ----- Search Results Screen -----
def show_search_results_screen():
    """
    Handles the text-based search flow:
    1. Take the raw query the user typed on the home screen (any of the 3 languages)
    2. Ask Groq to identify the plant name (identify_plant_from_text)
    3. Ask Groq to generate a care guide (generate_care_guide)
    4. Display the result using the same display_care_guide() helper as Upload
    """
    query = st.session_state.search_query

    st.markdown(
        f'<div class="hero-heading" style="font-size:1.8rem;">🔍 Searching for "{query}"</div>',
        unsafe_allow_html=True
    )
    st.write("")

    if st.session_state.confirmed_plant and st.session_state.care_guide:
        plant = st.session_state.confirmed_plant
        display_care_guide(
            plant["common_name"],
            plant["scientific_name"],
            None,
            st.session_state.care_guide
        )
        return

    if not st.session_state.search_attempted:
        with st.spinner("Understanding your query..."):
            id_result = identify_plant_from_text(query)

        st.session_state.search_attempted = True

        if id_result["success"]:
            st.session_state.confirmed_plant = {
                "common_name": id_result["common_name"],
                "scientific_name": id_result["scientific_name"],
            }
        else:
            st.session_state.search_error = id_result["error"]

        st.rerun()

    if st.session_state.search_error:
        st.error(st.session_state.search_error)
        if st.button("🔙 Back to Home", use_container_width=True):
            reset_diagnosis_state()
            st.session_state.screen = "home"
            st.rerun()
        return

    if st.session_state.confirmed_plant and not st.session_state.care_guide:
        plant = st.session_state.confirmed_plant
        with st.spinner(f"Generating a care guide for {plant['common_name']}..."):
            guide_result = generate_care_guide(plant["common_name"], plant["scientific_name"])

        if guide_result["success"]:
            st.session_state.care_guide = guide_result["care_guide"]
            st.session_state.history.append(plant["common_name"])
            st.rerun()
        else:
            st.error(guide_result["error"])


# ----- Main App Router -----
show_sidebar()

if st.session_state.screen == "home":
    show_home_screen()
elif st.session_state.screen == "camera":
    show_camera_screen()
elif st.session_state.screen == "upload":
    show_upload_screen()
elif st.session_state.screen == "search_results":
    show_search_results_screen()