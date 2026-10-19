# ExportFlow AI

**An export documentation review copilot — portfolio prototype**

ExportFlow AI helps an exporter compare structured fields from a commercial invoice and packing list, flag discrepancies, validate basic arithmetic, and download a CSV comparison report for human review.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run app.py
```

The app opens in your browser. The **Use sample shipment** option is enabled by default. Click **Compare Documents** to see an example quantity and total-value mismatch. To use your own data, uncheck the sample option and upload a CSV or JSON file for each document.

## Upload format

Upload CSV or JSON files with fields such as:

- `Invoice Number` / `invoice_number`
- `Buyer` / `buyer_name`
- `Currency`
- `Product` / `product_description`
- `Quantity`
- `Unit Price` / `unit_price`
- `Total Value` / `total_value`
- `Destination` / `country_of_destination`

CSV files should contain one record per document for this prototype. JSON should be a single object or a list containing one object. Field names are compared as provided, so use consistent names across both files.

## Current capabilities

- Compare fields across a commercial invoice and packing list.
- Flag matching, mismatching, or missing values.
- Show counts for fields checked, passed checks, discrepancies, and missing information.
- Check whether quantity multiplied by unit price matches the stated total, when the needed numeric fields are available.
- Download comparison results as a CSV report.

## Limitations

- This build compares structured CSV/JSON data; it does not extract text from PDFs.
- Checks are rule-based; the prototype is not connected to a language model.
- It does not verify official customs or legal compliance.
- Sample records are synthetic. Human review is required before acting on any result.

## Repository contents

- `app.py` — Streamlit prototype
- `PRD.md` — product requirements and acceptance criteria
- `CASE_STUDY.md` — problem hypothesis, design choices, and evaluation plan
- `requirements.txt` — dependencies
