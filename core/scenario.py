import random, json, pathlib

SCENARIOS = json.loads(pathlib.Path("data/base_scenarios.json").read_text())

def random_scenario(role:str|None=None):
    """Returns a dict with company, contact_role, pain_points, objections"""
    pool = [s for s in SCENARIOS if (role is None or s["contact_role"] == role)]
    return random.choice(pool)

