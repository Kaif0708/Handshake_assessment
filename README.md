# log-report — Terminal-Bench 2 (Harbor) Task

## Overview

**Task Name:** `dynamo/log-report`  
**Category:** Data Processing → Log Parsing  
**Difficulty:** Beginner–Intermediate  
**Estimated Expert Time:** 30 minutes  

This task evaluates an agent's ability to parse a raw HTTP server access log, extract structured metrics from unstructured text, and produce a correctly formatted JSON report. It tests fundamental skills in text processing, regex-based parsing, and structured data serialisation.

---

## Task Description

The agent is given a web server access log at `/app/data/access.log` in the standard **Apache/Nginx Combined Log Format**. It must:

1. Count every line in the file as one HTTP request (`total_requests`).
2. Identify lines where the HTTP status code falls in the `4xx` or `5xx` range (client and server errors).
3. Calculate the `error_rate` as a percentage of total requests.
4. Write a valid JSON file to `/app/report.json` with exactly the following structure:

```json
{
    "total_requests": 1542,
    "error_rate": 4.150453955901426
}
```

---

## Directory Structure

```
log-report/
├── README.md                  ← This file
├── task.toml                  ← Task manifest (metadata, resource limits, artifact paths)
├── instruction.md             ← Agent-facing task instructions
├── environment/
│   ├── Dockerfile             ← Docker image definition for the task environment
│   └── data/
│       └── access.log         ← Input log file (1542 lines, Apache/Nginx Combined Format)
├── tests/
│   ├── test.sh                ← Verifier entry-point shell script
│   └── test_outputs.py        ← Pytest test suite (3 criteria)
└── solution/
    └── solve.sh               ← Reference solution script
```

---

## Log File Format

`access.log` follows the **Combined Log Format** used by Apache and Nginx:

```
<IP> - - [<Date>] "<Method> <Path> HTTP/1.1" <Status> <Bytes> <Referrer> "<User-Agent>"
```

**Example line:**
```
192.168.1.1 - - [04/Jul/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0 ..."
```

### Log Composition

| Metric | Value |
|--------|-------|
| Total lines | **1542** |
| Successful responses (2xx, 3xx) | 1478 |
| Error responses (4xx, 5xx) | 64 |
| Error rate | **≈ 4.15%** |

Status codes used:
- **Success:** `200`, `201`, `301`, `302`, `304`
- **Errors:** `400`, `401`, `403`, `404`, `500`, `503`

---

## Technical Approach

### Reference Solution (`solution/solve.sh`)

The solution embeds a Python 3 script inside a Bash script for maximum portability within the Docker environment.

**Step-by-step logic:**

1. **Open** `/app/data/access.log` for reading line by line.
2. **Strip** whitespace and skip any blank lines.
3. **Increment** `total_requests` for every non-blank line.
4. **Apply a regex** to extract the HTTP status code field:
   ```python
   pattern = re.compile(r'^.*? ".*?" (\d{3})')
   ```
   The regex matches the quoted request string (`"GET /path HTTP/1.1"`) and captures the three-digit status code that follows it.
5. **Check** if the captured status code `>= 400` and `< 600` — increment `errors` if true.
6. **Compute** `error_rate = (errors / total_requests) * 100`.
7. **Serialise** the result as JSON and write to `/app/report.json`.

### Why Python Inside Bash?

- The Docker image (`python:3.11-slim-bookworm`) provides Python 3 out of the box.
- Bash acts as the outer runner (consistent with Terminal-Bench's `solve.sh` convention).
- Python's `json` and `re` standard library modules require **no additional dependencies**.
- This avoids fragile `awk`/`sed` pipelines while remaining portable.

---

## Verification

### Test Runner (`tests/test.sh`)

```bash
pytest tests/test_outputs.py --json-ctrf=/logs/verifier/ctrf.json
```

Writes a binary reward signal to `/logs/verifier/reward.txt`:
- `1` → all tests passed
- `0` → one or more tests failed

The CTRF JSON report provides structured, machine-readable test results for the Harbor platform.

### Test Suite (`tests/test_outputs.py`)

Three independent pytest test functions map directly to the three success criteria:

| Test | Criterion | Assertion |
|------|-----------|-----------|
| `test_criterion_1_file_exists_and_is_valid_json` | File exists and is parseable JSON | `os.path.exists` + `json.load` |
| `test_criterion_2_total_requests_metric` | `total_requests` is correct integer | `== 1542` |
| `test_criterion_3_error_rate_metric` | `error_rate` is within tolerance | `pytest.approx(4.15, rel=0.01)` |

> **Tolerance note:** `pytest.approx` with `rel=0.01` allows up to ±1% relative deviation, accommodating minor floating-point differences across implementations while still requiring a genuinely correct parse.

---

## Environment

| Setting | Value |
|---------|-------|
| Base image | `python:3.11-slim-bookworm` (pinned SHA digest) |
| Pre-installed packages | `pytest`, `pytest-json-ctrf` |
| CPUs | 1 |
| Memory | 2048 MB |
| Storage | 10240 MB |
| Internet access | Enabled |
| Agent timeout | 120 seconds |
| Verifier timeout | 120 seconds |
| Build timeout | 600 seconds |

---

## Running Locally (Docker)

```bash
# Build the image
docker build -t log-report -f environment/Dockerfile .

# Run the solution
docker run --rm log-report bash solution/solve.sh

# Run the verifier
docker run --rm log-report bash tests/test.sh
```

---

## Key Design Decisions

- **Pinned image digest** in the Dockerfile ensures fully reproducible builds regardless of upstream updates to `python:3.11-slim-bookworm`.
- **Line-counting** (not regex-matching) is used for `total_requests` — every non-blank line counts as one request, making the metric immune to malformed log lines.
- **Regex targets the status field by position** (after the quoted request string), not by scanning for any 3-digit number, reducing false positives from IP addresses or byte counts.
- **64 error lines** were chosen to produce a clean `≈4.15%` rate against 1542 total, satisfying the `pytest.approx` tolerance without hard-coding a rounded number.
