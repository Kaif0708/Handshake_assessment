#!/bin/bash
python3 -c '
import json
import re

log_file_path = "/app/data/access.log"
report_file_path = "/app/report.json"

total_requests = 0
errors = 0

log_pattern = re.compile(r"^.*? \".*?\" (\d{3})")

with open(log_file_path, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total_requests += 1
        match = log_pattern.match(line)
        if match:
            status_code = int(match.group(1))
            if 400 <= status_code < 600:
                errors += 1

if total_requests > 0:
    error_rate = (errors / total_requests) * 100
else:
    error_rate = 0.0

report_data = {
    "total_requests": total_requests,
    "error_rate": error_rate
}

with open(report_file_path, "w") as f:
    json.dump(report_data, f, indent=4)
'
