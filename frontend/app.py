import streamlit as st
import json
from pathlib import Path

# ---------- FILE SETUP ----------
DATA_FILE = Path(__file__).parent / "data.json"

if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")

def load_data():
    return json.loads(DATA_FILE.read_text())

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


# ---------- SIDEBAR ----------
st.sidebar.title(" Smart Resource Finder")

st.sidebar.markdown("""
### How to Use
1. Select a subject  
2. Search resources  
3. Choose the top-rated one
""")

st.sidebar.markdown("""
### Version / Status
**Version:** v1.0  
 Learning & Experimental
""")

st.sidebar.markdown("---")
st.sidebar.caption("Built by **Harsh Dev**")


# ---------- MAIN ----------
st.title("Smart Resource Finder")

resources = load_data()

# ---------- SUBJECT FILTER ----------
subjects = sorted(list(set(r["subject"] for r in resources)))
selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

# ---------- SEARCH ----------
search_query = st.text_input("Search resource (within subject)")

filtered = resources

if selected_subject != "All":
    filtered = [r for r in filtered if r["subject"] == selected_subject]

if search_query:
    q = search_query.lower()
    filtered = [
        r for r in filtered
        if q in r["name"].lower()
        or q in r["resource_type"].lower()
        or q in r["link"].lower()
    ]

# ---------- ADD RESOURCE ----------
st.subheader(" Add Resource")

with st.form("add_form"):
    subject = st.text_input("Subject")
    name = st.text_input("Resource Name")
    rtype = st.selectbox("Type", ["Notes", "Video", "Book"])
    link = st.text_input("Resource Link")
    submit = st.form_submit_button("Add")

    if submit:
        new_id = max([r["id"] for r in resources], default=0) + 1

        resources.append({
            "id": new_id,
            "subject": subject,
            "name": name,
            "resource_type": rtype,
            "link": link,
            "avg_rating": 0,
            "rating_count": 0
        })

        save_data(resources)
        st.success("Resource added. Refresh page.")

# ---------- DISPLAY ----------
st.subheader(" Resources")

if not filtered:
    st.info("No resources found.")
else:
    for idx, r in enumerate(filtered):
        st.markdown(f"### {r['name']}")
        st.caption(f"{r['subject']} | {r['resource_type']}")
        st.markdown(f"[🔗 Open Resource]({r['link']})")
        st.write(f" {round(r['avg_rating'],2)} ({r['rating_count']} ratings)")

        rating = st.slider(
            "Rate",
            1, 5, 3,
            key=f"slider_{r['id']}_{idx}"
        )

        if st.button("Submit Rating", key=f"btn_{r['id']}_{idx}"):
            total = r["avg_rating"] * r["rating_count"] + rating
            r["rating_count"] += 1
            r["avg_rating"] = total / r["rating_count"]

            save_data(resources)
            st.success("Rating submitted. Refresh page.")
