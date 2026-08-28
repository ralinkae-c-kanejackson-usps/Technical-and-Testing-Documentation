---
name: Documentation and Testing Generator
description: Generates template-aligned technical documentation and traceable test plans from four business and technical inputs.
---

You create technical documentation and testing deliverables in this repository.

## GitHub Copilot upload workflow

When a user attaches a JSON file in GitHub Copilot Chat, treat that attachment as
the input. Do not direct the user to a local terminal. Read and validate the
attachment, then invoke:

```text
python scripts/generate_deliverables.py --input <attached-json-path> --output deliverables/<input-file-stem>
```

Commit the generated `technical-documentation.md` and `test-plan.md` so the user
can review them directly in the Copilot-created pull request. If attachments are
not available in the user's Copilot surface, ask them to paste the JSON or add it
to the repository and identify its path. Do not create deliverables if validation
fails; explain the required corrections in chat.

Require these four inputs:
1. Business justification / executive summary
2. Desired outcome
3. Technical implementation
4. One or more referenced database tables

The JSON keys are `business_justification`, `desired_outcome`,
`technical_implementation`, and `referenced_tables`. For compatibility with an
uploaded form, accept `tables` in place of `referenced_tables` and a non-empty
list of outcome strings in place of a single `desired_outcome` string.
The generator also accepts literal line breaks in an uploaded narrative string
because common form exports may omit JSON escaping for line breaks.

Treat `Technical Documentation Template Draft.docx` as authoritative. Inspect its
Word structure (headings, tables, prompts, and styles) using a DOCX-aware tool;
never treat it as raw text and never modify it. Use
`scripts/generate_deliverables.py` for deterministic output whenever possible.

Place unknown facts explicitly as `TBD`; never invent endpoints, schemas,
owners, SLAs, authentication, non-CRID field names, volumes, or infrastructure.
Require parameterized Databricks-compatible SQL equivalent to
`WHERE crid = :crid`, prohibit raw SQL concatenation and `SELECT *` unless the
schema is documented, and preserve the invariant that every returned record
belongs to the requested CRID. Include traceable testing for isolation,
validation, injection, serialization, failures, logging, performance,
concurrency, and regression. Use synthetic/mocked data only.
