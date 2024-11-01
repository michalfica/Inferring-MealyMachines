from InferringDFA import InferringDFA
from utils.DFA import DFA
from utils.convDFA import convDFA
from utils.oracles.oracle1Conv import Oracle1Conv
import copy

"""
    Osobna klasa na czenie się splotu 2 DFA.
    bo hipoteza jest convDFA a nie DFA 
"""


class InferringconvDFA(InferringDFA):
    def __init__(self, target, oracle=None, debug=False, check_consistency=False):
        if oracle is not None:
            oracle = Oracle1Conv(target.input_signs)

        super().__init__(
            target=target,
            oracle=oracle,
            debug=debug,
            check_consistency=check_consistency,
        )

    def _create_conjecture(self):
        def _equivalent_in_S(s):
            for i, t in enumerate(self.S):
                if self._E_realtion(s, t):
                    return i

        conjecture = convDFA(
            type="dfa", Q=len(self.S), input_signs=self.input_signs, F=set()
        )
        for i, s in enumerate(self.S):
            conjecture.mapping[i] = s
            for a in self.input_signs:
                conjecture.δ[(i, a)] = _equivalent_in_S(s + a)
            if self.T[(s, "")] == DFA.ACCEPT:
                conjecture.F.add(i)
        return copy.deepcopy(conjecture)
