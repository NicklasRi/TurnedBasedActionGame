from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
import constants
from utils import Utils

class PoisonDart:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        if hitOrMiss:
            effect = EffectInfo("Poison Dart", roundCount + constants.POISONDURATION, target, False, False, True, "")
            effect.setHpAdjustment(constants.POISONPERROUNDDMG)
            effects.append(effect)
        return SpecialAttackResults('', hitOrMiss, 0, effects, target)

    #we must execute the "Poison Dart" effect between every round
    def executeEffect(self, affected):
        chance = random.randint(1,100)
        x = round(constants.POISONFACTOR * (Rules.getModifier(affected.getAdjustedVitality())))
        # we want there to be at least a 1% chance to die to poison
        x = Utils.checkMaxValue(x,2)
        chance += x
        if chance <= constants.POISIONKILLPER:
            print(f'{affected.getName()} is succumbing to the poison!')
            affected.setHp(0)
