"""params.py - leitura e escrita de parâmetros""\"
import json
from pathlib import Path

PARAM_FILE = Path(__file__).parent.parent / 'config' / 'parametros.json'

def load_params():
    with open(PARAM_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_params(params):
    with open(PARAM_FILE, 'w', encoding='utf-8') as f:
        json.dump(params, f, indent=2)
