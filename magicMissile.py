import random
from rules import Rules
from specialAttack import SpecialAttackResults
from utils import Utils
import constants

class MagicMissile:
    def execute(self, cAction, tAction, roundCount):
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        numMissles = ((combatant.getAdjustedIntelligence() - 15) // 5) + 3
        damage = random.randint(numMissles, constants.PERMISSILEDMG * numMissles)
        damage = Utils.checkMinValue(damage, 0)
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        msg = ""
        #for magic missile, a "miss" reduces the damage received by half
        if not hitOrMiss:
            damage = damage//2
            msg = str(tAction.getCombatant().getName()) + "\'s magic defense reduced the damage by half."
        results = SpecialAttackResults(msg, hitOrMiss, damage, [], target)
        return results