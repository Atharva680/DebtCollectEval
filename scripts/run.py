
import json
import requests
import os
import sys
from typing import List, Dict, Any, Optional
from evaluator import ScoringEngine

class OllamaHarness:
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        with open("configs/tools.json", "r") as f:
            self.tools = json.load(f)
        with open("configs/baseline.txt", "r") as f:
            self.prompt_template = f.read()

    def run_case(self, case: Dict) -> Dict:
        try:
            system_prompt = self.prompt_template.format(
                LENDER=case['lender'],
                NAME=case['name'],
                DPD=case['bucket'],
                PRODUCT=case['product'],
                AMOUNT=case['amount']
            )
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": case['borrower_turn']}
                ],
                "tools": self.tools,
                "stream": False,
                "options": {"temperature": 0.0}
            }
            
            response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            return {"tool_calls": result.get("message", {}).get("tool_calls", []), "raw": result}
        except Exception as e:
            return {"error": str(e), "tool_calls": []}

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5:0.5b"
    suite_path = sys.argv[2] if len(sys.argv) > 2 else "suite/test_suite.jsonl"
    
    print(f"Evaluating model: {model} using suite: {suite_path}")
    harness = OllamaHarness(model)
    
    if not os.path.exists(suite_path):
        print(f"Error: Suite file {suite_path} not found.")
        sys.exit(1)
        
    with open(suite_path, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f]

    results = []
    for case in cases:
        print(f"Running case {case['case_id']}...", end=" ", flush=True)
        out = harness.run_case(case)
        if "error" in out: print(f"Error in case {case['case_id']}: {out['error']}")
        score_res = ScoringEngine.score(out.get("tool_calls", []), case['expected_tool'], case['expected_arguments'])
        print(f"Result: {score_res['status']}")
        
        results.append({
            **case,
            "model": model,
            "actual_tool_calls": out.get("tool_calls", []),
            "score": score_res['status'],
            "metric": score_res['metric'],
            "raw_response": out.get("raw")
        })

    output_path = f"results/results_{model.replace(':', '_')}.jsonl"
    os.makedirs("results", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for res in results:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
