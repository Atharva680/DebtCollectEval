import pytest
from src.evaluator import ScoringEngine

def test_no_call_correct():
    # Case: No tool expected, none emitted
    result = ScoringEngine.score([], None, {})
    assert result["status"] == "PASS"
    assert result["metric"] == "no_call_correct"

def test_spurious_call():
    # Case: No tool expected, but one emitted
    result = ScoringEngine.score([{"name": "test_tool"}], None, {})
    assert result["status"] == "FAIL"
    assert result["metric"] == "spurious_call"

def test_missed_call():
    # Case: Tool expected, none emitted
    result = ScoringEngine.score([], "expected_tool", {"arg1": "val1"})
    assert result["status"] == "FAIL"
    assert result["metric"] == "missed_call"

def test_wrong_tool():
    # Case: Wrong tool emitted
    result = ScoringEngine.score([{"name": "wrong_tool"}], "expected_tool", {"arg1": "val1"})
    assert result["status"] == "FAIL"
    assert result["metric"] == "wrong_tool"

def test_argument_level_accurate():
    # Case: Correct tool and correct args
    result = ScoringEngine.score([{"name": "expected_tool", "arguments": {"arg1": "val1"}}], "expected_tool", {"arg1": "val1"})
    assert result["status"] == "PASS"
    assert result["metric"] == "argument_level_accurate"

def test_malformed_argument():
    # Case: Correct tool, missing arg
    result = ScoringEngine.score([{"name": "expected_tool", "arguments": {}}], "expected_tool", {"arg1": "val1"})
    assert result["status"] == "FAIL"
    assert result["metric"] == "malformed_argument"
