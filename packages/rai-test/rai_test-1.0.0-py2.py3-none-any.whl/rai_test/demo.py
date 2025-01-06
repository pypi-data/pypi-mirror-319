import os
import sys

class RaiSamTest():
    def __init__(
        self,
        verbose = False,
    ):
        super().__init__()
        print("RaiSamTest -- __init__")

    def __del__(self):
        pass

    def RaiSamTestContact(
        self,
        pid: str,
        psw: str) -> str:

        print("pid: ", pid)
        print("psw: ", psw)

        return pid + psw

