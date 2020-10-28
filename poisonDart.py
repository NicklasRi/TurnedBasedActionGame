from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
import constants

class PoisonDart:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        if hitOrMiss:
            effect = EffectInfo("Poison Dart", roundCount + 3, target, False, False, True, "")
            effect.setHpAdjustment(-6)
            effects.append(effect)
        return SpecialAttackResults('', hitOrMiss, 0, effects, target)

    #we must execute the "Poison Dart" effect between every round
    def executeEffect(self, affected):
        chance = random.randint(1,100) + round(constants.POISONFACTOR * (Rules.getModifier(affected.getAdjustedVitality())))
        if chance <= 3:
            print(f'{affected.getName()} is succumbing to the poison!')
            affected.setHp(0)
