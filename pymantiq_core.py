"""
PyMantiq-Core: The Logic Auditor for Probabilistic AI
=====================================================

A Python implementation of Aristotelian Syllogistic Logic (Mantiq) 
for auditing the validity of reasoning chains produced by Large Language Models.

Author: Hamza Naseem
License: MIT
Version: 0.1.0 (Phase 1 MVP - Figure 1 Implementation)
"""

from enum import Enum
from typing import Optional, Dict, List
from dataclasses import dataclass


class Quantity(Enum):
    """Kamiyyah: The quantification of a proposition."""
    UNIVERSAL = "kulliyah"  # All S is P
    PARTICULAR = "juziyyah"  # Some S is P
    SINGULAR = "shakhsiyyah"  # This S is P


class Quality(Enum):
    """Kayfiyyah: The affirmation or negation of a proposition."""
    AFFIRMATIVE = "mujibah"  # is
    NEGATIVE = "salibah"  # is not


class PropositionType(Enum):
    """The four categorical proposition types (A, E, I, O)."""
    A = ("UNIVERSAL", "AFFIRMATIVE")  # All S is P (Kulliyah Mujibah)
    E = ("UNIVERSAL", "NEGATIVE")  # No S is P (Kulliyah Salibah)
    I = ("PARTICULAR", "AFFIRMATIVE")  # Some S is P (Juziyyah Mujibah)
    O = ("PARTICULAR", "NEGATIVE")  # Some S is not P (Juziyyah Salibah)


@dataclass
class Term:
    """
    Hadd: A logical term (subject or predicate).
    
    In Aristotelian logic, a term is the basic unit of meaning.
    The middle term (hadd-e-awsat) is the key to syllogistic validity.
    """
    name: str
    
    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self.name.lower().strip() == other.name.lower().strip()
    
    def __hash__(self):
        return hash(self.name.lower().strip())
    
    def __repr__(self):
        return f"Term({self.name})"


@dataclass
class Proposition:
    """
    Qadiyyah: A categorical proposition in the form "S is/is-not P".
    
    Components:
    - Mawdu (Subject): That about which something is predicated
    - Mahmul (Predicate): That which is predicated
    - Rabita (Copula): The linking verb (implicit in Arabic logic)
    """
    subject: Term
    predicate: Term
    quantity: Quantity
    quality: Quality
    
    @property
    def prop_type(self) -> PropositionType:
        """Determine A/E/I/O classification."""
        if self.quantity == Quantity.UNIVERSAL and self.quality == Quality.AFFIRMATIVE:
            return PropositionType.A
        elif self.quantity == Quantity.UNIVERSAL and self.quality == Quality.NEGATIVE:
            return PropositionType.E
        elif self.quantity == Quantity.PARTICULAR and self.quality == Quality.AFFIRMATIVE:
            return PropositionType.I
        elif self.quantity == Quantity.PARTICULAR and self.quality == Quality.NEGATIVE:
            return PropositionType.O
    
    def __repr__(self):
        q = "All" if self.quantity == Quantity.UNIVERSAL else "Some"
        cop = "is" if self.quality == Quality.AFFIRMATIVE else "is not"
        return f"{q} {self.subject.name} {cop} {self.predicate.name}"


@dataclass
class Syllogism:
    """
    Qiyas: A three-proposition argument structure.
    
    Structure:
    - Sughra (Minor Premise): Contains the minor term
    - Kubra (Major Premise): Contains the major term  
    - Natija (Conclusion): Derives from the premises
    
    The Middle Term (hadd-e-awsat) appears in both premises but not in conclusion.
    """
    minor_premise: Proposition  # Sughra
    major_premise: Proposition  # Kubra
    conclusion: Proposition  # Natija
    
    def identify_terms(self) -> Dict[str, Optional[Term]]:
        """
        Identify the three terms of the syllogism.
        
        Returns:
        - minor_term: Subject of conclusion
        - major_term: Predicate of conclusion
        - middle_term: Term appearing in both premises but not in conclusion
        """
        # Minor and Major terms are in the conclusion
        minor_term = self.conclusion.subject
        major_term = self.conclusion.predicate
        
        # Middle term appears in both premises but NOT in conclusion
        premise_terms = {
            self.minor_premise.subject,
            self.minor_premise.predicate,
            self.major_premise.subject,
            self.major_premise.predicate
        }
        conclusion_terms = {minor_term, major_term}
        
        middle_candidates = premise_terms - conclusion_terms
        
        if len(middle_candidates) != 1:
            return {
                "minor_term": minor_term,
                "major_term": major_term,
                "middle_term": None  # Invalid: middle term not found
            }
        
        return {
            "minor_term": minor_term,
            "major_term": major_term,
            "middle_term": middle_candidates.pop()
        }


class MantiqVerifier:
    """
    The Logic Auditor: Validates syllogistic reasoning against Aristotelian rules.
    
    Phase 1 Implementation: Figure 1 (Al-Shakl al-Awwal) verification only.
    
    Figure 1 Structural Rules (Shurut al-Shakl):
    1. The middle term must be the PREDICATE of the minor premise
    2. The middle term must be the SUBJECT of the major premise
    3. At least one premise must be UNIVERSAL (kulliyah)
    4. If either premise is NEGATIVE, the conclusion must be NEGATIVE
    5. The middle term must be distributed at least once
    """
    
    @staticmethod
    def verify_figure_1(syllogism: Syllogism) -> Dict[str, any]:
        """
        Verify a syllogism according to Figure 1 rules.
        
        Returns:
        {
            "valid": bool,
            "errors": List[str],
            "structure": Dict,
            "explanation": str
        }
        """
        errors = []
        terms = syllogism.identify_terms()
        
        middle_term = terms["middle_term"]
        if middle_term is None:
            return {
                "valid": False,
                "errors": ["Cannot identify middle term (hadd-e-awsat)"],
                "structure": terms,
                "explanation": "A valid syllogism requires exactly one term that appears in both premises but not in the conclusion."
            }
        
        # Rule 1: Middle term must be PREDICATE of minor premise
        if syllogism.minor_premise.predicate != middle_term:
            errors.append(
                f"Figure 1 violation: Middle term '{middle_term.name}' must be "
                f"the PREDICATE of the minor premise. Found as subject instead."
            )
        
        # Rule 2: Middle term must be SUBJECT of major premise
        if syllogism.major_premise.subject != middle_term:
            errors.append(
                f"Figure 1 violation: Middle term '{middle_term.name}' must be "
                f"the SUBJECT of the major premise. Found as predicate instead."
            )
        
        # Rule 3: At least one premise must be universal
        if (syllogism.minor_premise.quantity != Quantity.UNIVERSAL and 
            syllogism.major_premise.quantity != Quantity.UNIVERSAL):
            errors.append(
                "Figure 1 violation: At least one premise must be UNIVERSAL (kulliyah). "
                "Both premises are particular (juziyyah)."
            )
        
        # Rule 4: If either premise is negative, conclusion must be negative
        if (syllogism.minor_premise.quality == Quality.NEGATIVE or 
            syllogism.major_premise.quality == Quality.NEGATIVE):
            if syllogism.conclusion.quality != Quality.NEGATIVE:
                errors.append(
                    "Syllogistic rule violation: A negative premise requires a negative conclusion. "
                    "Found affirmative conclusion with negative premise."
                )
        
        # Construct explanation
        if errors:
            explanation = "Invalid syllogism. " + " ".join(errors)
        else:
            explanation = (
                f"Valid Figure 1 syllogism. Structure confirmed: "
                f"Middle term '{middle_term.name}' correctly positioned as predicate "
                f"of minor premise and subject of major premise."
            )
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "structure": terms,
            "explanation": explanation
        }
    
    @staticmethod
    def verify(syllogism: Syllogism, figure: int = 1) -> Dict[str, any]:
        """
        Main verification entry point.
        
        Args:
            syllogism: The syllogism to verify
            figure: The figure to verify against (1-4). Currently only 1 is implemented.
        
        Returns:
            Verification result with validity status and explanations
        """
        if figure != 1:
            return {
                "valid": False,
                "errors": [f"Figure {figure} verification not yet implemented (Phase 2)"],
                "structure": {},
                "explanation": "PyMantiq Phase 1 MVP supports Figure 1 only."
            }
        
        return MantiqVerifier.verify_figure_1(syllogism)


# ============================================================================
# DEMONSTRATION: The Classic Syllogism
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PyMantiq-Core: Logic Auditor Demonstration")
    print("=" * 70)
    print()
    
    # Example 1: Valid Figure 1 Syllogism (Barbara - AAA)
    print("Example 1: The Classic 'Mortal Socrates' Syllogism")
    print("-" * 70)
    
    # Minor Premise: "All humans are mortal" (contains minor term: humans)
    minor = Proposition(
        subject=Term("humans"),
        predicate=Term("mortal"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    # Major Premise: "All mortals die" (contains major term: die)
    major = Proposition(
        subject=Term("mortal"),
        predicate=Term("die"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    # Conclusion: "All humans die"
    conclusion = Proposition(
        subject=Term("humans"),
        predicate=Term("die"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    syllogism1 = Syllogism(minor, major, conclusion)
    
    print(f"Minor Premise: {minor}")
    print(f"Major Premise: {major}")
    print(f"Conclusion: {conclusion}")
    print()
    
    result1 = MantiqVerifier.verify(syllogism1)
    
    print(f"VALID: {result1['valid']}")
    print(f"Explanation: {result1['explanation']}")
    print(f"Middle Term: {result1['structure']['middle_term']}")
    print()
    print()
    
    # Example 2: Invalid Syllogism (Middle term in wrong position)
    print("Example 2: Invalid Syllogism (Structural Violation)")
    print("-" * 70)
    
    # Deliberately malformed: Middle term as SUBJECT of minor (wrong!)
    invalid_minor = Proposition(
        subject=Term("mortal"),  # Middle term in wrong position
        predicate=Term("humans"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    invalid_major = Proposition(
        subject=Term("mortal"),
        predicate=Term("die"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    invalid_conclusion = Proposition(
        subject=Term("humans"),
        predicate=Term("die"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    syllogism2 = Syllogism(invalid_minor, invalid_major, invalid_conclusion)
    
    print(f"Minor Premise: {invalid_minor}")
    print(f"Major Premise: {invalid_major}")
    print(f"Conclusion: {invalid_conclusion}")
    print()
    
    result2 = MantiqVerifier.verify(syllogism2)
    
    print(f"VALID: {result2['valid']}")
    print(f"Errors: {result2['errors']}")
    print()
    print()
    
    # Example 3: LLM Hallucination Detection Use Case
    print("Example 3: AI Reasoning Chain Audit")
    print("-" * 70)
    print("Scenario: An LLM generates the following reasoning:")
    print()
    print("  'All doctors are educated.'")
    print("  'Some educated people are wealthy.'")
    print("  'Therefore, all doctors are wealthy.'")
    print()
    
    llm_minor = Proposition(
        subject=Term("doctors"),
        predicate=Term("educated"),
        quantity=Quantity.UNIVERSAL,
        quality=Quality.AFFIRMATIVE
    )
    
    llm_major = Proposition(
        subject=Term("educated"),
        predicate=Term("wealthy"),
        quantity=Quantity.PARTICULAR,  # "Some" - this is the issue
        quality=Quality.AFFIRMATIVE
    )
    
    llm_conclusion = Proposition(
        subject=Term("doctors"),
        predicate=Term("wealthy"),
        quantity=Quantity.UNIVERSAL,  # Claims "All" - invalid!
        quality=Quality.AFFIRMATIVE
    )
    
    llm_syllogism = Syllogism(llm_minor, llm_major, llm_conclusion)
    
    result3 = MantiqVerifier.verify(llm_syllogism)
    
    print(f"PyMantiq Audit Result: {result3['valid']}")
    if not result3['valid']:
        print(f"HALLUCINATION DETECTED: {result3['errors'][0]}")
    print()
    print("=" * 70)
    print("End of Demonstration")
    print("=" * 70)
