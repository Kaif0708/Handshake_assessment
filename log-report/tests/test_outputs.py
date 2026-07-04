import os
import json
import pytest

REPORT_PATH = "/app/report.json"

def test_criterion_1_file_exists_and_is_valid_json():
    """Verifies Success Criterion 1: The output file must be a valid JSON file located at the absolute path /app/report.json."""
    assert os.path.exists(REPORT_PATH), f"Expected report file to exist at {REPORT_PATH}"
    try:
        with open(REPORT_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("The generated file is not valid JSON.")
    assert isinstance(data, dict), "The root of the JSON file must be an object."

def test_criterion_2_total_requests_metric():
    """Verifies Success Criterion 2: The JSON object must contain a key 'total_requests' mapping to the total integer count of log lines parsed."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert "total_requests" in data, "The key 'total_requests' is missing from the JSON report."
    assert isinstance(data["total_requests"], int), "The field 'total_requests' must be an integer."
    assert data["total_requests"] == 1542, "Log count mismatch."

def test_criterion_3_error_rate_metric():
    """Verifies Success Criterion 3: The JSON object must contain a key 'error_rate' representing the percentage of requests that resulted in a 4xx or 5xx HTTP status code, formatted as a float."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert "error_rate" in data, "The key 'error_rate' is missing from the JSON report."
    assert isinstance(data["error_rate"], (int, float)), "The field 'error_rate' must be numeric."
    assert pytest.approx(data["error_rate"], 0.01) == 4.15
