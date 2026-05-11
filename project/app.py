# app.py
# pyrefly: ignore [missing-import]
import streamlit as st
from activities import recommend_activities
from core.moment_logic import get_moment_type
from core.memory import get_last_activity, save_last_activity
from services.llm import explain_recommendation
import models.feedback_store as fb

st.set_page_config(page_title="AI Activity Recommender")
st.title("🧠 AI Activity Recommender")

if "recs" not in st.session_state:
    st.session_state.recs = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = []

username = st.text_input("Enter your username", value="default_user", key="username_input")
if not username:
    username = "default_user"

time_of_day = st.selectbox("Time of day", ["Morning", "Afternoon", "Evening", "Night"])
energy = st.selectbox("Energy level", ["low", "medium", "high"])
location = st.selectbox(
    "Location",
    ["home", "library", "campus", "cafe", "bus", "train", "walking"]
)
time_available = st.selectbox("Time available (minutes)", [5, 15, 30, 60])

avoid = st.text_input("❌ I don’t want to do", key="avoid_input")
prefer = st.text_input("✅ I want to do", key="prefer_input")

# Tag filters
st.subheader("Filter by Categories")
col1, col2, col3 = st.columns(3)
with col1:
    physical = st.checkbox("Physical", key="physical")
    mental = st.checkbox("Mental", key="mental")
with col2:
    social = st.checkbox("Social", key="social")
    creative = st.checkbox("Creative", key="creative")
with col3:
    relax = st.checkbox("Relax", key="relax")
    productivity = st.checkbox("Productivity", key="productivity")

selected_tags = []
if physical: selected_tags.append("physical")
if mental: selected_tags.append("mental")
if social: selected_tags.append("social")
if creative: selected_tags.append("creative")
if relax: selected_tags.append("relax")
if productivity: selected_tags.append("productivity")

avoid_tags = [x.strip().lower() for x in avoid.split(",") if x] + ([tag for tag in selected_tags if st.checkbox(f"Avoid {tag}", key=f"avoid_{tag}")] if selected_tags else [])
prefer_tags = [x.strip().lower() for x in prefer.split(",") if x] + selected_tags

if "recs" not in st.session_state or st.button("✨ Recommend"):
    moment = get_moment_type(time_of_day, energy, location)
    st.session_state.moment = moment
    last = get_last_activity(username)

    with st.spinner("Generating personalized activities..."):
        recs = recommend_activities(
            moment,
            time_available,
            avoid_tags,
            prefer_tags,
            last,
            username
        )

    st.session_state.recs = recs
    st.session_state.feedback_given = [False] * len(recs)

if "recs" in st.session_state and st.session_state.recs:
    recs = st.session_state.recs
    moment = st.session_state.get("moment", "general_free_time")

    for i, rec in enumerate(recs):
        desc = rec["description"].replace("{time}", str(time_available))
        explanation = explain_recommendation(
            {
                "time_of_day": time_of_day,
                "energy": energy,
                "location": location,
                "time_available": time_available
            },
            rec["name"]
        )

        st.success(f"✅ {rec['name']}")
        st.write(desc)
        st.info(explanation)

        if st.session_state.feedback_given[i]:
            st.write("Feedback given ✅")
        else:
            feedback = st.feedback("thumbs", key=f"feedback_{i}")
            if feedback == "thumbs_up":
                fb.give_feedback(username, moment, rec["name"], True)
                st.session_state.feedback_given[i] = True
            elif feedback == "thumbs_down":
                fb.give_feedback(username, moment, rec["name"], False)
                st.session_state.feedback_given[i] = True
