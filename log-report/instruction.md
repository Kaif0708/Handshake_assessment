Please parse the server access log file located at /app/data/access.log and generate an aggregated JSON summary report. Your final script execution must process the file log entries completely and write the output precisely to the designated path below.

Output File Path:
/app/report.json

Success Criteria:
1. The output file must be a valid JSON file located at the absolute path /app/report.json.
2. The JSON object must contain a key "total_requests" mapping to the total integer count of log lines parsed.
3. The JSON object must contain a key "error_rate" representing the percentage of requests that resulted in a 4xx or 5xx HTTP status code, formatted as a float.
