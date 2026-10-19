import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ExportFlow AI",
    page_icon="📦",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

[data-testid="stMetric"] {
    background: #171e2b;
    border: 1px solid #30394a;
    padding: 18px;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📦 ExportFlow AI")
    st.caption("Export operations copilot")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Shipment Review", "About the Product"]
    )

    st.divider()
    st.caption("Prototype · Human review required")

if page == "About the Product":
    st.title("About ExportFlow AI")
    st.write(
        "ExportFlow AI helps export operations teams compare "
        "shipment document data, identify discrepancies, "
        "and prepare a review checklist."
    )

    st.subheader("Core capabilities")
    st.markdown("""
    - Cross-document field comparison
    - Missing-information detection
    - Arithmetic validation
    - Downloadable comparison reports
    """)

    st.info(
        "This prototype uses structured data and rule-based "
        "checks. It does not certify customs compliance."
    )
    st.stop()

st.title("Shipment Review")
st.caption(
    "Review shipment documents, identify inconsistencies, "
    "and resolve issues before further processing."
)

st.write(
    "Compare export documents and identify "
    "information that needs human review."
)

def get_sample_data():
    invoice = {
        "Invoice Number": "EXP-104",
        "Buyer": "Northstar Retail GmbH",
        "Currency": "USD",
        "Product": "Cotton T-shirts",
        "Quantity": 100,
        "Unit Price": 8.5,
        "Total Value": 850.0,
        "Destination": "Germany"
    }

    packing_list = {
        "Invoice Number": "EXP-104",
        "Buyer": "Northstar Retail GmbH",
        "Currency": "USD",
        "Product": "Cotton T-shirts",
        "Quantity": 90,
        "Unit Price": 8.5,
        "Total Value": 765.0,
        "Destination": "Germany"
    }

    return invoice, packing_list


def compare_documents(invoice, packing_list):
    results = []

    fields = list(dict.fromkeys(
        list(invoice.keys()) + list(packing_list.keys())
    ))

    for field in fields:
        a = invoice.get(field)
        b = packing_list.get(field)

        if a is None or b is None or str(a).strip() == "" or str(b).strip() == "":
            status = "Missing Information"
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
            status = "Match" if abs(a - b) < 0.000001 else "Mismatch"
        else:
            status = (
                "Match"
                if str(a).strip().casefold() == str(b).strip().casefold()
                else "Mismatch"
            )

        results.append({
            "Field": field,
            "Invoice": a if a is not None else "",
            "Packing List": b if b is not None else "",
            "Status": status
        })

    return pd.DataFrame(results)


st.divider()
st.header("Shipment Review")

use_sample = st.checkbox("Use sample shipment", value=True)

if use_sample:
    invoice, packing_list = get_sample_data()
    st.info("Sample shipment loaded.")
else:
    left, right = st.columns(2)

    with left:
        st.subheader("Commercial Invoice")
        invoice_file = st.file_uploader(
            "Upload invoice CSV or JSON",
            type=["csv", "json"],
            key="invoice_upload"
        )

    with right:
        st.subheader("Packing List")
        packing_file = st.file_uploader(
            "Upload packing list CSV or JSON",
            type=["csv", "json"],
            key="packing_upload"
        )

    def read_document(uploaded_file):
        if uploaded_file is None:
            return None

        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)

                if df.empty:
                    st.error("The uploaded CSV is empty.")
                    return None

                return df.iloc[0].to_dict()

            if uploaded_file.name.endswith(".json"):
                import json
                data = json.load(uploaded_file)

                if isinstance(data, list):
                    if not data:
                        st.error("The uploaded JSON is empty.")
                        return None
                    data = data[0]

                if not isinstance(data, dict):
                    st.error("JSON must contain an object or a list of objects.")
                    return None

                return data

        except Exception as error:
            st.error(f"Could not read the file: {error}")

        return None

    invoice = read_document(invoice_file)
    packing_list = read_document(packing_file)

if st.button("Compare Documents", type="primary"):
    if invoice is None or packing_list is None:
        st.error("Please provide both documents first.")
    else:
        st.session_state["results"] = compare_documents(
            invoice, packing_list
        )

if "results" in st.session_state:
    results = st.session_state["results"]

    mismatches = results[results["Status"] == "Mismatch"]
    missing = results[results["Status"] == "Missing Information"]

    st.divider()
    st.header("Comparison Results")

    matches = results[results["Status"] == "Match"]
    total_fields = len(results)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fields Checked", total_fields)
    c2.metric("Passed Checks", len(matches))
    c3.metric("Discrepancies", len(mismatches))
    c4.metric("Missing Information", len(missing))

    if len(mismatches) == 0 and len(missing) == 0:
        st.success("All compared fields match. Continue with the normal human review process.")
    else:
        st.warning(
            f"Review required: {len(mismatches)} discrepancy/discrepancies "
            f"and {len(missing)} field(s) with missing information."
        )

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Arithmetic Validation")

    if all(
        field in invoice and field in packing_list
        for field in ["Quantity", "Unit Price", "Total Value"]
    ):
        invoice_total = (
            float(invoice["Quantity"]) *
            float(invoice["Unit Price"])
        )

        packing_total = (
            float(packing_list["Quantity"]) *
            float(packing_list["Unit Price"])
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Invoice calculation**")
            st.write(
                f"{invoice['Quantity']} × "
                f"{invoice['Unit Price']} = {invoice_total:.2f}"
            )

            if abs(invoice_total - float(invoice["Total Value"])) < 0.01:
                st.success("Invoice arithmetic is consistent.")
            else:
                st.error("Invoice total does not match the calculation.")

        with col2:
            st.write("**Packing-list calculation**")
            st.write(
                f"{packing_list['Quantity']} × "
                f"{packing_list['Unit Price']} = {packing_total:.2f}"
            )

            if abs(packing_total - float(packing_list["Total Value"])) < 0.01:
                st.success("Packing-list arithmetic is consistent.")
            else:
                st.error("Packing-list total does not match the calculation.")
    else:
        st.info("Required numeric fields are not available for arithmetic validation.")
