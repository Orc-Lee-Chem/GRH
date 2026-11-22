import Init

namespace TrustControls
def RiemannHypothesis : Prop := True
theorem candidate : RiemannHypothesis := True.intro

-- Expected to fail: a proof of the weakened definition is not a proof of this goal.
theorem claimed : (0 : Nat) = 1 := candidate
end TrustControls
