# Test Plan and Scenarios – CRID-Scoped Promotion API

## Context
Business objective: Increase participation volume; Attract new participants; Increase USPS revenue

Implementation under test: MuleSoft sends a CRID parameter to an API supported by a Databricks App. The service queries the referenced table and returns a JSON response containing only records where the table CRID equals the MuleSoft-provided CRID.

Source table: `saldev.db_rpt.mailing_promotions_crid_high_account_t3`. Use synthetic/mocked data only; production data and credentials are not required.

## Traceability and scenarios
| ID | Documentation requirement | Scenario | Expected result |
| --- | --- | --- | --- |
| TS-01 | FR-1, FR-2 | Positive exact match | Mock records for requested CRID are returned; every `crid` equals request. |
| TS-02 | FR-3 | Cross-CRID isolation | Mixed mock records never return a record for another CRID. |
| TS-03 | FR-1 | Missing/null/malformed CRID | Reject; do not issue an unfiltered query. |
| TS-04 | FR-1 | Whitespace/case/type boundaries | Apply only the documented TBD contract; otherwise reject ambiguity. |
| TS-05 | FR-5 | No-result CRID | Return documented successful empty JSON collection. |
| TS-06 | FR-2 | Duplicate matching rows | Behavior is documented; no nonmatching row is returned. |
| TS-07 | FR-3 | SQL injection payload | Bound parameter is treated as a value; no broadened result. |
| TS-08 | FR-4 | JSON schema/serialization | Approved fields only; JSON is valid and preserves CRID invariant. |
| TS-09 | NFR | Authorization/security | Unauthorized access follows TBD contract and reveals no data. |
| TS-10 | NFR | Upstream/downstream failure and timeout/retry | Documented safe error/retry behavior; no leaked data. |
| TS-11 | NFR | Logging/auditing | Correlation/audit data meets TBD policy without response/sensitive data. |
| TS-12 | NFR | Performance, concurrency, regression | Meets TBD thresholds under concurrent scoped requests; prior cases continue passing. |

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
FROM saldev.db_rpt.mailing_promotions_crid_high_account_t3
WHERE crid = :crid
```

Never use string concatenation, interpolated request input, or `SELECT *`. The endpoint, status codes, field schema, authorization model, response limits, retry policy, and performance thresholds remain TBD and require approval before production testing.
