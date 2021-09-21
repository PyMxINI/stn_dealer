import re
import steampy.client

class Currency:
    ref = 0
    key = 0

    def __init__(self, *args):

        if len(args) == 2:
            self._init1(args[0], args[1])
        else:
            self._init2(args[0])

    def _init1(self, key: int, ref: float):
        self.ref = ref
        self.key = key
        self.valid = True

    def _init2(self, text: str):
        try:
            key_regex = re.findall(r"(\d+) key", text)
            ref_regex = re.findall(r"(\d+.\d+|\d+) ref", text)
            if key_regex:
                self.key = int(key_regex[0])
            if ref_regex:
                self.ref = float(ref_regex[0])
            if ref_regex or key_regex:
                self.valid = True
            else:
                self.valid = False

        except:
            self.valid = False

    def __str__(self):
        return f"{self.key} key, {self.ref} ref"

    def __eq__(self, other):
        return self.ref == other.ref and self.key == other.key

    def __gt__(self, other):
        if self.key == other.key:
            return self.ref > other.ref
        return self.key > other.key and self.ref > other.ref

    def __add__(self, other):
        return Currency(self.key + other.key, self.ref + other.ref)

    def __sub__(self, other):

        return Currency(self.key - other.key, self.ref - other.ref)
