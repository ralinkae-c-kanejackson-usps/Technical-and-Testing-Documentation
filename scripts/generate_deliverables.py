#!/usr/bin/env python3
"""Generate template-aligned technical documentation and a traceable test plan."""

import argparse
import json
from pathlib import Path

TEMPLATE_SECTIONS = (
    "1. Document Control",
    "2. Executive Summary/Business Justification",
    "3. Scope & Requirements",
    "4. Source Tables",
    "5. Data Model Overview (New Tables)",
    "6. Detailed Table Specifications",
    "7. Data Lineage & Flow (Source → Gold/Dashboard)",
    "8. Transformation Logic & Business Rules",
    "9. Basic Data Quality & Validation",
    "10. Orchestration & Operations",
    "11. Consumption Guide",
    "12. Risks, Defects, Mitigations",
    "13. Testing & Deployment Summary",
    "14. Document Change Log",
)

REQUIRED_FIELDS = (
    "business_justification",
    "desired_outcome",
    "technical_implementation",
    "referenced_tables",
)
NARRATIVE_FIELDS = REQUIRED_FIELDS[:-1]


def validate_input(data):
    """Return a normalized input object or raise ValueError with all violations."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object.")
    errors = []
    for field in NARRATIVE_FIELDS:
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"'{field}' must be a non-empty string")
    tables = data.get("referenced_tables")
    if not isinstance(tables, list) or not tables:
        errors.append("'referenced_tables' must be a non-empty list")
    elif any(not isinstance(table, str) or not table.strip() for table in tables):
        errors.append("'referenced_tables' entries must be non-empty strings")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "business_justification": data["business_justification"].strip(),
        "desired_outcome": data["desired_outcome"].strip(),
        "technical_implementation": data["technical_implementation"].strip(),
        "referenced_tables": [table.strip() for table in tables],
    }


def technical_document(data):
    tables = "\n".join(
        f"| `{table}` | TBD | Databricks API query | TBD | TBD | CRID-filtered source; schema not supplied |"
        for table in data["referenced_tables"]
    )
    return f"""# Technical Documentation – TBD: Project Name

## 1. Document Control
| Field | Value |
| --- | --- |
| Project | TBD |
| Business Owner / Technical Owner | TBD / TBD |
| Version / Status | TBD / Draft |
| Created Date / Last Updated | TBD / TBD |
| Approvers | TBD |

## 2. Executive Summary/Business Justification
**Business justification:** {data["business_justification"]}

**Desired outcome / success criteria:** {data["desired_outcome"]}

**Problem statement:** Provide CRID-scoped promotion data to the requesting integration without exposing another CRID's records.

**In scope:** Validate a supplied CRID, retrieve only matching source records, and serialize an approved JSON response.
**Out of scope:** TBD: promotion rules, table maintenance, endpoint design, authentication, and consumer behavior not supplied.

## 3. Scope & Requirements
### 3.1 Functional Requirements
| ID | Requirement |
| --- | --- |
| FR-1 | The service accepts one CRID parameter from MuleSoft. |
| FR-2 | Every returned record has `crid` exactly equal to the validated requested CRID. |
| FR-3 | No CRID is accepted as an unfiltered-query fallback. |
| FR-4 | The service returns JSON; field allowlist and schema are TBD pending source-schema review. |
| FR-5 | A valid CRID with no matching records returns a successful empty JSON collection; HTTP/status contract is TBD. |

### 3.2 Non-Functional Requirements
Security, authorization, privacy classification, SLA, expected row count, timeout, retry policy, performance target, and availability are TBD. Logs/audit events must not expose response data or sensitive values and must support request correlation using an approved non-sensitive identifier (TBD).

### 3.3 Assumptions / Constraints
The contract for CRID type, case sensitivity, whitespace normalization, length, and permitted characters is TBD. Until documented, reject missing, null, malformed, or ambiguous input rather than coercing it. Databricks-compatible parameter binding is required; raw SQL concatenation is prohibited.

## 4. Source Tables
| Source Tables | Layer | Workflow | Refresh Times | Table Owner | Notes |
| --- | --- | --- | --- | --- | --- |
{tables}

## 5. Data Model Overview (New Tables)
| Table Name | Layer (Bronze/Source, Silver, Gold, Dashboard) | Purpose | Primary Key(s) | Workflow/Scheduled Job | Table Owner | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| None proposed | TBD | Read-only API response | TBD | TBD | TBD | No new tables supplied |

## 6. Detailed Table Specifications
### 6.1 Table: source schema TBD
| Column Name | Data Type | Nullable (Y/N) | Description | Allowed Values | Derivation | Notes | Permissions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `crid` | TBD | TBD | Request filter key | TBD | Source | Only confirmed field | TBD |
| `<approved_column_1>` | TBD | TBD | TBD | TBD | Source | Replace after schema review | TBD |

## 7. Data Lineage & Flow (Source → Gold/Dashboard)
### 7.1 Flow Narrative
1. MuleSoft submits one CRID parameter to the Databricks App-supported API.
2. The API validates the CRID under the TBD contract and authorizes the request under the TBD security model.
3. The API issues a parameterized query against the referenced source table.
4. The API verifies/maintains CRID isolation and serializes only approved fields as JSON.
5. MuleSoft receives the JSON collection or documented error/empty result.

### 7.2 Transformation Mapping
| From Object | To Object | Join/Key | Transformation Rule | Output Field |
| --- | --- | --- | --- | --- |
| MuleSoft CRID | Source table | `crid = :crid` | Validated bind parameter | `crid` |
| Source table | JSON response | `crid = :crid` | Approved-column allowlist; no cross-CRID rows | TBD |

## 8. Transformation Logic & Business Rules
**Core selection invariant:** Every query must be equivalent to `WHERE crid = :crid`.

Illustrative Databricks-compatible SQL (adapt column names only after schema review; not production-ready code):
```sql
SELECT crid, <approved_column_1>, <approved_column_2>
FROM {data["referenced_tables"][0]}
WHERE crid = :crid
```
Bind `:crid` through the supported Databricks client/connector parameter API. Never form SQL by interpolating or concatenating request input. Deduplication, late-arriving-data handling, KPI formulas, and exception/fallback rules are TBD.

## 9. Basic Data Quality & Validation
| Test Name | Test Scenario | SQL Script | Expected Results | Pass Criteria | Status | Data Tested | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRID isolation | Request one CRID | Parameterized query above | Only exact matching CRID rows | All returned `crid` values equal requested CRID | Planned | Synthetic fixture | No `SELECT *` |

Validation sign off: TBD.

## 10. Orchestration & Operations
Workflow/job, schedule, dependencies, runtime, retry policy, backfill procedure, failure runbook, monitoring, alert owner, and operational support model are TBD. Upstream/downstream failures and timeout/retry behavior must return the approved error contract without leaking data.

## 11. Consumption Guide
Primary consumer: MuleSoft (supplied). Approved use case: retrieve authorized, CRID-scoped promotion data. Endpoint, authentication/authorization, JSON schema, pagination, rate limits, and known limitations are TBD. Consumers must not infer a missing CRID means “all records.”

## 12. Risks, Defects, Mitigations
| Identified Risks Description | Impacts | Resolution | Owner | Notes |
| --- | --- | --- | --- | --- |
| Missing/unsafe CRID filter | Cross-CRID data leakage | Validate input; bind `:crid`; test invariant | TBD | Block release on failure |
| Unknown schema / response contract | Invalid or excess data exposure | Approve explicit output allowlist | TBD | Do not use `SELECT *` |
| Upstream/downstream failure | Unavailable or inconsistent response | Define error, timeout, retry, and monitoring contract | TBD | TBD |

## 13. Testing & Deployment Summary
Unit, integration, data, UAT, deployment version/date, rollback plan, environment promotion, and approvals are TBD. Execute the traceable scenarios in the companion test plan before deployment.

## 14. Document Change Log
| Date | Version | Change Description | Author | Reviewer/Approver |
| --- | --- | --- | --- | --- |
| TBD | TBD | Initial generated draft | TBD | TBD |
"""


def test_plan(data):
    table = data["referenced_tables"][0]
    cases = [
        ("TS-01", "FR-1, FR-2", "Positive exact match", "Mock records for requested CRID are returned; every `crid` equals request."),
        ("TS-02", "FR-3", "Cross-CRID isolation", "Mixed mock records never return a record for another CRID."),
        ("TS-03", "FR-1", "Missing/null/malformed CRID", "Reject; do not issue an unfiltered query."),
        ("TS-04", "FR-1", "Whitespace/case/type boundaries", "Apply only the documented TBD contract; otherwise reject ambiguity."),
        ("TS-05", "FR-5", "No-result CRID", "Return documented successful empty JSON collection."),
        ("TS-06", "FR-2", "Duplicate matching rows", "Behavior is documented; no nonmatching row is returned."),
        ("TS-07", "FR-3", "SQL injection payload", "Bound parameter is treated as a value; no broadened result."),
        ("TS-08", "FR-4", "JSON schema/serialization", "Approved fields only; JSON is valid and preserves CRID invariant."),
        ("TS-09", "NFR", "Authorization/security", "Unauthorized access follows TBD contract and reveals no data."),
        ("TS-10", "NFR", "Upstream/downstream failure and timeout/retry", "Documented safe error/retry behavior; no leaked data."),
        ("TS-11", "NFR", "Logging/auditing", "Correlation/audit data meets TBD policy without response/sensitive data."),
        ("TS-12", "NFR", "Performance, concurrency, regression", "Meets TBD thresholds under concurrent scoped requests; prior cases continue passing."),
    ]
    rows = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in cases)
    return f"""# Test Plan and Scenarios – CRID-Scoped Promotion API

## Context
Business objective: {data["desired_outcome"]}

Implementation under test: {data["technical_implementation"]}

Source table: `{table}`. Use synthetic/mocked data only; production data and credentials are not required.

## Traceability and scenarios
| ID | Documentation requirement | Scenario | Expected result |
| --- | --- | --- | --- |
{rows}

## Adaptable test asset
Use the following standard-library test pattern with mocked query results. It specifically enforces the core leakage-prevention invariant:

```python
def assert_crid_isolation(requested_crid, response_records):
    assert isinstance(response_records, list)
    assert all(record["crid"] == requested_crid for record in response_records)
```

For a production integration test, replace the mock with an approved non-production Databricks connection, bind `:crid` through its parameter API, and use an approved explicit column list:

```sql
SELECT crid, <approved_column_1>
FROM {table}
WHERE crid = :crid
```

Never use string concatenation, interpolated request input, or `SELECT *`. The endpoint, status codes, field schema, authorization model, response limits, retry policy, and performance thresholds remain TBD and require approval before production testing.
"""


def generate(data, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / "technical-documentation.md").write_text(technical_document(data), encoding="utf-8")
    (output / "test-plan.md").write_text(test_plan(data), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = validate_input(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    generate(data, args.output)


if __name__ == "__main__":
    main()
