RUBRIC = """
Score the rep 1‑5 on:
1. Uncovering true objection
2. Demonstrating empathy
3. Differentiating value
4. Closing with next‑step ask
Return JSON: {"scores": {...}, "feedback": "..."}"""

async def grade_transcript(history:list[dict]):
    graded = await chat([
        {"role":"system","content":RUBRIC},
        {"role":"user","content":str(history)}
    ])
    return graded.content

