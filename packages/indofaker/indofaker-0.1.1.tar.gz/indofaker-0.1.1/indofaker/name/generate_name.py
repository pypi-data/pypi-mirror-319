import random

from indofaker.name.base_name import BaseName
from indofaker.name.family_name import  FamilyName, family_names
from indofaker.name.first_name import FirstName, first_names
from indofaker.name.gender import Gender
from indofaker.name.religion import Religion
from indofaker.name.tribe import Tribe


def generate_random_name():
    gender_list  = [
        Gender.ALL,
        Gender.MALE,
        Gender.FEMALE
    ]
    religion_list = [
        Religion.ALL,
        Religion.MOUSLEM,
        #Religion.CHRISTIAN
    ]
    tribe_list = [
        Tribe.ALL,
        Tribe.JAVA,
        Tribe.BATAK
    ]

    gender = random.choice(gender_list)
    tribe = random.choice(tribe_list)
    religion = random.choice(religion_list)
    return generate_name(gender,tribe, religion)



def generate_name(
        gender:Gender = Gender.ALL,
        tribe:Tribe= Tribe.ALL,
        religion:Religion = Religion.ALL,
):
    def name_filter(name: BaseName):
        return (
                (name.gender == gender or name.gender == Gender.ALL)  and
                (name.tribe == tribe or name.tribe == Tribe.ALL) and
                (name.religion == religion or name.religion == Religion.ALL)
        )

    def family_filter(name: BaseName):
        if tribe == Tribe.ALL:
            return True
        elif tribe == Tribe.BATAK:
            return name.tribe == tribe and name.religion == religion
        elif tribe == Tribe.BUGIS:
            return name.tribe == tribe and  (name.gender == gender or name.gender == Gender.ALL)
        else:
            return name.tribe == tribe

    filtered_first_names =  list(filter(name_filter, first_names))
    filtered_family_names =  list(filter(family_filter, family_names))


    first_name : FirstName = random.choice(filtered_first_names)
    family_name : FamilyName = random.choice(filtered_family_names)

    return f"{first_name.name} {family_name.name}"

