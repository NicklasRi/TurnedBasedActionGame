import unittest
from game import Game
from class_combatant import Warrior, Mage, Rogue
from enums import Attribute

class Test(unittest.TestCase):
    
    def test_testBattle(self):
        combatants = []
        warrior = Warrior(1, "Joe")
        combatants.append(warrior)
        rogue = Rogue(2, "Bob")
        combatants.append(rogue)
        mage = Mage(3, "Will")
        combatants.append(mage)
        for c in combatants:
            c.applyPoints(Attribute.DEXTERITY, 20)
            c.getAdjustedDexterity()


        Game.loadSpecialAttacks()

        Game.doBattle(combatants)