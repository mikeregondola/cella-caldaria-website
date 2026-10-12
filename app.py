import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4


import json
import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4

SPREADSHEET_ID = "1KyyNgVfNP1kpn4YYD5oUbOHrU0OYasQnYsMwT6i6EIE"


@st.cache_resource
def get_worksheet():
    if "gcp_service_account" in st.secrets:
        # Streamlit Community Cloud or local Streamlit secrets
        credentials = dict(st.secrets["gcp_service_account"])
        client = gspread.service_account_from_dict(credentials)
    else:
        # Local fallback: credentials remain outside the project folder
        key_file = r"C:\Users\Administrator\.cella-caldaria\service-account.json"
        client = gspread.service_account(filename=key_file)

    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    return spreadsheet.worksheet("Website Leads")


def save_inquiry(name, contact, location, project_type, space, timeline, details):
    worksheet = get_worksheet()
    inquiry_id = "CC-" + uuid4().hex[:10].upper()
    submitted_at = datetime.now(ZoneInfo("Asia/Manila")).strftime("%Y-%m-%d %H:%M:%S")

    row = [
        inquiry_id, submitted_at, name.strip(), contact.strip(),
        location.strip(), project_type, space, timeline, details.strip(),
        "Yes", "Website", "New", "", "", "", "Not Started", "", ""
    ]

    worksheet.append_row(row, value_input_option="RAW")
    return inquiry_id

st.set_page_config(
    page_title="Cella Caldaria | Turn Space Into Wellness",
    page_icon="♨️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(135deg, #243832, #40594b);
        color: #ffffff;
        padding: 3rem 2rem;
        border-radius: 18px;
        margin-bottom: 2rem;
    }
    .hero h1 {color: #ffffff; font-size: clamp(2rem, 5vw, 3.5rem);}
    .hero p {font-size: 1.15rem; line-height: 1.7;}
    .eyebrow {
        letter-spacing: 0.15em;
        font-weight: 700;
        color: #c8a96b;
    }
    .section {padding: 1rem 0 2rem 0;}
    .contact {
        background: #f1eee6;
        color: #243832;
        border-radius: 16px;
        padding: 1.5rem;
    }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button {
        background: #243832;
        border-color: #243832;
    }
</style>
""", unsafe_allow_html=True)

PHONE = "0927 066 4317"
EMAIL = "mikeregondola@gmail.com"
FACEBOOK = "https://facebook.com/cellacaldariaph/"


hero_text, hero_image = st.columns([1.2, 0.8], gap="large")

with hero_text:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">CELLA CALDARIA</div>
      <h1>Your Space. Your Steam Room. Your Wellness.</h1>
      <p>We design and build complete steam-room projects for homes,
      resorts, pools, fitness facilities and wellness spaces.</p>
      <p><strong>TURN SPACE INTO WELLNESS.</strong></p>
    </div>
    """, unsafe_allow_html=True)

with hero_image:
    st.image(
        "hero_steamroom.jpg",
        use_container_width=True,
        caption="Real steam-room project",
    )

if st.button("SHOW US YOUR SPACE", type="primary", use_container_width=True):
    st.session_state["show_inquiry"] = True

st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("Transform Your Space")
st.write(
    "An existing bathroom, a suitable underused room, or a planned "
    "poolside or hospitality project may offer an opportunity for a "
    "steam room. Every project needs to be assessed for space, "
    "construction, ventilation, drainage, electrical and equipment requirements."
)
st.markdown("</div>", unsafe_allow_html=True)

st.header("Complete Steam-Room Projects")
st.write(
    "Cella Caldaria provides a complete project service: design, "
    "construction, installation and commissioning. Steam equipment "
    "is part of the complete project; we do not offer standalone "
    "steam-generator installation as a separate service."
)

st.header("Who We Serve")
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Residential")
    st.write("Homeowners planning a new build, renovation or private wellness space.")
with c2:
    st.subheader("Hospitality & Wellness")
    st.write("Resorts, hotels, spas, pools and fitness facilities.")
with c3:
    st.subheader("Project Partners")
    st.write("Contractors, architects, interior designers, pool builders and developers.")

st.header("Tell Us About Your Project")
st.write("Share a few details. We can discuss your space and the next steps.")

if "show_inquiry" not in st.session_state:
    st.session_state["show_inquiry"] = False

with st.form("project_inquiry", clear_on_submit=False):
    name = st.text_input("Your name *")
    contact = st.text_input("Phone number or email *")
    location = st.text_input("Project location (city or province) *")
    project_type = st.selectbox(
        "What kind of project is this?",
        [
            "Select a project type",
            "New home / residential",
            "Bathroom conversion / renovation",
            "Poolside steam room",
            "Resort / hotel",
            "Spa / wellness business",
            "Fitness / sports facility",
            "Project partner enquiry",
            "Other",
        ],
    )
    space = st.selectbox(
        "What is the status of the space?",
        [
            "Not decided yet",
            "Existing bathroom",
            "Existing room / underused space",
            "New construction",
            "Poolside / outdoor area",
            "Commercial / hospitality space",
        ],
    )
    timeline = st.selectbox(
        "When are you considering the project?",
        ["Just exploring", "Within 1–3 months", "Within 3–6 months", "More than 6 months"],
    )
    details = st.text_area("Anything else we should know? (optional)")
    consent = st.checkbox(
        "I agree that Cella Caldaria may use these details to respond to my enquiry."
    )
    submitted = st.form_submit_button("Submit project enquiry", type="primary")

    if submitted:
        if not name.strip() or not contact.strip() or not location.strip():
            st.error("Please complete your name, contact details and project location.")
        elif project_type == "Select a project type":
            st.error("Please select a project type.")
        elif not consent:
            st.error("Please consent to the use of your details so we can respond.")

        else:
           try:
               inquiry_id = save_inquiry(
                   name=name,
                   contact=contact,
                   location=location,
                   project_type=project_type,
                   space=space,
                   timeline=timeline,
                   details=details,
               )
               st.success(
                   f"Thank you! Your enquiry was saved successfully. "
                   f"Reference: {inquiry_id}"
               )
           except Exception:
               st.error(
                   "We couldn't save your enquiry right now. "
                   "Please contact us directly using the details below."
               )

st.markdown("---")
st.subheader("SHOW US YOUR SPACE.")
st.write(f"**Phone:** {PHONE}")
st.write(f"**Email:** {EMAIL}")
st.markdown(f"**Facebook:** [Cella Caldaria Facebook Page]({FACEBOOK})")
st.markdown("**CELLA CALDARIA — TURN SPACE INTO WELLNESS.**")

st.caption(
    "Project feasibility, scope, technical requirements and pricing are "
    "confirmed after discussion and appropriate assessment."
)
