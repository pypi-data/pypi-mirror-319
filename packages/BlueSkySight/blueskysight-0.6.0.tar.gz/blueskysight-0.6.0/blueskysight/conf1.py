import re


vulnerability_lookup_base_url = "http://127.0.0.1:5000/"
vulnerability_auth_token = "qoBZi2sv6v6BRRRoxsMl2vbgesT6bT7Vl0zVUia1OHYi-xj5BM3JsaLbfL0eAd5P_ByV3r17nE3jY-xYusWzXA"


vulnerability_patterns = re.compile(
    r"\b(CVE-\d{4}-\d{4,})\b"  # CVE pattern
    r"|\b(GHSA-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4})\b"  # GHSA pattern
    r"|\b(PYSEC-\d{4}-\d{2,5})\b"  # PYSEC pattern
    r"|\b(GSD-\d{4}-\d{4,5})\b"  # GSD pattern
    r"|\b(wid-sec-w-\d{4}-\d{4})\b"  # CERT-Bund pattern
    r"|\b(cisco-sa-\d{8}-[a-zA-Z0-9]+)\b"  # CISCO pattern
    r"|\b(RHSA-\d{4}:\d{4})\b",  # RedHat pattern
    re.IGNORECASE,
)

# DID of accounts to ignore
ignore = ["did:plc:xrwz7tco7wyptkqee3wbjmci"]
