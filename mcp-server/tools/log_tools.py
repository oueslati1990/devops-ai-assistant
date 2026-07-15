import re

ERROR_PATTERNS = [
    r"\bERROR\b",
    r"\bFATAL\b",
    r"\bPANIC\b",
    r"\bEXCEPTION\b",
    r"exit code [1-9]",
    r"OOMKilled",
    r"CrashLoopBackOff",
    r"ImagePullBackOff",
    r"Pending.*timeout",
]
WARN_PATTERNS = [r"\bWARN(ING)?\b", r"\bDEPRECATED\b", r"retrying"]


def analyze_logs(log_content: str, focus: str = "all") -> str:
    lines = log_content.splitlines()
    errors = []
    warnings = []

    for line in lines:
        is_error = any(re.search(p, line, re.IGNORECASE) for p in ERROR_PATTERNS)
        is_warning = any(re.search(p, line, re.IGNORECASE) for p in WARN_PATTERNS)

        if is_error:
            errors.append(line)
        if is_warning:
            warnings.append(line)

    output_parts = [f"Log analysis {len(lines)} lines in total"]
    output_parts.append(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    output_parts.append("")

    if focus in ["errors", "all"] and errors:
        output_parts.append("----ERRORS----")
        for e in errors[:20]:  # get only 20 to not overwhelm the LLM
            output_parts.append(e)

    if focus in ["warnings", "all"] and warnings:
        output_parts.append("----WARNINGS----")
        for w in warnings[:10]:
            output_parts.append(w)

    if not errors and not warnings:
        output_parts.append("No errors or warnings detected !")

    return "\n".join(output_parts)
