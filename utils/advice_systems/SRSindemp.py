# from advice_system1 import advice_system1
from importlib import reload
import utils.advice_systems.SRS as SRS

reload(SRS)

from utils.advice_systems.SRS import SRS


class SRSindemp(SRS):

    def __init__(self, letter):
        pi = [(letter + letter, letter)]
        self.pi = pi

    def get_normal_form(self, w):
        nf_w = w

        while nf_w.find("aa") != -1:
            l = nf_w.find("aa")
            r = l + 1
            while r + 1 < len(nf_w) and nf_w[r + 1] == "a":
                r += 1
            nf_w = nf_w[:l] + "a" + nf_w[r + 1 :]

        return nf_w
