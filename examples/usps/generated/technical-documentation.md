# Technical Documentation – TBD: Project Name

## 1. Document Control
| Field | Value |
| --- | --- |
| Project | TBD |
| Business Owner / Technical Owner | TBD / TBD |
| Version / Status | TBD / Draft |
| Created Date / Last Updated | TBD / TBD |
| Approvers | TBD |

## 2. Executive Summary/Business Justification
**Business justification:** The Postal Service has offered promotions and incentives (postage price discounts) since 2012 to maintain and grow the value of mail by encouraging mailers to adopt technologies and techniques that improve innovation and effectiveness. Examples include integrating digital technology with physical mail, improving mail quality and appeal through new print technology and techniques, and increasing personalization and targeting for higher ROI. Promotions are intended to increase direct-mail value and retain transactional-mail volumes for long-term product growth. Past analysis indicates that participating mailers have higher volume growth than nonparticipants. USPS is planning the 2027 Promotion Calendar based on the anticipated success of approved 2026 promotions.

**Desired outcome / success criteria:** Increase participation volume, attract new participants, and increase USPS revenue.

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
| `saldev.db_rpt.mailing_promotions_crid_high_account_t3` | TBD | Databricks API query | TBD | TBD | CRID-filtered source; schema not supplied |

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
FROM saldev.db_rpt.mailing_promotions_crid_high_account_t3
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
