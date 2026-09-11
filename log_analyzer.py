import re


def analyze_log(log):
    error_type = "Unknown Error"
    message = log.strip()
    likely_cause = "Unable to determine"
    severity = "Medium"

    if "ModuleNotFoundError" in log:
        error_type = "Missing Python Module"
        likely_cause = "A required Python package is missing"
        severity = "High"

    elif "ImportError" in log:
        error_type = "Import Error"
        likely_cause = "A required module or dependency could not be imported"
        severity = "High"

    elif "SyntaxError" in log:
        error_type = "Syntax Error"
        likely_cause = "The source code contains invalid Python syntax"
        severity = "High"

    elif "NameError" in log:
        error_type = "Name Error"
        likely_cause = "A variable or function is being used before definition"
        severity = "Medium"

    elif "TypeError" in log:
        error_type = "Type Error"
        likely_cause = "An operation is being performed on an incompatible data type"
        severity = "Medium"

    elif "404" in log:
        error_type = "HTTP 404"
        likely_cause = "The requested route or resource was not found"
        severity = "Medium"

    elif "500" in log:
        error_type = "HTTP 500"
        likely_cause = "The server encountered an internal error"
        severity = "High"

    return {
        "error_type": error_type,
        "message": message,
        "likely_cause": likely_cause,
        "severity": severity
    }