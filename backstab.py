from rules import Rules, EffectInfo
from specialAttack import SpecialAttackResults
import random
from utils import Utils

class Backstab:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()

        hitOrMiss = Rules.determineHitOrMiss(cAction, tAction)
        damage = 0
        #combatants get a temporary dex penalty when doing a backstab
        msg = f'{combatant.getName()}\'s dexterity has been reduced by 2!'
        backstab = EffectInfo("Backstab", roundCount + 1, combatant, False, False, False, msg)
        backstab.setDexterityScoreAdjustment(-2)
        effects.append(backstab)
        if hitOrMiss:
            #bleed effect
            if (random.randint(1,25) + combatant.getDexterity()) <= 25:
                msg = f'{target.getName()} is bleeding!'
                bleed = EffectInfo("Bleed", roundCount + 3, target, False, False, False, msg)
                bleed.setHpAdjustment(-random.randint(1,4))
                effects.append(bleed)

            damage = random.randint(4,24) + Rules.getModifier(combatant.getDexterity())
            damage = Utils.checkMinValue(damage, 0)

        return SpecialAttackResults('', hitOrMiss, damage, effects, target)
                
