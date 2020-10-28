from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
from utils import Utils

class Whirlwind:
    def execute(self, cAction, tAction, roundNumber):
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        targets = cAction.getTargets()
        targetIndex = targets.index(target)

        damage = 0
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        if hitOrMiss:
            dexterity = combatant.getAdjustedDexterity()
            damage = random.randint(1,8) + round(0.4 * Rules.getModifier(combatant.getAdjustedDexterity()))
            damage = Utils.checkMinValue(damage, 0)
            #damage is multiplied by a factor of n for the nth target attacked
            damage = damage * (targetIndex + 1)
        return SpecialAttackResults('', hitOrMiss, damage, [], target)