# Product Requirements Document (PRD): ExportFlow AI

**Status:** Portfolio MVP prototype  
**Product area:** Export documentation review  
**Target users:** Operations staff at small and medium-sized Indian exporters

## 1. Problem hypothesis

Export operations can involve reviewing related documents and checking whether key information is consistent. Manual cross-checking may be repetitive, and missing or inconsistent values may require follow-up before a shipment progresses.

This is a problem hypothesis for the portfolio project and needs validation with exporters or freight-forwarding professionals.

## 2. Product objective

Help an export operations user identify potential inconsistencies between a commercial invoice and a packing list, understand which values differ, and prepare the comparison for human review.

## 3. Primary user story

As an export operations user, I want to compare key fields across shipment documents so that I can spot potential inconsistencies before sending the documents for further processing.

## 4. Current MVP scope

- Load a synthetic sample shipment or upload one-record CSV/JSON documents.
- Compare fields from the two inputs.
- Identify matching, mismatching, and missing values.
- Display summary counts and source values side by side.
- Check basic arithmetic using quantity, unit price, and total value where available.
- Download comparison results as CSV.
- Clearly communicate that human review is required.

## 5. Out of scope

- Automatic customs clearance or legal compliance certification.
- Sending documents to banks, customs, buyers, or logistics partners.
- User accounts, multi-tenant storage, and production security.
- Full PDF/OCR extraction in this MVP.
- Autonomous shipment approval.
- A connected LLM or autonomous AI agent.

## 6. Core fields

Invoice number, buyer name, currency, product description, quantity, unit price, total value, and destination country. The prototype compares the field names and values as supplied; users should keep field names consistent across files.

## 7. Acceptance criteria

- The sample shipment loads and surfaces a quantity difference (100 vs 90).
- The total-value difference (850 vs 765) is visible in the comparison.
- Matching fields are shown as matches.
- Missing information is surfaced instead of silently treated as valid.
- Unsupported or invalid uploads show an error where handled by the app.
- The comparison results can be downloaded as CSV.
- The product does not claim to certify trade compliance.

## 8. User journey

1. Open the shipment review page.
2. Use the sample shipment or upload two structured files.
3. Compare the documents.
4. Review summary counts and field-level values.
5. Inspect arithmetic validation when numeric fields are available.
6. Download the CSV and follow up manually.

## 9. Product metrics to evaluate

- **Seeded discrepancy recall:** known seeded discrepancies detected / total seeded discrepancies.
- **False-positive rate:** clean fields incorrectly flagged / total clean fields tested.
- **Review time:** elapsed time to identify and understand all seeded issues.
- **Task completion:** percentage of test users who complete the review without help.

These metrics are an evaluation plan, not measured results. Do not report results until tests have been run.

## 10. Risks and mitigations

- **False negatives:** test explicit comparison rules against known examples.
- **False positives:** show source values so a human can decide.
- **Sensitive trade data:** use synthetic data in demos and avoid uploading real customer information.
- **Compliance confusion:** state clearly that this is a review aid, not a legal or customs compliance system.

## 11. Next iteration

Validate the workflow with export operations users, add PDF text extraction/OCR with source snippets, support editable field corrections and audit history, and evaluate whether an LLM helps with ambiguous descriptions or explanations.
