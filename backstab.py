from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
from utils import Utils
import constants

class Backstab:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()

        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        damage = 0
        #combatants get a temporary dex penalty when doing a backstab
        msg = f'{combatant.getName()}\'s dexterity has been reduced by 2!'
        backstab = EffectInfo("Backstab", roundCount + constants.BACKSTABDURATION , combatant, False, False, False, msg)
        backstab.setDexterityScoreAdjustment(constants.BACKSTABDEXPENALITY)
        effects.append(backstab)
        if hitOrMiss:
            #bleed effect
            chance = random.randint(1,constants.BLEEDPER) + Rules.getModifier(target.getAdjustedDexterity())
            chance = Utils.checkMaxValue(chance, constants.BLEEDPER)
            if chance <= constants.BLEEDPER:
                msg = f'{target.getName()} is bleeding!'
                bleed = EffectInfo("Bleed", roundCount + constants.BLEEDDURATION, target, False, False, False, msg)
                bleed.setHpAdjustment(-random.randint(1,6))
                effects.append(bleed)

            damage = random.randint(4,24) + Rules.getModifier(combatant.getAdjustedDexterity())
            damage = Utils.checkMinValue(damage, 0)

        return SpecialAttackResults('', hitOrMiss, damage, effects, target)
                
