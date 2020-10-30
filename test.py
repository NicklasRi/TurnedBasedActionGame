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

        
    def test_demo(self):
        combatants = []

        rogue = Rogue(1, "Tyrion")
        combatants.append(rogue)
        rogue.applyPoints(Attribute.DEXTERITY, 11)
        rogue.applyPoints(Attribute.ENDURANCE, 4)
        rogue.applyPoints(Attribute.VITALITY, 5)

        warrior = Warrior(2, "Solaire")
        combatants.append(warrior)
        warrior.applyPoints(Attribute.STRENGTH, 13)
        warrior.applyPoints(Attribute.ENDURANCE, 3)
        warrior.applyPoints(Attribute.VITALITY, 4)

        mage = Mage(3, "Eyia")
        combatants.append(mage)
        mage.applyPoints(Attribute.INTELLIGENCE, 10)
        mage.applyPoints(Attribute.DEXTERITY, 6)
        mage.applyPoints(Attribute.VITALITY, 4)

        Game.loadSpecialAttacks()
        Game.doBattle(combatants)