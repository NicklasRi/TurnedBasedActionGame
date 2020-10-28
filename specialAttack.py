class SpecialAttack:
    def __init__(self, name, stamCost, atkType, needsTarget, isRanged, maxTargets,needsTargetOrder):
        self.name = name
        self.stamCost = stamCost
        self.atkType = atkType
        self.needsTarget = needsTarget
        self.isRanged = isRanged
        self.maxTargets = maxTargets
        self.needsTargetOrder = needsTargetOrder
    
    def getName(self):
        return self.name

    def getStamCost(self):
        return self.stamCost

    def getAtkType(self):
        return self.atkType

    def getNeedsTarget(self):
        return self.needsTarget

    def getIsRanged(self):
        return self.isRanged

    def getMaxTargets(self):
        return self.maxTargets
    
    def getNeedsTargetOrder(self):
        return self.needsTargetOrder

class SpecialAttackResults:
    def __init__(self, msg, hitOrMiss, damage, effects, target):
        self.msg = msg
        self.hitOrMiss = hitOrMiss
        self.damage = damage
        self.effects = effects
        self.target = target
    
    def getMsg(self):
        return self.msg

    def getHitOrMiss(self):
        return self.hitOrMiss

    def getDamage(self):
        return self.damage

    def getEffects(self):
        return self.effects

    def getTarget(self):
        return self.target