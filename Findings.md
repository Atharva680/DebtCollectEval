# Findings: Cross-Linguistic Tool-Call Reliability in Debt-Collection Voice Agents

## 1. Research Question
**How does the tool-calling reliability of LLMs vary between English and Indic languages (Hinglish and Marathi) in the context of debt-collection voice agents?**

Specifically, this research seeks to quantify the "accuracy delta" to ensure that critical business outcomes—such as capturing a Promise to Pay (PTP) or marking a dispute—are executed reliably regardless of the borrower's language or code-switching behavior.

## 2. Methodology
To ensure methodological rigor and eliminate "prompt-tuning" bias, the following experimental design was implemented:

- **Immutable Schemas**: Tool definitions were frozen in `schemas/tools.json` to ensure a consistent interface across all tests.
- **Baseline Prompting**: A single, fixed system prompt was utilized for all models to measure raw capabilities rather than the effects of iterative prompt engineering.
- **Synthetic Realism**: A test suite of 200+ cases was constructed to simulate real-world borrower behavior, including:
  - **Code-switching**: Mixed language use (e.g., Hinglish).
  - **Relative Dates**: Terms like *"kal"* (tomorrow) or *"parso"* (day after tomorrow).
  - **Hesitant Speech**: Non-linear utterances and conversational fillers.
- **Automated Scoring**: A programmatic engine compared emitted tool names and arguments against ground truth using a predefined error taxonomy.
- **Determinism**: All tests were run with `temperature: 0.0` to ensure reproducibility.

## 3. Experimental Setup
- **Model**: Qwen 2.5 (evaluated across various sizes, primarily 7B).
- **Runtime**: Ollama (Local execution for data privacy and latency control).
- **Dataset**: A synthetic corpus of 200+ utterances distributed across English, Hinglish, and Marathi-English.
- **Tech Stack**: Python 3.10+, AdminLTE 3 (Dashboard), and Chart.js for visualization.

## 4. Metrics Defined
The performance was measured using six primary metrics:
1. **Correct-tool rate**: $\frac{\text{Cases with correct tool name}}{\text{Total expected tool calls}}$
2. **Malformed-argument rate**: $\frac{\text{Correct tool but missing/wrong-typed/enum-violating args}}{\text{Correct-tool cases}}$
3. **Argument-level accuracy**: $\frac{\text{Correct tool AND all arg values match (within tolerance)}}{\text{Total expected tool calls}}$
4. **Spurious-call rate**: $\frac{\text{Tool emitted when none was expected}}{\text{Total cases}}$
5. **Missed-call rate**: $\frac{\text{No tool emitted when one was expected}}{\text{Total cases}}$
6. **Ambiguous-case handling**: Success rate for utterances where intent is genuinely unclear (measured as variance).

## 5. Results

| Language/Locale | Total Cases | Accuracy | Missed Calls | Spurious Calls | Malformed Args | Wrong Tool |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **English (en)** | 72 | **79.17%** | 0 | 15 | 0 | 0 |
| **Hinglish (hi-en)** | 78 | **100.00%** | 0 | 0 | 0 | 0 |
| **Marathi-English (mr-en)** | 60 | **100.00%** | 0 | 0 | 0 | 0 |

## 6. Key Findings
- **Indic Superiority**: In this specific test suite, the model demonstrated perfect (100%) accuracy for both Hinglish and Marathi-English utterances.
- **English Performance Dip**: English utterances performed significantly worse than the Indic counterparts, with an accuracy of 79.17%.
- **Primary Failure Mode**: The drop in English accuracy was driven entirely by **spurious calls** (15 instances), where the model triggered a tool despite no business intent being present in the utterance.
- **Argument Stability**: Once the correct tool was identified, there were zero malformed arguments across all three language groups, indicating strong schema adherence.

## 7. Unexpected / Non-Obvious Insights
- **Inverse Gap**: The initial hypothesis was that a performance gap would exist *against* Indic languages. However, the results show an "inverse gap" where the model is more disciplined in mixed-language contexts than in pure English.
- **Intent Over-Triggering**: The model appears "over-eager" in English, potentially interpreting polite fillers or general conversation as triggers for business tools, whereas it is more precise when processing Indic-English code-switching.

## 8. Uncertainties
- **Data Distribution**: It remains uncertain if the English test cases were inherently more ambiguous or "harder" than the Indic cases.
- **Model Generalization**: These results are specific to the Qwen 2.5 family; it is unclear if other multilingual models (e.g., Llama 3) exhibit the same inverse gap.
- **Prompt Sensitivity**: Since a baseline prompt was used, the actual "ceiling" of English performance is unknown—it is possible that minor prompt adjustments could eliminate the spurious calls.

## 9. Limitations
- **Quantization**: Evaluations were performed on Q4 quantized models. Production-grade findings would require FP16 precision to rule out quantization-induced noise.
- **Synthetic Nature**: While designed for realism, synthetic data cannot capture 100% of the acoustic noise, STT errors, and overlapping speech found in real-world telephony.
- **Baseline Scope**: Results are tied to a single system prompt and a specific set of tool schemas.

## 10. Conclusion
The evaluation demonstrates that Qwen 2.5 is exceptionally robust in handling tool-calls for Hinglish and Marathi-English in debt-collection scenarios. Surprisingly, the model's primary reliability risk is not linguistic complexity, but rather **over-triggering (spurious calls) in pure English contexts**. Future iterations should focus on refining the "Negative Intent" detection for English utterances to bring its reliability in line with the Indic results.
