"""Combine all KB parts into diseases.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen_kb_part1 import get_part1
from gen_kb_part2 import get_part2
from gen_kb_part3 import get_part3

def main():
    all_diseases = get_part1() + get_part2() + get_part3()
    dest = Path(__file__).resolve().parent.parent.parent / "knowledge_base"
    dest.mkdir(parents=True, exist_ok=True)
    with open(dest / "diseases.json", "w", encoding="utf-8") as f:
        json.dump(all_diseases, f, indent=2, ensure_ascii=False)
    print(f"[OK] Generated diseases.json with {len(all_diseases)} entries")

if __name__ == "__main__":
    main()
