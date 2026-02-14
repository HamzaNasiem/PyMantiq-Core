# Contributing to PyMantiq

Thank you for your interest in contributing to PyMantiq! This project bridges ancient Aristotelian logic with modern AI systems, and we welcome contributors from both philosophy and computer science backgrounds.

## Philosophy

PyMantiq is built on two core principles:

1. **Rigor**: Every implementation must be faithful to the classical rules of Mantiq
2. **Clarity**: Code should be readable by both AI researchers and logic scholars

## How to Contribute

### Phase 1 Priority Areas

- [ ] Implement Figures 2, 3, and 4 verification
- [ ] Add comprehensive test cases (classical syllogisms from Aristotle's *Prior Analytics*)
- [ ] Improve error messages with more detailed explanations
- [ ] Add Arabic language support (full transliteration)

### Phase 2 Roadmap Items

- [ ] Natural language parsing (extract syllogisms from text)
- [ ] Distribution tracking (implement illicit major/minor detection)
- [ ] OpenAI Function Calling integration
- [ ] LangChain plugin
- [ ] Benchmark suite (test against LLM outputs)

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/figure-2-implementation`)
3. Write tests first (TDD approach)
4. Implement your feature
5. Ensure all tests pass (`python test_suite.py`)
6. Submit a pull request

### Code Style

- Use type hints for all function signatures
- Follow PEP 8 naming conventions
- Include docstrings with Arabic terminology where appropriate
- Add inline comments explaining *why*, not *what*

### Testing

All contributions must include tests. For logic implementations:

1. **Valid test cases**: Prove your code accepts valid syllogisms
2. **Invalid test cases**: Prove your code rejects invalid syllogisms
3. **Edge cases**: Middle term detection failures, malformed inputs

Example test structure:

```python
def test_figure_2_valid():
    """Test valid Figure 2 syllogism (Cesare - EAE)"""
    # No animals are plants (E)
    # All trees are plants (A)
    # No trees are animals (E)
    ...
    assert result['valid'] == True
```

### Documentation

When adding new features:

- Update README.md with new capabilities
- Add examples to the demonstration section
- Explain the logical rule you're implementing (with references to classical texts)

### Questions?

- Open an issue on GitHub
- Tag with `question` label
- Maintainer will respond within 48 hours

## Research Contributions

If you're an academic working on neuro-symbolic AI, formal verification, or AI safety:

- We welcome citations and academic collaborations
- For research partnerships, contact: [Your Email]
- If you use PyMantiq in a paper, please cite the repository

## Code of Conduct

### Intellectual Honesty

- Admit when you don't know something
- Cite sources for logical rules (Aristotle, Al-Farabi, etc.)
- Don't claim credit for others' work

### Respect for Tradition

- This project honors a 1,000-year-old intellectual tradition
- Avoid dismissing classical terminology or methods
- If you disagree with a design decision, explain your reasoning respectfully

### Inclusivity

- We welcome contributors from all backgrounds
- Questions are never "stupid"—if you don't understand Mantiq, ask!
- If you don't understand Python, ask!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*"Logic is the art of thinking well. It is the foundation of all sciences."* — Al-Ghazali
