import sys

from importlib import reload

sys.path.append("../")

import inferring.Inferring

reload(inferring.Inferring)
from inferring.Inferring import Inferring


class InferringDFA(Inferring):
    def __init__(self, target, oracle=None, debug=False):
        super().__init__(target=target, oracle=oracle, debug=debug)

    def initialization(self):
        self._extend_E(self.input_signs + [""])
        for e in self.E:
            self.T[("", e)] = self._query_type1("", e)
        self._extend_S("")

    def _query_type1(self, s, e):
        w = s + e
        if w not in self.queries:
            self.cnt[0] += 1
            self.queries[w] = self.target.route(w)[1]
        return self.queries[w]

    def create_conjecture(self):
        pass
