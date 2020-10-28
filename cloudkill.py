import random
import constants
from specialAttack import SpecialAttackResults
from utils import Utils


class Cloudkill:
    def execute(self, cAction, tAction, roundCount):
        target = tAction.getCombatant()
        chance = constants.CLOUDKILLPER - target.getMagDefense()
        msg = ''
        damage = 0
        Utils.checkMinValue(chance, 1)
        roll = random.randint(1,100)
        if roll <= chance:
            damage = target.getHp()
            msg = f'{target.getName()} has been disintegrated!'
        results = SpecialAttackResults(msg, False, damage, [], target)
        return results