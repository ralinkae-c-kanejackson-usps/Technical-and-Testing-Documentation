# Documentation and Testing Generator

This repository preserves `Technical Documentation Template Draft.docx` as the
authoritative template.  The generator produces Markdown deliverables whose
section order and table headings map directly to that template; it does not
modify the Word document.

## Quick start

Python 3.9+ and only the standard library are required.

```bash
# From the repository root:
python scripts/generate_deliverables.py \
  --input examples/usps/input.json \
  --output output/usps-deliverables
```

This creates `technical-documentation.md` and `test-plan.md`.  The checked-in
copies under `examples/usps/generated/` are the acceptance fixture.

## Inputs

Provide a JSON object with all four required categories:

```json
{
  "business_justification": "Why the work is needed.",
  "desired_outcome": "The measurable intended result.",
  "technical_implementation": "Known implementation facts.",
  "referenced_tables": ["catalog.schema.table_name"]
}
```

Each narrative value must be a non-empty string and `referenced_tables` must
be a non-empty list of non-empty strings. Unknown facts are rendered as
`TBD` rather than invented.

## Reusable Copilot agent

In GitHub Copilot Chat, select the **Documentation and Testing Generator**
custom agent in `.github/agents/documentation-testing.agent.md`. Attach your JSON
file and say: **“Generate deliverables from this attached JSON file.”** The agent
validates the attachment, runs the generator, and commits
`deliverables/<your-file-name>/technical-documentation.md` and `test-plan.md` to
its pull request. Review those files in GitHub; no local terminal is needed.

If attachment upload is unavailable, paste the JSON in Copilot Chat or commit it
to the repository and state its path. The agent will report validation errors
instead of generating incomplete deliverables. The uploaded form may use `tables`
instead of `referenced_tables`, and `desired_outcome` may be a non-empty list of
strings.
For compatibility with common form exports, literal line breaks in narrative
strings are accepted even though strict JSON normally requires them to be
escaped. Do not supply both table keys with different values.

## Layout

* `Technical Documentation Template Draft.docx` — authoritative, unchanged
  Word template.
* `scripts/generate_deliverables.py` — deterministic generator and validation.
* `examples/usps/input.json` — USPS CRID fixture.
* `examples/usps/generated/` — generated technical documentation and test plan.
* `tests/test_generator.py` — generator validation and output tests.

## Security and extension

Do not place credentials, production customer data, connection strings, or
tokens in inputs or outputs. The generated SQL uses a named `:crid` bind
parameter and explicit, schema-dependent column placeholders; replace those
placeholders with approved columns only after schema review. Extend
`TEMPLATE_SECTIONS` in the generator when the authoritative template changes,
then update its tests and regenerate fixtures. Generated examples are
illustrative, not production-ready API or database code.
