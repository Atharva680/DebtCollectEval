# Metric Definitions - Frozen

## 1. Correct-tool rate
Cases where the emitted tool name matches the expected tool name, over all cases where a tool call was expected.

## 2. Malformed-argument rate
Cases with the correct tool but at least one required argument missing, wrong-typed, or outside its enum, over cases scored correct-tool.

## 3. Argument-level accuracy
Cases with correct tool AND all argument values matching expected values within tolerance (exact match for date/amount), over all cases where a tool call was expected.

## 4. Spurious-call rate
Cases where no tool call was expected but one was emitted.

## 5. Missed-call rate
Cases where a tool call was expected but none was emitted.

## 6. Ambiguous-case handling
Reported as a separate variance metric. A case is 'pass' if the output is within the acceptable-response set defined in the test case.
