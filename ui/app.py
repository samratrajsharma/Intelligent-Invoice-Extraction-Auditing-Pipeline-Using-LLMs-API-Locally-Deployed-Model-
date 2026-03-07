import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Financial Intelligence Platform", layout="wide")

st.title("AI Financial Intelligence Dashboard")

tab1, tab2, tab3, tab4 = st.tabs([
    "Upload Document",
    "Analytics",
    "Vendor Insights",
    "AI Assistant"
])

# -------------------------
# Upload Document
# -------------------------

with tab1:

    st.header("Upload Financial Document")

    uploaded_file = st.file_uploader("Upload invoice / receipt")

    if uploaded_file:

        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        response = requests.post(
            f"{API_URL}/upload-document",
            files=files
        )

        if response.status_code != 200:
            st.error(f"API Error: {response.text}")
        else:
            result = response.json()

            st.success("Document processed")

            st.json(result["structured_data"])

            if result.get("similar_documents"):
                st.subheader("Similar Documents Found")
                st.write(result["similar_documents"])

# -------------------------
# Analytics
# -------------------------

with tab2:

    st.header("System Analytics")

    if st.button("Load Analytics"):

        response = requests.get(f"{API_URL}/analytics")

        data = response.json()

        col1, col2 = st.columns(2)

        col1.metric("Total Documents", data["total_documents"])
        col2.metric("High Risk Documents", data["high_risk_documents"])

        df = pd.DataFrame(data["vendor_spending"])

        st.subheader("Vendor Spending")

        st.bar_chart(df.set_index("vendor"))

# -------------------------
# Vendor Intelligence
# -------------------------

with tab3:

    st.header("Vendor Intelligence")

    vendor = st.text_input("Enter Vendor Name")

    if st.button("Get Vendor Insights"):

        response = requests.get(
            f"{API_URL}/vendor-insights/{vendor}"
        )

        st.json(response.json())

# -------------------------
# AI Assistant
# -------------------------

with tab4:

    st.header("AI Financial Assistant")

    question = st.text_input("Ask a financial question")

    if st.button("Ask AI"):

        response = requests.post(
            f"{API_URL}/ask-ai",
            params={"question": question}
        )

        st.write(response.json()["answer"])