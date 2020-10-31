import random
import constants
import importlib
from utils import Utils

class EffectInfo:
    # Some effects are executed between rounds, so isExecutableEffect will be true
    # Other effects have an executable defensive effect, so isExecutableDefensiveEffect will be ture
    def __init__(self, name, endRound, affected, isExecutableDefensiveEffect, isIncapacitated, isExecutableEffect, msg):
        self.name = name
        self.endRound = endRound
        self.affected = affected
        self.isExecutableDefensiveEffect = isExecutableDefensiveEffect
        self.isIncapacitated = isIncapacitated
        self.isExecutableEffect = isExecutableEffect
        self.msg = msg
        self.vitalityScoreAdjustment = 0
        self.enduranceScoreAdjustment = 0
        self.strengthScoreAdjustment = 0
        self.dexterityScoreAdjustment = 0
        self.intelligenceScoreAdjustment = 0
        self.faithScoreAdjustment = 0
        self.hpAdjustment = 0

    def getName(self):
        return self.name

    def getEndRound(self):
        return self.endRound

    def getAffected(self):
        return self.affected

    def getIsExecutableDefensiveEffect(self):
        return self.isExecutableDefensiveEffect

    def getIsIncapacitated(self):
        return self.isIncapacitated

    def getIsExecutableEffect(self):
        return self.isExecutableEffect

    def setVitalityScoreAdjustment(self, value):
        self.vitalityScoreAdjustment = value

    def getVitalityScoreAdjustment(self):
        return self.vitalityScoreAdjustment
    
    def setEnduranceScoreAdjustment(self, value):
        self.enduranceScoreAdjustment = value
    
    def getEnduranceScoreAdjustment(self):
        return self.enduranceScoreAdjustment

    def setStrengthScoreAdjustment(self, value):
        self.strengthScoreAdjustment = value
    
    def getStrengthScoreAdjustment(self):
        return self.strengthScoreAdjustment

    def setDexterityScoreAdjustment(self, value):
        self.dexterityScoreAdjustment = value
    
    def getDexterityScoreAdjustment(self):
        return self.dexterityScoreAdjustment

    def setIntelligenceScoreAdjustment(self, value):
        self.intelligenceScoreAdjustment = value
    
    def getIntelligenceScoreAdjustment(self):
        return self.intelligenceScoreAdjustment
    
    def setFaithScoreAdjustment(self, value):
        self.faithScoreAdjustment = value
    
    def getFaithScoreAdjustment(self):
        return self.faithScoreAdjustment

    def setHpAdjustment(self, value):
        self.hpAdjustment = value
    
    def getHpAdjustment(self):
        return self.hpAdjustment
    
    def getMsg(self):
        return self.msg
    



class Rules():
    effects = []

    @staticmethod
    def getPlayerOrder(cbtList):
        random.shuffle(cbtList)

    @staticmethod
    def getTargetAction(target, cbtActions):
        for a in cbtActions:
            if a.getCombatant() == target:
                return a

    @staticmethod   
    def doAction(action, cbtActions, roundCount, specialAttackNamesDictionary):
        targets = action.getTargets()
        cbt = action.getCombatant()
        actionName = action.getActionName()

        """regular attacks can only have a single target so we use the target
         at index 0"""
        
        if actionName == "Attack":
            targetAction = Rules.getTargetAction(targets[0], cbtActions)
            Rules.doAttack(action, targetAction, specialAttackNamesDictionary)
        
        elif actionName == "Block":
            Rules.doBlock(cbt)
        
        elif actionName == "Rest":
            Rules.doRest(cbt)
        
        elif actionName == "Special Attack":
            specialAttack = action.getSpecialAttack()
            specialAttackName = specialAttack.getName()
            resultsList = []
            #we set stamina here to avoid decreasing stamina for every target
            stamCost = Rules.getStamCost(cbt, actionName, specialAttack)
            cbt.setStamina(cbt.getStamina() - stamCost)
            #we can't iterate if targets is None
            if targets == None:
                results = Rules.doSpecialAttack(action, None, roundCount, specialAttackNamesDictionary)
                resultsList.append(results)
            else:
                for t in targets:                
                    targetAction = Rules.getTargetAction(t, cbtActions)
                    results = Rules.doSpecialAttack(action, targetAction, roundCount, specialAttackNamesDictionary)
                    resultsList.append(results)
            Rules.displaySpecialAttackMsg(action, resultsList, roundCount, specialAttackName)

    @staticmethod
    def doAttack(cAction, tAction, specialAttackNamesDictionary):
        combatant = cAction.getCombatant()
        target = tAction.getCombatant()
        print(f'{combatant.getName()} is attacking {target.getName()}')
        combatant.setStamina(combatant.getStamina() - Rules.getStamCost(combatant, cAction.getActionName(), None))
        Rules.applyDefensiveEffects(cAction, target, specialAttackNamesDictionary)
        if Rules.determineHitOrMiss(cAction, tAction):
            print(f'{combatant.getName()}\'s attack was successful!')
            damage = Rules.getDmg(combatant)
            damage = Utils.checkMinValue(damage, 0)
            target.setHp(target.getHp() - damage)
            print(f'{target.getName()} took {damage} damage.')
        else:
            print(f'{combatant.getName()}\'s attack missed!')

    def applyDefensiveEffects(cAction, target, specialAttackNamesDictionary):
        for e in target.getEffects():
            if e.getIsExecutableDefensiveEffect():
                #getting the file and class from the name of the effect
                className = specialAttackNamesDictionary.getClassName(e.getName())
                fileName = className[0].lower() + className[1:]
                specialAttackClass = getattr(importlib.import_module(fileName), className)
                specialAttack = specialAttackClass()
                specialAttack.executeDefensiveEffect(cAction, target)


    @staticmethod
    def doBlock(combatant):
        stamRegen = constants.STAMREGENBLOCK + Rules.getModifier(combatant.getAdjustedVitality())
        previousStamina = combatant.getStamina()
        combatant.setStamina(previousStamina + stamRegen)
        print(f'By blocking, {combatant.getName()} recovered {str(combatant.getStamina() - previousStamina)} stamina.')

    @staticmethod
    def doRest(combatant):
        stamRegen = constants.STAMREGENREST + Rules.getModifier(combatant.getAdjustedVitality())
        previousStamina = combatant.getStamina()
        combatant.setStamina(previousStamina + stamRegen)
        print(f'By resting, {combatant.getName()} recovered {str(combatant.getStamina() - previousStamina)} stamina.')

    @staticmethod
    def doSpecialAttack(cAction, tAction, roundCount, specialAttackNamesDictionary):
        combatant = cAction.getCombatant()
        target = None
        """getting the target from the target action gives us a single target
        rather than a list"""
        if tAction != None:
            target = tAction.getCombatant()
        specialAttack = cAction.getSpecialAttack()
        specialAttackName = specialAttack.getName()
        """for now, only physical attacks are subject to defensive effects
        ***subject to change*** """
        if specialAttack.getAtkType() == "P" and target != None:
            Rules.applyDefensiveEffects(cAction, target, specialAttackNamesDictionary)
        results = None

        className = specialAttackNamesDictionary.getClassName(specialAttackName)
        fileName = className[0].lower() + className[1:]
        specialAttackClass = getattr(importlib.import_module(fileName), className)
        specialAttack = specialAttackClass()
        results = specialAttack.execute(cAction, tAction, roundCount)
        if results.getHitOrMiss():
            target.setHp(target.getHp()- results.getDamage())
        effects = results.getEffects()

        for effect in effects:
            Rules.addEffect(effect)

        return results

    @staticmethod
    def getTargetNames(targets):
        nameString = ''
        if len(targets)>1:
            for i in range(len(targets)):
                target = targets[i]
                #if we are on the second to last target
                if i == len(targets)-2:
                    nameString += target.getName() + ' and ' + targets[i+1].getName()
                    return nameString
                else:
                    nameString += target.getName() + ", "
        #if there is only one target we simply return its name
        else:
            nameString = targets[0].getName()
            return nameString

    @staticmethod
    def displaySpecialAttackMsg(cAction, resultList, roundCount, specialAttackName):
        combatant = cAction.getCombatant()
        cName = combatant.getName()
        targets = cAction.getTargets()
        string = f'{cName} is performing {specialAttackName}'
        if cAction.getTargets() != None:
            string += f' against {Rules.getTargetNames(targets)}'
        string += "."
        print(string)
        #new list with only results that have targets
        resultWithTargetList = list(filter(Rules.filterNones,resultList))
        if len(resultWithTargetList) > 0:
            for result in resultWithTargetList:
                hitOrMiss = result.getHitOrMiss()
                tName = result.getTarget().getName()
                atkType = cAction.getSpecialAttack().getAtkType()
                damage = result.getDamage()
                effects = result.getEffects()
                if hitOrMiss:
                    print(f'{tName} took {damage} damage.') 
                    """ some magic attacks do not use hitOrMiss, 
                    so we have to deal with them separately """
                elif atkType == "M":
                    if damage > 0:
                        if result.getMsg() != "":
                            print(result.getMsg())
                        print(f'{tName} took {damage} damage')
                        """ magic attacks that do 0 damage and have no effect
                        are deemed ineffective """
                    elif len(effects) == 0:
                        print(f'The magic had no effect against {tName}.')
                    else:
                        if result.getMsg() != "":
                            print(result.getMsg())
                #for physical attacks that hit, hitOrMiss is always True               
                elif atkType == "P":
                    print(f'{cName}\'s attack missed {tName}.')

                for e in effects:
                    """ we only want the message to print once if the person
                    is put under the same effect twice in one round"""
                    if not Rules.isCombatantUnderEffect(result.getTarget(), e, roundCount) and e.getMsg() != "":
                        msg = e.getMsg()
                        if msg != '':
                            print(msg)
        #special attacks with results that do not have targets are simply performed
        else:
            print(f'{cName} performed {specialAttackName}!')

    def filterNones(element):
        return element.getTarget() != None

    @staticmethod
    def determineHitOrMiss(cAction, tAction):
        target = tAction.getCombatant()
        combatant = cAction.getCombatant()
        roll = random.randint(1,20)
        attack = roll + combatant.toHit
        defense = target.getPhysDefense()
        # all regular attacks are physical, so we default to "P"
        atkType = "P"
        if cAction.getSpecialAttack() != None:
            atkType = cAction.getSpecialAttack().getAtkType()
        if atkType == "M":
            defense = target.getMagDefense()
        #blocking adds to the targets' defense only if the attack is physical
        if tAction.getActionName() == "Block" and atkType == "P":
            defense += constants.BLOCK
        if attack >= defense:
            return True
        return False

    def addEffect(effect):
        if not effect.getIsExecutableDefensiveEffect():
            #because we will iterate backwards through this list, we insert effects at the front of the list
            Rules.effects.insert(0,effect)
        # if it's a defensive effect, we check to make sure cbt does not already have that effect; if true, replace
        # https://stackoverflow.com/questions/2582138/finding-and-replacing-elements-in-a-list
        else:
            replaced = False
            for i,e in enumerate(Rules.effects):
                if e.getName() == effect.getName() and e.getAffected() == effect.getAffected():
                    Rules.effects[i] == effect
                    replaced = True
            if not replaced:
                Rules.effects.insert(0,effect)

    #returns a bonus based on the value of an attribute
    def getModifier(score):
        if score <= 0:
            return -5
        elif score <= 3:
            return -4
        elif score <= 5:
            return -3
        elif score <= 7:
            return -2
        elif score <= 9:
            return -1
        elif score <= 11:
            return 0
        elif score <= 13:
            return 1
        elif score <= 15:
            return 2
        elif score <= 17:
            return 3
        elif score <= 19:
            return 4
        elif score <= 21:
            return 5
        elif score <= 23:
            return 6
        elif score <= 25:
            return 7
        elif score <= 27:
            return 8
        elif score <= 29:
            return 9
        else:
            return 10

    @staticmethod
    def isCombatantUnderEffect(combatant, effect, roundCount):
        if effect == None:
            return False
        for e in Rules.effects:
            # we want to ignore the effect that we are currently processing
            if e == effect:
                continue
            if e.getAffected() == combatant and e.getName() == effect.getName() and effect.getEndRound() >= roundCount:
                return True
        return False
    
    @staticmethod
    def getStamCost(cbt, actionName, specialAttack):
        stamCost = 0
        if actionName == "Attack":
            stamCost = cbt.getStamCost()
        elif actionName == "Special Attack" and specialAttack != None:
            stamCost = specialAttack.getStamCost()
        stamCost -= Rules.getModifier(cbt.getAdjustedEndurance())
        if stamCost <= 0:
            stamCost = 1
        return stamCost

    def getDmg(cbt):
        dmg = cbt.getDmg() + Rules.getModifier(cbt.getAdjustedStrength())
        dmg = Utils.checkMinValue(dmg, 0)
        return dmg

class ActionInfo:
    def __init__(self, combatant, targets, actionName, specialAttack = None):
        self.combatant = combatant
        self.targets = targets
        self.actionName = actionName
        self.specialAttack = specialAttack
    
    def getCombatant(self):
        return self.combatant
    
    def getTargets(self):
        return self.targets
    
    def getActionName(self):
        return self.actionName

    def getSpecialAttack(self):
        return self.specialAttack

class TargetInfo:
    def __init__ (self, target, targetNumber):
        self.target = target
        self.targetNumber = targetNumber

    def getTarget(self):
        return self.target
    
    def getTargetNumber(self):
        return self.targetNumber