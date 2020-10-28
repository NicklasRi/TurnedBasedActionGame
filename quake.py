import random
import constants
from rules import EffectInfo, Rules
from specialAttack import SpecialAttackResults
from utils import Utils

class Quake:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        damage = random.randint(2,24) + Rules.getModifier(cAction.getCombatant().getAdjustedStrength())
        damage = Utils.checkMinValue(damage,0)
        target = tAction.getCombatant()
        effect = EffectInfo("Quake", roundCount + constants.QUAKEDURATION, target, False, False, False, f'{target.getName()}\'s dexterity has been reduced by {str(abs(constants.QUAKEDEXPENALTY))}.')
        effect.setDexterityScoreAdjustment(constants.QUAKEDEXPENALTY)
        effects.append(effect)
        sResults = SpecialAttackResults('', True, damage, effects, target)
        return sResults