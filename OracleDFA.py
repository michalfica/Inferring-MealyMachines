class OracleDFA:
    """konwencja:
    Q                   - liczba stanów maszyny,
    δ                   - funkcja (q,a) -> q'(funkcja przejścia automatu), słownik
    F                   - zbiór stanów akceptujących
    """

    NO_ANSWER = ""

    def __init__(self, Q, alphabet=[], δ=dict(), F=set()):
        self.Q = Q
        self.alphabet = alphabet
        self.δ = δ
        self.F = F

    def __str__(self):
        return f"DFA amount of states = {self.Q}, transitions = {self.δ}, accept states = {self.F}"

    def route(self, w):
        q, v = 0, ""
        for i in range(2 * len(w)):
            if i % 2 == 0:
                # print(f"czytam {w[i//2]}, jestem w {q} ide do {self.δ[(q, w[i // 2])]}")
                q = self.δ[(q, w[i // 2])]
            else:
                for a in self.alphabet:
                    if (q, a) in self.δ:
                        v += a
                        q = self.δ[(q, a)]
        # print(f"na koniec jestem w {q}, utworzyłem v = {v}")
        if q in self.F:
            return v
        else:
            return self.NO_ANSWER
