import sys

from importlib import reload

sys.path.append("../")

import inferring.Inferring

reload(inferring.Inferring)
from inferring.Inferring import Inferring


class InferringDFA(Inferring):
    def __init__(self, target_mm, oracle=None, debug=False):
        super().__init__(target_mm=target_mm, oracle=oracle, debug=debug)

    def initialization(self):
        pass

    def _query_type1(self, w):
        pass

    def create_conjecture(self):
        pass
