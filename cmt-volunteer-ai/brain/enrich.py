import yaml
from brain.llm_client import call_llm

# Load prompts safely
with open("config/prompts.yaml", "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)

def enrich_bio(bio_text):
    """
    Always returns valid enrichment output.
    Never returns None.
    """

    # Default fallback (VERY IMPORTANT)
    result = {
        "skills": [],
        "persona": "Needs Guidance",
        "confidence": 0.3
    }

    if not bio_text or not bio_text.strip():
        return result

    try:
        skills_raw = call_llm(PROMPTS["skill_extraction"], bio_text)
        persona_raw = call_llm(PROMPTS["persona_classification"], bio_text)
        confidence_raw = call_llm(PROMPTS["confidence"], bio_text)

        # Parse skills safely
        try:
            skills = eval(skills_raw) if isinstance(skills_raw, str) else []
            if not isinstance(skills, list):
                skills = []
        except:
            skills = []

        # Parse confidence safely
        try:
            confidence = float(confidence_raw)
            confidence = max(0.0, min(confidence, 1.0))
        except:
            confidence = 0.3

        result = {
            "skills": skills,
            "persona": persona_raw.strip() if persona_raw else "Needs Guidance",
            "confidence": confidence
        }

    except Exception as e:
        # Silent fallback but still return something
        pass

    return result
