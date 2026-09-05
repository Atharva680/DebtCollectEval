@echo off
echo [1/4] Installing dependencies...
pip install -r requirements.txt

echo [2/4] Running Evaluation (Qwen 2.5 0.5B)...
python scripts/run.py qwen2.5:0.5b configs/suite/test_suite.jsonl

echo [3/4] Exporting Raw Results...
python scripts/export_results.py results/results_qwen2.5_0.5b.jsonl

echo [4/4] Evaluating Metrics...
python scripts/evaluate.py results/results_qwen2.5_0.5b.jsonl

echo.
echo Reproduce complete. Check results/ directory.
pause
