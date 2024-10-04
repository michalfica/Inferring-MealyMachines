from importlib import reload

import sys

sys.path.append("../")
sys.path.append("../utils")

import utils.Mealymachine
import utils.DFA

reload(utils.Mealymachine)
reload(utils.DFA)
from utils.Mealymachine import MealyMachine
from utils.DFA import DFA

import copy


class Inferring:
    NO_ANSWER = ""

    def __init__(self, target_mm, oracle=None, debug=False):
        self.target_mm = target_mm
        self.oracle = oracle  # DFA or Mealy machine (for now)
        self.input_signs = self.target_mm.input_signs
        self.output_signs = self.target_mm.output_signs
        self.S = set()
        self.E = set()
        self.T = dict()
        self.cnt = [0, 0]
        self.counterexamples = []
        self.debug = debug

        self.queries = dict()

    def _initialization(self):
        pass

    def run(self, counterexamples=False):
        self._initialization()

        while True:
            if self.debug:
                print(f"S = {sorted(self.S)}, rozmiar E = {sorted(self.E)}")
            check, x = self._closed()
            while check == False:
                self._extend_S(x)
                check, x = self._closed()

            if self.debug:
                print(
                    f"zamkniętość sprawdzona - S = {sorted(self.S)}, rozmiar E = {sorted(self.E)}"
                )

            conjecture = self._create_conjecture()

            if self.debug:
                print(f"hipoteza: ")
                conjecture.print_transitions()

            check, x = self._query_type2(conjecture)

            if check == False:
                if self.debug:
                    print(f"kontrprzyklad = {x}")
                self.counterexamples.append(x)
                self._process_counterexample(x)
            else:
                if counterexamples:
                    return (
                        conjecture,
                        self.cnt,
                        [len(x) for x in self.counterexamples],
                    )
                else:
                    return (conjecture, self.cnt)

    def _ask_oracle(self, w):
        return self.oracle.route(w)[1]

    def _E_realtion(self, s, t):
        for e in self.E:
            if self.T[(s, e)] != self.T[(t, e)]:
                return False
        return True

    def _query_type1(self, w):
        pass

    def _query_type2(self, conjecture):
        self.cnt[1] += 1
        return self.target_mm.equiv(conjecture)

    def _closed(self):
        wlist = []
        for s in self.S:
            for a in self.input_signs:
                if s + a not in self.S:
                    wlist.append(s + a)
        wlist = sorted(wlist, key=len)

        for w in wlist:
            check = False
            for t in self.S:
                if self._E_realtion(w, t):
                    check = True
                    break
            if not check:
                return (False, w)
        return (True, "")

    def _extend_S(self, s):
        self.S.add(s)
        for a in self.input_signs:
            for e in self.E:
                self.T[(s + a, e)] = self._query_type1(s + a + e)[-len(e) :]

    def _extend_E(self, elist):
        for s in self.S:

            for e in elist:
                if e not in self.E:
                    self.T[(s, e)] = self._query_type1(s + e)[-len(e) :]

            for a in self.input_signs:
                for e in elist:
                    if e not in self.E and s + a not in self.S:
                        self.T[(s + a, e)] = self._query_type1(s + a + e)[-len(e) :]
        self.E.update(elist)

    def _create_conjecture(self):
        pass

    def _process_counterexample(self, w):
        states = copy.deepcopy(self.S)
        max_pref, idx = "", -1
        for a in w:
            if max_pref + a in states:
                max_pref += a
                idx += 1
            else:
                break

        max_pref += w[idx + 1]  # dokładam jedną literkę
        idx += 1

        w = w[idx + 1 :]  # zostawiam sobie sufiks
        w = w[::-1]  # odwracam go

        suffixes, suffix = [], ""
        for a in w:
            suffix = a + suffix
            suffixes.append(suffix)
        self._extend_E(suffixes)