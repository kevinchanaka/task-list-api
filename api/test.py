from dataclasses import dataclass


class Foo:
    var3 = 3

    def __init__(self):
        self.var1 = 1
        self.var2 = 2


@dataclass
class Bar:
    var1 = 1
    var2 = 2
    _var3 = 3
