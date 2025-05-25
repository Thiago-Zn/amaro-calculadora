"""params.py - leitura e escrita de parâmetros"""

import json

PARAMS_FILE = "config/parametros.json"

def load_params():
    with open(PARAMS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_params(data):
    with open(PARAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
