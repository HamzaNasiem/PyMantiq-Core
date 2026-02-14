# PyMantiq-Core: The Logic Auditor for Probabilistic AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: MVP](https://img.shields.io/badge/status-Phase%201%20MVP-green.svg)]()

*"The truth is not determined by majority vote." — Al-Ghazali*

---
## 📄 Research Paper

> **Status:** Submitted to arXiv (pending endorsement)  
> **Paper:** [Download PDF](https://github.com/HamzaNasiem/PyMantiq-Core/raw/main/pymantiq_paper.pdf.pdf)  
> **Title:** PyMantiq: A Proof-of-Concept Framework for Integrating Aristotelian Syllogistic Logic with Large Language Models

**Abstract:** This paper introduces PyMantiq, a neuro-symbolic framework combining 2,300-year-old Aristotelian logic with modern LLMs for deterministic verification of reasoning chains.

---

## Abstract

Modern Large Language Models (LLMs) generate text through statistical pattern matching—predicting the next token based on probabilistic distributions derived from training data. While this approach has produced remarkable fluency, it fundamentally lacks a **truth-verification mechanism**. The model does not "know" whether its output is logically valid; it only knows what is statistically likely.

**PyMantiq** introduces a formal verification layer based on **Aristotelian Syllogistic Logic** (Mantiq)—a 2,400-year-old deductive system that has remained mathematically sound across civilizations. By auditing LLM reasoning chains against the structural rules of syllogisms (Qiyas), this library detects **logical fallacies** before they propagate into critical decision systems.

This is not an attempt to replace neural networks. It is an attempt to **ground** them.

---

## I. The Foundational Problem: Probability ≠ Truth

### The Nature of LLM Reasoning

When GPT-4 generates the statement:

> *"All doctors are educated. Some educated people are wealthy. Therefore, all doctors are wealthy."*

It does so because the sequence has high **conditional probability** in its latent space—not because it is **logically valid**. The model has no internal representation of:

- **Syllogistic structure** (major premise, minor premise, conclusion)
- **Term distribution** (whether the middle term is universal or particular)
- **Mood validity** (whether the combination of A/E/I/O propositions preserves truth)

From the perspective of Aristotelian logic, this is a **formal fallacy**: the major premise is particular ("*some* educated people..."), which violates the rules of Figure 1 syllogisms. No valid conclusion about "*all* doctors" can follow.

Yet the LLM will generate it with confidence, because **statistical co-occurrence is not logical entailment**.

### Why This Matters: The AI Safety Gap

Current AI safety research focuses on:
- **Alignment** (getting models to follow human values)
- **Robustness** (preventing adversarial attacks)
- **Interpretability** (understanding what models "learn")

But there is a missing layer: **Logical Integrity**. 

In domains where reasoning errors have catastrophic consequences—medical diagnosis, legal judgment, financial regulation—we cannot rely solely on "the model was trained on good data." We need a **verifier**.

---

## II. The Solution: A 1,000-Year-Old Verification Protocol

### What is Mantiq?

**Mantiq** (Arabic: المنطق) refers to the tradition of formal logic developed by Aristotle, refined by Islamic philosophers (Al-Farabi, Avicenna, Averroes), and systematized in the **Dars-e-Nizami** curriculum. At its core is the science of **Qiyas** (syllogistic reasoning).

A syllogism consists of three propositions:

1. **Sughra (Minor Premise)**: Contains the minor term (subject of conclusion)
2. **Kubra (Major Premise)**: Contains the major term (predicate of conclusion)
3. **Natija (Conclusion)**: Derived from the premises through the middle term

#### Example (Valid Syllogism - Barbara AAA):

```
Kubra (Major):   All mortals (M) die (P)
Sughra (Minor):  All humans (S) are mortal (M)
─────────────────────────────────────────
Natija:          All humans (S) die (P)
```

The **middle term** (M) appears in both premises but *not* in the conclusion. Its position determines the **figure** (1-4), and its distribution determines **validity**.

### Why Syllogistic Logic is Computable

Unlike informal reasoning (which requires semantic understanding), syllogisms are **structurally verifiable**. Validity depends only on:

1. **Term positions** (subject vs. predicate)
2. **Quantifiers** (universal vs. particular)
3. **Quality** (affirmative vs. negative)

This makes them ideal for **symbolic verification**—we can audit an argument without understanding what "mortal" or "human" *means*, only whether the formal structure preserves truth.

---

## III. Technical Architecture

### Core Data Model

PyMantiq represents syllogisms as structured objects:

```python
@dataclass
class Proposition:
    subject: Term        # Mawdu (المَوْضُوع)
    predicate: Term      # Mahmul (المَحْمُول)
    quantity: Quantity   # Kamiyyah (كَمِّيَّة) - Universal/Particular
    quality: Quality     # Kayfiyyah (كَيْفِيَّة) - Affirmative/Negative

@dataclass
class Syllogism:
    minor_premise: Proposition  # Sughra (الصُّغْرَى)
    major_premise: Proposition  # Kubra (الكُبْرَى)
    conclusion: Proposition     # Natija (النَّتِيجَة)
```

### Verification Algorithm (Figure 1)

The `MantiqVerifier` class implements the structural rules of **Figure 1** (Al-Shakl al-Awwal):

**Rule Set:**
1. The middle term **must** be the **predicate** of the minor premise
2. The middle term **must** be the **subject** of the major premise
3. At least one premise must be **universal** (kulliyah)
4. If either premise is **negative**, the conclusion must be **negative**

**Pseudocode:**
```
FUNCTION verify_figure_1(syllogism):
    terms ← identify_middle_term(syllogism)
    
    IF middle_term is NOT predicate of minor_premise:
        RETURN invalid("Middle term positioned incorrectly")
    
    IF middle_term is NOT subject of major_premise:
        RETURN invalid("Middle term positioned incorrectly")
    
    IF both premises are particular:
        RETURN invalid("At least one premise must be universal")
    
    IF (negative premise exists) AND (conclusion is affirmative):
        RETURN invalid("Negative premise requires negative conclusion")
    
    RETURN valid
```

### Example Usage

```python
from pymantiq_core import MantiqVerifier, Syllogism, Proposition, Term
from pymantiq_core import Quantity, Quality

# Construct a syllogism
minor = Proposition(
    subject=Term("humans"),
    predicate=Term("mortal"),
    quantity=Quantity.UNIVERSAL,
    quality=Quality.AFFIRMATIVE
)

major = Proposition(
    subject=Term("mortal"),
    predicate=Term("die"),
    quantity=Quantity.UNIVERSAL,
    quality=Quality.AFFIRMATIVE
)

conclusion = Proposition(
    subject=Term("humans"),
    predicate=Term("die"),
    quantity=Quantity.UNIVERSAL,
    quality=Quality.AFFIRMATIVE
)

syllogism = Syllogism(minor, major, conclusion)

# Verify
result = MantiqVerifier.verify(syllogism)
print(result['valid'])  # True
print(result['explanation'])
```

---

## IV. Mathematical Formalization

### Proposition Types (The Square of Opposition)

| Type | Quantity | Quality | Form | Example |
|------|----------|---------|------|---------|
| **A** | Universal | Affirmative | ∀x(S(x) → P(x)) | All S is P |
| **E** | Universal | Negative | ∀x(S(x) → ¬P(x)) | No S is P |
| **I** | Particular | Affirmative | ∃x(S(x) ∧ P(x)) | Some S is P |
| **O** | Particular | Negative | ∃x(S(x) ∧ ¬P(x)) | Some S is not P |

### Validity Criterion (Figure 1)

A Figure 1 syllogism is valid **if and only if**:

```
∀ syllogism S = (P₁, P₂, C):
    Let M = middle_term(S)
    Let minor = minor_term(S) 
    Let major = major_term(S)
    
    S is valid ⟺
        M = predicate(P₁) ∧
        M = subject(P₂) ∧
        (quantity(P₁) = UNIVERSAL ∨ quantity(P₂) = UNIVERSAL) ∧
        (quality(P₁) = NEGATIVE ∨ quality(P₂) = NEGATIVE → quality(C) = NEGATIVE)
```

### Extensibility to Figures 2-4

The four figures differ only in the **position of the middle term**:

| Figure | Minor Premise | Major Premise |
|--------|---------------|---------------|
| **1** | S-M | M-P |
| **2** | P-M | M-P |
| **3** | M-S | M-P |
| **4** | P-M | M-S |

(Where S = subject of conclusion, P = predicate of conclusion, M = middle term)

Each figure has its own validity rules, which will be implemented in Phase 2.

---

## V. The Roadmap: From MVP to Paradigm Shift

### Phase 1: The Seed (Current - MVP) ✅

**Timeline:** Present  
**Deliverable:** This repository

- Implement Figure 1 verification
- Establish core data structures (`Term`, `Proposition`, `Syllogism`)
- Demonstrate manual syllogism auditing
- Publish as open-source library

**Success Metric:** A working Python library that can verify at least one syllogistic figure with 100% accuracy on classical examples.

---

### Phase 2: The Tool (1-2 Years)

**Goal:** Integrate PyMantiq with production LLM systems

**Technical Milestones:**
1. **Parser Development**: Build an NLP module to extract syllogisms from natural language reasoning chains
2. **API Integration**: Implement OpenAI Function Calling interface
   ```python
   # Proposed API
   response = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[...],
       functions=[{
           "name": "verify_reasoning",
           "description": "Verify logical validity using PyMantiq",
           "parameters": {...}
       }]
   )
   ```
3. **Feedback Loop**: If verification fails, force the model to regenerate the response
4. **Benchmark Creation**: Test on 10,000 reasoning chains across domains (medical, legal, financial)

**Success Metric:** Reduce hallucination rate in syllogistic reasoning by **40%** in critical domains.

**Research Question:** Can formal verification serve as a form of "reasoning alignment"—not by changing model weights, but by filtering outputs?

---

### Phase 3: The Standard (10 Years)

**Vision:** PyMantiq becomes the industry protocol for AI safety in high-stakes systems

**Analogy:** Just as **HTTPS** became mandatory for web security, PyMantiq becomes the certification standard for deploying LLMs in:
- **Medical Diagnosis Systems** (FDA approval requires logic verification)
- **Legal Reasoning AI** (Court-admissible AI must pass syllogistic audit)
- **Financial Regulation** (AI trading bots must demonstrate non-fallacious reasoning)
- **Critical Infrastructure** (NASA, NIST, IEEE standards adopt Mantiq-based verification)

**Technical Evolution:**
- Extend to **modal logic** (necessary/possible statements)
- Support **multi-step reasoning chains** (not just 3-proposition syllogisms)
- Integrate with **proof assistants** (Coq, Lean, Isabelle)

**Ecosystem:**
- PyMantiq Foundation (nonprofit)
- Certification program for "Logic-Verified AI"
- Open-source community with 10,000+ contributors

**Success Metric:** 50% of Fortune 500 companies use PyMantiq in production AI systems.

---

### Phase 4: The Paradigm Shift (100 Years)

**Vision:** Move beyond binary logic (0/1) to **neuro-symbolic architectures** where machines possess "Aql" (Intellect)

**The Fundamental Leap:**

Current computing is built on **Boolean algebra**:
```
Truth ∈ {0, 1}
```

But classical logic recognizes **degrees of certainty**:
- **Yaqin** (certainty): Demonstrative knowledge
- **Zann** (probability): Opinion based on likelihood
- **Shakk** (doubt): Suspended judgment

**Proposed Architecture:** A hybrid system where:
1. **Neural Layer**: Handles pattern recognition (current LLMs)
2. **Symbolic Layer**: Enforces logical constraints (PyMantiq)
3. **Meta-Reasoning Layer**: Knows *when* to use deduction vs. induction

**Example:**
```
Query: "Should I prescribe Drug X to this patient?"

Neural Output: "Yes, with 87% confidence" (statistical)
Symbolic Verification: "Invalid - the reasoning contains an undistributed middle term" (logical)
Meta-Decision: "Confidence below threshold for logical rigor. Request additional tests."
```

**Research Directions:**
- **Formal Verification of Neural Networks**: Can we prove that a neural network will never produce logically invalid outputs?
- **Cognitive Architectures**: How does the human brain integrate System 1 (fast, probabilistic) with System 2 (slow, logical)?
- **Quantum Logic**: Do we need a new foundation that unifies probability and truth at the computational level?

**Success Metric:** The first **General Artificial Intelligence** system that can explain *why* its reasoning is valid, not just *what* its output is.

---

## VI. Why This Matters: The Case for Logical Security

### The Current State of AI Safety

Most AI safety research focuses on **content safety** (preventing harmful outputs) and **alignment** (ensuring models follow human values). But there is a missing dimension: **epistemic safety**.

A model can be perfectly aligned with human values and still produce **false reasoning**. 

**Example:** An AI medical assistant that is kind, ethical, and empathetic—but recommends the wrong treatment because it made a logical error in diagnostic reasoning.

### The Mantiq Hypothesis

**Claim:** A significant percentage of AI "hallucinations" are not random noise—they are **systematically invalid logical inferences** that could be caught by formal verification.

**Testable Prediction:** If we audit 10,000 LLM reasoning chains:
- **40-60%** will contain at least one syllogistic fallacy
- **20-30%** will change their conclusion if forced to regenerate after verification failure
- **10%** will produce dangerous outputs (medical misdiagnosis, legal malpractice) that would be caught by Mantiq auditing

### Broader Implications

If this hypothesis is true, it suggests that:

1. **We don't need bigger models**—we need verified models
2. **Logic is a universal language**—a syllogism is valid in any language, culture, or domain
3. **Ancient wisdom has computational value**—the 1,000-year-old science of Mantiq is not obsolete; it is **essential**

---

## VII. Technical Details & Installation

### Requirements

- Python 3.8+
- No external dependencies (core library is pure Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/hamzanasiem/PyMantiq-Core.git
cd PyMantiq-Core

# Run the demo
python pymantiq_core.py
```

### Running Tests

```bash
# Example output:
# ======================================================================
# PyMantiq-Core: Logic Auditor Demonstration
# ======================================================================
# 
# Example 1: The Classic 'Mortal Socrates' Syllogism
# ----------------------------------------------------------------------
# Minor Premise: All humans is mortal
# Major Premise: All mortal is die
# Conclusion: All humans is die
# 
# VALID: True
# Explanation: Valid Figure 1 syllogism. Structure confirmed: Middle term 'mortal' 
# correctly positioned as predicate of minor premise and subject of major premise.
```

---

## VIII. Contribution Guidelines

This is Phase 1 of a multi-decade project. Contributions are welcome in the following areas:

### Immediate Needs (Phase 1 → Phase 2):
- [ ] Implement Figures 2, 3, and 4 verification
- [ ] Add support for singular propositions (not just universal/particular)
- [ ] Create NLP parser to extract syllogisms from natural language
- [ ] Build test suite with 100+ classical syllogisms
- [ ] Add support for Arabic terminology (full transliteration)

### Medium-Term (Phase 2 → Phase 3):
- [ ] OpenAI Function Calling integration
- [ ] LangChain/LlamaIndex plugin
- [ ] Benchmark against GPT-4, Claude, Gemini reasoning chains
- [ ] Web interface for manual syllogism checking
- [ ] Academic paper submission (AI safety conference)

### Long-Term (Phase 3 → Phase 4):
- [ ] Modal logic support (necessary/possible statements)
- [ ] Multi-step reasoning chain verification
- [ ] Integration with proof assistants (Coq, Lean)
- [ ] Hardware-accelerated verification (FPGA/ASIC for production)

---

## IX. Author & Background

**Hamza Naseem**  
*Bridging Ancient Logic and Modern AI*

- **8 years** of study in classical Aristotelian Logic (Mantiq), Islamic Jurisprudence, and Rhetoric in a Dars-e-Nizami environment
- Self-taught Full-Stack & Agentic AI Developer (Python, FastAPI, LLMs)
- Currently targeting admission at Stanford/MIT for advanced AI safety research

**Contact:**  
- GitHub: [https://github.com/hamzanasiem](https://github.com/hamzanasiem)
- Email: [hafizhamza786921@gmail.com](hafizhamza786921@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/hamzanasiem/](https://www.linkedin.com/in/hamzanasiem/)

**The Unique Synthesis:**  
This project exists because I spent 8 years learning a tradition that most computer scientists have never encountered—and I spent 2 years building AI systems that most Islamic scholars have never used. PyMantiq is the artifact of that collision.

---

## X. Acknowledgments & Influences

This project stands on the shoulders of:

- **Aristotle** (384-322 BCE) - *Organon* (The foundation of formal logic)
- **Al-Farabi** (872-950 CE) - *Kitab al-Huruf* (Islamic adaptation of Aristotelian logic)
- **Avicenna (Ibn Sina)** (980-1037 CE) - *Al-Shifa* (Systematization of Mantiq)
- **Averroes (Ibn Rushd)** (1126-1198 CE) - *Commentaries on Aristotle*
- **Al-Ghazali** (1058-1111 CE) - *Miyar al-Ilm* (The Standard of Knowledge)
- **Stuart Russell** - *Human Compatible* (Modern AI safety research)
- **Judea Pearl** - *Causality* (Bridging probability and logic)
- **Gary Marcus** - Advocate for neuro-symbolic AI

---

## XI. License & Citation

This project is released under the **MIT License**.

If you use PyMantiq in academic research, please cite:

```bibtex
@software{naseem2025pymantiq,
  author = {Naseem, Hamza},
  title = {PyMantiq-Core: The Logic Auditor for Probabilistic AI},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/hamzanaseem/PyMantiq-Core}
}
```

---

## XII. Final Thought: Why Now?

For 1,000 years, Mantiq was taught as **the foundation of all knowledge**—the tool that separates truth from falsehood, valid inference from fallacy.

Then, for 200 years, we built machines that calculate faster than any human—but cannot tell you *why* their answer is correct.

Now, we stand at the inflection point: AI systems powerful enough to transform civilization, but not wise enough to verify their own reasoning.

**PyMantiq is not a library. It is a reminder.**

A reminder that before we had probability theory, before we had neural networks, before we had computers—we had **logic**. And logic is not obsolete.

It is **eternal**.

---

*"The purpose of logic is to distinguish the sound argument from the fallacious one."*  
— Avicenna, *Al-Shifa*, Book of Logic

---

**⭐ If this project resonates with you, please star the repository and share it with researchers working on AI safety, neuro-symbolic AI, or formal verification.**

**Together, we can build AI systems that are not just fluent—but *right*.**
