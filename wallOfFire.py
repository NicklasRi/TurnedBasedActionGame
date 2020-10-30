from rules import EffectInfo
from specialAttack import SpecialAttackResults
import random
import constants

class WallOfFire:
    def execute(self, cAction, tAction, roundCount):
        effects = []
        combatant = cAction.getCombatant()
        effect = EffectInfo("Wall of Fire", roundCount + constants.WALLOFFIREDURATION, combatant, True, False, False, '')
        effects.append(effect)
        results = SpecialAttackResults('', False, 0, effects, None)
        return results

    """defensive effects are executed every time a combatant that is under a
    defensive effect is attacked"""
    def executeDefensiveEffect(self, cAction, target):
        combatant = cAction.getCombatant()
        specialAttack = cAction.getSpecialAttack()
        """all combatants who execute standard attacks or non-ranged special attacks
        against a combatant with Wall of Fire cast are damaged""" 
        if specialAttack == None or not specialAttack.getIsRanged():
                damage = random.randint(3,24)
                combatant.setHp(combatant.getHp() - damage)
                print(f'{combatant.getName()} took {damage} damage from {target.getName()}\'s Wall of Fire!')