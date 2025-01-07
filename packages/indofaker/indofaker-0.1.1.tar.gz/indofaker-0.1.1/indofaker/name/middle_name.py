from indofaker.name.base_name import BaseName
from indofaker.name.religion import Religion
from indofaker.name.tribe import Tribe


class MiddleName(BaseName):
    def __init__(self, name: str, religion: Religion, tribe: Tribe):
        super().__init__(name, religion, tribe)