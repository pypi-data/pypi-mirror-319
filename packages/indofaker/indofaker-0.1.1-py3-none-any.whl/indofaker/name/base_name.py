from indofaker.name.gender import Gender
from indofaker.name.religion import Religion
from indofaker.name.tribe import Tribe


class BaseName():
    def __init__(self, name: str, gender:Gender, religion: Religion, tribe: Tribe):
        self.name = name
        self.religion = religion
        self.tribe = tribe
        self.gender = gender


