from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
from utils import Utils
import constants

class KnifeBarrage:
    def execute(self, cAction, tAction, roundNumber):
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        damage = 0
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        if hitOrMiss:
            dexterity = combatant.getAdjustedDexterity()
            damage = random.randint(1,6) + round(constants.KNIFEBARRAGEFACTOR * Rules.getModifier(combatant.getAdjustedDexterity()))
            damage = Utils.checkMinValue(damage, 0)
        return SpecialAttackResults('', hitOrMiss, damage, [], target)