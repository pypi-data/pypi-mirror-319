from indofaker.name.base_name import BaseName
from indofaker.name.gender import Gender
from indofaker.name.religion import Religion
from indofaker.name.tribe import Tribe


class FirstName(BaseName):
    def __init__(self, name: str,gender:Gender, religion: Religion, tribe: Tribe):
        super().__init__(name, gender, religion, tribe)





first_names = [

    # MALE, MUSLIM, ALL
    FirstName("Muhammad", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Mochammad", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Akhmad", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Achmad", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Abdul", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Abdullah", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),
    FirstName("Ali", Gender.MALE, Religion.MOUSLEM, Tribe.ALL),

    # MALE, CHRISTIAN, ALL
    FirstName("Christian", Gender.MALE, Religion.CHRISTIAN, Tribe.ALL),
    FirstName("John", Gender.MALE, Religion.CHRISTIAN, Tribe.ALL),
    FirstName("Johannes", Gender.MALE, Religion.CHRISTIAN, Tribe.ALL),
    FirstName("Mikael", Gender.MALE, Religion.CHRISTIAN, Tribe.ALL),

    # ALL, ALL, ALL
    FirstName("Nur", Gender.ALL, Religion.ALL, Tribe.ALL),
    FirstName("Tri", Gender.ALL, Religion.ALL, Tribe.ALL),

    # MALE, ALL, ALL
    FirstName("Agus", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Budi", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Dedi", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Eko", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Firman", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Hadi", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Joko", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Karto", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Mardi", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Purwadi", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Surya", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Wijaya", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Yudha", Gender.MALE, Religion.ALL, Tribe.ALL),
    FirstName("Zul", Gender.MALE, Religion.ALL, Tribe.ALL),

    # FEMALE, ALL, ALL
    FirstName("Anisa", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Ayu", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Dewi", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Fitri", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Gita", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Indah", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Kartini", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Lestari", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Lia", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Lina", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Mega", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Okta", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Ratna", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Rini", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Santi", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Sri", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Wulan", Gender.FEMALE, Religion.ALL, Tribe.ALL),
    FirstName("Yanti", Gender.FEMALE, Religion.ALL, Tribe.ALL),
]




