import random
import constants
from rules import EffectInfo, Rules
from specialAttack import SpecialAttackResults

class Freeze:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        target = tAction.getCombatant()
        chance = constants.FREEZEPER - target.getMagDefense()
        msg = ''
        if chance < 1:
            chance = 1
        roll = random.randint(1,100)
        if roll <= chance:
            effect = EffectInfo("Freeze", roundCount + 2, target, None, True, False, f'{target.getName()} has been frozen!')
            effects.append(effect)
            
        return SpecialAttackResults('', False, 0, effects, target)