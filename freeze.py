import random
import constants
from rules import EffectInfo, Rules
from specialAttack import SpecialAttackResults
from utils import Utils

class Freeze:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        target = tAction.getCombatant()
        chance = constants.FREEZEPER - target.getMagDefense()
        msg = ''
        chance = Utils.checkMinValue(chance, 1)
        roll = random.randint(1,100)
        if roll <= chance:
            effect = EffectInfo("Freeze", roundCount + constants.FREEZEDURATION, target, None, True, False, f'{target.getName()} has been frozen!')
            effects.append(effect)
            
        return SpecialAttackResults('', False, 0, effects, target)