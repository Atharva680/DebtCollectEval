import json
import csv
import sys
import os

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

def export_results(results_path):
    if not os.path.exists(results_path):
        print(f"Error: {results_path} not found")
        return

    data = []
    with open(results_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    # 1. Raw JSON
    with open("results/raw_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 2. Raw CSV using native csv module
    if data:
        keys = data[0].keys()
        with open("results/raw_results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in data:
                # Convert complex types to string for CSV
                clean_row = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in row.items()}
                writer.writerow(clean_row)

    # 3. Metrics JSON
    metrics = analyze(results_path)
    with open("results/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("Exported: results/raw_results.json, results/raw_results.csv, results/metrics.json")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        export_results(sys.argv[1])
    else:
        export_results("results/results_qwen2.5_0.5b.jsonl")
