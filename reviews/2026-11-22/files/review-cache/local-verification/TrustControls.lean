import Init

namespace TrustControls

-- Intentional negative controls, isolated from every audited repository.
axiom missingFact : False
theorem extraAxiom : (0 : Nat) = 1 := False.elim missingFact
#print axioms extraAxiom

theorem incomplete : (0 : Nat) = 1 := by sorry
#print axioms incomplete

theorem conditional (h : False) : (0 : Nat) = 1 := False.elim h
#print conditional
#print axioms conditional

namespace Shadowed
def RiemannHypothesis : Prop := True
theorem fakeRH : RiemannHypothesis := True.intro
#print RiemannHypothesis
#print axioms fakeRH
end Shadowed

def ExpectedGoal : Prop := (0 : Nat) = 1
theorem rejectFalseConclusion : ¬ExpectedGoal := Nat.zero_ne_add_one 0

end TrustControls
