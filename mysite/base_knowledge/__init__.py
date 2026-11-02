from pathlib import Path

KNOWLEDGE = (Path(__file__).parent / 'auto.txt').read_text(encoding='utf-8')