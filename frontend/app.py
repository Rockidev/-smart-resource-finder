import streamlit as st
import requests

API = "http://127.0.0.1:8000"

# ================= SIDEBAR =================
st.sidebar.title(" Smart Resource Finder")

st.sidebar.markdown("""
### How to Use
1. Select a subject  
2. Search for a resource  
3. Choose the top-rated one
""")

st.sidebar.markdown("""
### Version / Status
**Version:** v1.0  
 Learning & Experimental
""")

st.sidebar.markdown("---")
st.sidebar.caption("Built by **Harsh**")

# ================= MAIN PAGE =================
st.title("Smart Resource Finder")

# ---------- FETCH DATA ----------
response = requests.get(f"{API}/resources")
resources = response.json()

# ---------- DYNAMIC SUBJECT LIST ----------
subjects = sorted(list(set(r["subject"] for r in resources)))
selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

# ---------- SEARCH (SUBJECT-WISE ONLY) ----------
search_query = st.text_input("Search resource (within subject)")

# ---------- FILTER ----------
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
    rid = st.number_input("ID", min_value=1)
    subject = st.text_input("Subject")
    name = st.text_input("Resource Name")
    rtype = st.selectbox("Type", ["Notes", "Video", "Book"])
    link = st.text_input("Resource Link")

    submit = st.form_submit_button("Add")

    if submit:
        payload = {
            "id": rid,
            "subject": subject,
            "name": name,
            "resource_type": rtype,
            "link": link,

            "avg_rating": 0,
            "rating_count": 0
        }
        requests.post(f"{API}/resource", json=payload)
        st.success("Resource added. Refresh page.")

# ---------- DISPLAY ----------
st.subheader(" Resources")

if not filtered:
    st.info("No resources found.")
else:
    for idx, r in enumerate(filtered):
        st.markdown(f"### {r['name']}")
        st.caption(f"{r['subject']} | {r['resource_type']} ")
        st.markdown(f"[🔗 Open Resource]({r['link']})")
        st.write(f" {round(r['avg_rating'], 2)} ({r['rating_count']} ratings)")

        rating = st.slider(
            "Rate",
            1, 5, 3,
            key=f"slider_{r['id']}_{idx}"
        )

        if st.button("Submit Rating", key=f"btn_{r['id']}_{idx}"):
            requests.post(
                f"{API}/rate",
                params={
                    "resource_id": r["id"],
                    "rating": rating
                }
            )
            st.success("Rating submitted. Refresh page.")
