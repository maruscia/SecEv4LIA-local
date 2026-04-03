from secev4lia import SecEv4LIA

OLLAMA_BASE = "http://localhost:11434"
VICTIM_MODEL = "Almawave/Velvet:2b"
JUDGE_MODEL = "huihui_ai/lfm2.5-abliterated:latest"

# SecEv4LIA runs fully offline — results saved to local SQLite
agent = SecEv4LIA(name=VICTIM_MODEL, endpoint=OLLAMA_BASE, agent_type="ollama")

results = agent.hack(
    attack_config={
        "attack_type": "flipattack",
        "dataset": {"preset": "harmbench", "limit": 10},
        "flipattack_params": {"flip_mode": "FCS", "cot": False},
        "judges": [
            {
                "identifier": JUDGE_MODEL,
                "endpoint": OLLAMA_BASE,
                "agent_type": "ollama",
                "type": "harmbench",
            }
        ],
    }
)
print(results)
