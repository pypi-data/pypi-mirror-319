from indofaker.name.base_name import BaseName
from indofaker.name.gender import Gender
from indofaker.name.religion import Religion
from indofaker.name.tribe import Tribe


class FamilyName(BaseName):
    def __init__(self, name: str, gender: Gender, religion: Religion, tribe: Tribe):
        super().__init__(name, gender, religion, tribe)


family_names = [

    # ALL, ALL, ALL
    FamilyName("Sanjaya", Gender.ALL, Religion.ALL, Tribe.ALL),
    FamilyName("Kurnia", Gender.ALL, Religion.ALL, Tribe.ALL),

    # Jawa

    FamilyName("Arifin", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Bambang", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Basuki", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Budi", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Darmadi", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Haryono", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Hartono", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Iskandar", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Joko", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Karto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Krisna", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Kuswandi", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Marwoto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Mukti", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Prabowo", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Raharjo", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Saputra", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Setyawan", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Siswanto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Sudirman", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Sugeng", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Sugiyarto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Suharmono", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Suharto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Sukarno", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Supriyadi", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Surya", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Susanto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Triyono", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Waluyo", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Widodo", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Wijaya", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Wiranto", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Wiyono", Gender.ALL, Religion.ALL, Tribe.JAVA),
    FamilyName("Yudha", Gender.ALL, Religion.ALL, Tribe.JAVA),

    # Batak
    FamilyName("Butarbutar", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Harahap", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Hasibuan", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Hutagalung", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Hutauruk", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Lumbanbatu", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Lumbangaol", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Lumbantoruan", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Malau", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Manurung", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Marbun", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Nababan", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Pangaribuan", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Panjaitan", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Pardede", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Pasaribu", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Silalahi", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sibarani", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sianipar", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Simanjuntak", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Simatupang", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Simbolon", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sinaga", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Siregar", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sitanggang", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sitompul", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Sitorus", Gender.ALL, Religion.ALL, Tribe.BATAK),
    FamilyName("Tampubolon", Gender.ALL, Religion.ALL, Tribe.BATAK),

    # BATAK MUSLIM
    FamilyName("Nasution", Gender.ALL, Religion.MOUSLEM, Tribe.BATAK),

]
