import os
import re

def _load_health_terms():
    """
    Load health conditions from data/health-issues.txt (imported from your attachment),
    normalize to lowercase, include aliases found in parentheses, and return a list
    sorted by length (desc) to match longer phrases first and reduce double-counting.
    """
    terms: set[str] = set()
    path = os.path.join(os.path.dirname(__file__), "data", "health-issues.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                # lines look like "- Acne", "- Diabetes (Type 1 and Type 2)"
                # remove leading dash bullets
                if line.startswith("- "):
                    line = line[2:]
                line = line.strip().lower()

                # extract aliases inside parentheses, e.g. "high blood pressure (hypertension)"
                aliases = re.findall(r"$$([^)]+)$$", line)
                base = re.sub(r"$$[^)]*$$", "", line).strip()

                # add base term
                if base:
                    terms.add(base)

                # add each alias separately, split by commas if present
                for alias in aliases:
                    alias = alias.strip().lower()
                    if alias:
                        # split multiple aliases like "type 1 and type 2" are left intact as one phrase
                        terms.add(alias)

        # sort by length desc so longer phrases are considered first
        return sorted([t for t in terms if t], key=len, reverse=True)
    except Exception:
        # Fallback to the original short list if file missing
        return ["diabetes", "hypertension", "asthma", "cancer", "cardio", "thyroid", "kidney", "liver"]

_HEALTH_ISSUE_TERMS = _load_health_terms()

def _matched_health_terms(text: str) -> list[str]:
    """
    Find matched health terms in the user's free-text. Attempts to reduce
    double-counting synonyms by preferring longer phrases first and skipping
    terms that are substrings of already matched phrases.
    """
    if not text:
        return []
    normalized = " " + re.sub(r"\s+", " ", text.lower()) + " "
    matched: list[str] = []
    for term in _HEALTH_ISSUE_TERMS:
        if not term:
            continue
        # basic containment; we prefer longer terms first
        if term in normalized:
            # skip if this term is contained in an already matched longer term or vice versa
            if any(term in m or m in term for m in matched):
                continue
            matched.append(term)
    return matched

def compute_raf(profile):
    # Simple weighted RAF based on attachment guidance. Range ~0..1.5 then clamp to 0..1.
    age = max(0, min(100, int(profile.get("age", 0) or 0)))
    health_issues_text = (profile.get("health_issues") or "").strip().lower()
    smoking = bool(profile.get("smoking"))
    alcohol = bool(profile.get("alcohol"))
    income_inr = int(profile.get("annual_income_inr") or 0)

    # Base risk from age
    if age < 30:
        age_risk = 0.15
    elif age < 45:
        age_risk = 0.35
    elif age < 60:
        age_risk = 0.55
    else:
        age_risk = 0.75

    # Health issues risk (now uses the comprehensive list)
    issues = _matched_health_terms(health_issues_text)
    health_risk = min(0.6, 0.2 + 0.15 * len(issues)) if issues else (0.1 if health_issues_text else 0.0)

    lifestyle_risk = 0.2 * int(smoking) + 0.1 * int(alcohol)

    # Income can affect affordability buffer; lower income slightly increases risk exposure (INR)
    if income_inr < 300_000:
        income_risk = 0.15
    elif income_inr < 800_000:
        income_risk = 0.1
    else:
        income_risk = 0.05

    raf = age_risk + health_risk + lifestyle_risk + income_risk
    return max(0.0, min(1.0, raf))

def format_inr(n):
    try:
        n = int(n)
    except Exception:
        return f"₹{n}"
    # Basic Indian numbering format (lakh/crore)
    s = str(abs(n))
    if len(s) <= 3:
        res = s
    else:
        res = s[-3:]
        s = s[:-3]
        while len(s) > 2:
            res = s[-2:] + "," + res
            s = s[:-2]
        if s:
            res = s + "," + res
    return f"{'-' if n < 0 else ''}₹{res}"
