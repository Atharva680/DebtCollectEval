
import json
from typing import List, Dict, Any, Optional

class ScoringEngine:
    @staticmethod
    def score(actual_tool_calls: List[Dict], expected_tool: Optional[str], expected_args: Dict) -> Dict:
        # Case 1: No tool expected
        if expected_tool is None:
            if not actual_tool_calls:
                return {"status": "PASS", "metric": "no_call_correct"}
            else:
                return {"status": "FAIL", "metric": "spurious_call"}

        # Case 2: Tool expected but none emitted
        if not actual_tool_calls:
            return {"status": "FAIL", "metric": "missed_call"}

        # Case 3: Tool emitted - check the first one
        call = actual_tool_calls[0]
        # Ollama sometimes returns tool calls in different formats (function name vs name)
        actual_tool = call.get("function", {}).get("name") or call.get("name")
        actual_args = call.get("function", {}).get("arguments", {}) or call.get("arguments", {})

        if actual_tool != expected_tool:
            return {"status": "FAIL", "metric": "wrong_tool"}

        # Check arguments
        # We check if all expected keys are present. 
        # 'FULL' is a suite-level placeholder for 'the outstanding amount'
        missing_args = [k for k, v in expected_args.items() if k not in actual_args]
        if missing_args:
            return {"status": "FAIL", "metric": "malformed_argument"}

        # Value check
        for k, v in expected_args.items():
            actual_val = actual_args.get(k)
            if v == "FULL":
                continue # Skip strict check for placeholders
            if str(actual_val).lower() != str(v).lower():
                return {"status": "FAIL", "metric": "wrong_argument_value"}

        return {"status": "PASS", "metric": "argument_level_accurate"}
