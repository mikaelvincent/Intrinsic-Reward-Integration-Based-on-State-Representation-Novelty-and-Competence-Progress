# TASK OVERVIEW

Your task is to systematically verify each piece of information (facts, findings, formulas, data, etc.) from the **notes** against the **paper**. Produce two main outputs:

1. **Verification List**: For each piece of information in the notes:
   - State whether it is **correct** (i.e., matches the paper) or **incorrect** (i.e., contradicts or misrepresents the paper).
   - Provide a brief snippet from both the paper and the notes that shows how you confirmed or found an error. (You may truncate long snippets for brevity but preserve enough text to validate correctness or locate the relevant sections.)
   - If the information is correct, highlight the relevant phrase or text from the paper that supports it.
   - If the information is incorrect, indicate exactly how and why it diverges from the original paper.

2. **Erroneous Information Summary**: A concise list of any notes content that is **incorrect**, along with clear guidance on what needs correcting. If everything in the notes is correct, say so explicitly.

---

## INSTRUCTIONS

**Step 1: Read and Parse the Files**
1. Load `paper.pdf` in a way that you can reference relevant text or sections.  
2. Load `notes.md`, read it line by line, or bullet by bullet—each bullet or line is considered an "information snippet" from the notes that needs verification.

**Step 2: Compare the Notes Against the Paper**
For each snippet in `notes.md`, do the following:
1. **Locate** the relevant section/page/paragraph in `paper.pdf` where the snippet might be verified.
2. **Check for Accuracy**:
   - If it accurately reflects the paper, mark it **Correct** and provide the direct snippet or quote from `paper.pdf` that supports it.
   - If it misquotes, omits crucial detail, or contradicts the original content, mark it **Incorrect** and clarify the discrepancy. Provide relevant snippets from both the notes and the paper, explaining how they differ.

**Step 3: Produce the Outputs**

- Verification List
  - Present a bullet or enumerated list. For each piece of information from the notes:
    1. The snippet from the notes (truncated if needed but retaining key phrases).
    2. Label it as **Correct** or **Incorrect**.
    3. Include a short quote from the PDF that justifies your verdict (or clarifies the error).
- Erroneous Information Summary
  - After the verification list, provide a short summary enumerating all incorrect snippets, with each snippet’s corrected or more accurate version. If no errors exist, state that explicitly.

---

## EXAMPLE OUTPUT (FICTITIOUS ILLUSTRATION)

Below is a short example to illustrate the desired format:

```
1. **Notes Snippet**: "The method uses a convolutional architecture with 3 layers."
   - Verdict: **Correct**
   - PDF Snippet: "Section 3.1: Our approach employs a 3-layer CNN for feature extraction..."

2. **Notes Snippet**: "They tested on CIFAR-10 and achieved 95% accuracy."
   - Verdict: **Incorrect**
   - Explanation: The paper states 90.5% accuracy, not 95%.
   - PDF Snippet: "In Table 2, we report a 90.5% accuracy on the CIFAR-10 test set..."

...

**Erroneous Information Summary**:
- For snippet #2: The correct accuracy is 90.5%, not 95%.
```

---

## FINAL REMINDERS

1. **Do Not Summarize the Entire Paper**: Focus only on verifying the notes against the paper.
2. **Be Strictly Evidence-Based**: Provide short supporting or conflicting quotes from the paper.
3. **Give Enough Context**: Each snippet’s reference from both the paper and the notes should be sufficient to confirm the claim’s correctness or error.
