
import json
from collections import Counter

def analyze(results_path):
    data = []
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    except Exception as e:
        return {"error": f"Could not read file: {str(e)}"}
    
    if not data:
        return {"error": "No data found in results file."}

    metrics = {}
    languages = ["en", "hi-en", "mr-en"]
    
    for lang in languages:
        lang_data = [d for d in data if d.get("language") == lang]
        if not lang_data:
            metrics[lang] = "No data"
            continue
            
        total = len(lang_data)
        passes = sum(1 for d in lang_data if d.get("score") == "PASS")
        missed = sum(1 for d in lang_data if d.get("metric") == "missed_call")
        spurious = sum(1 for d in lang_data if d.get("metric") == "spurious_call")
        malformed = sum(1 for d in lang_data if d.get("metric") == "malformed_argument")
        wrong_tool = sum(1 for d in lang_data if d.get("metric") == "wrong_tool")
        
        metrics[lang] = {
            "total": total,
            "accuracy": f"{(passes/total)*100:.2f}%",
            "missed_call": missed,
            "spurious_call": spurious,
            "malformed": malformed,
            "wrong_tool": wrong_tool
        }
    
    return metrics

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = analyze(sys.argv[1])
        print(json.dumps(res, indent=2))
    else:
        print("Usage: python analyze.py <results_file>")
