from enum import IntEnum

class Attribute(IntEnum):
        VITALITY = 1
        ENDURANCE = 2
        STRENGTH = 3
        DEXTERITY = 4
        INTELLIGENCE = 5
        FAITH = 6
    
class ClassType(IntEnum):
        WARRIOR = 1
        MAGE = 2
        ROGUE = 3
        CLERIC = 4