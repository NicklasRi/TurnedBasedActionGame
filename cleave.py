import random
import constants
from rules import EffectInfo, Rules
from specialAttack import SpecialAttackResults
from utils import Utils

class Cleave:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        damage = 0
        if hitOrMiss:
            damage = random.randint(3,30) + Rules.getModifier(cAction.getCombatant().getAdjustedStrength())
            damage = Utils.checkMinValue(damage, 0)
            percent = random.randint(1,100)
            if percent <= constants.CLEAVEPER:
                effect = EffectInfo("Cleave", roundCount + constants.CLEAVEDURATION, target, False, False, False, f'{target.getName()} has been dazed!')
                effects.append(effect)
        sResults = SpecialAttackResults('', hitOrMiss, damage, effects, target)
        return sResults