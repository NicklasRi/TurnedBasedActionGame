import importlib
from class_combatant import Combatant, Warrior, Mage
from rules import Rules, ActionInfo, TargetInfo
from enums import Attribute, ClassType
from specialAttack import SpecialAttack
from specialAttackNamesDictionary import SpecialAttackNamesDictionary
from poisonDart import PoisonDart
from utils import Utils

global classNames
classNames = ['Warrior', 'Mage', 'Rogue']
global seeEffects
seeEffects = True


class ClassInfo: 
    def __init__(self, name, number):
        self.name = name
        self.number = number
    def __repr__(self):
        return f'{self.number}. {self.name}'

class ClassList:
    def __init__(self):
        self.ClassList = [ClassInfo("Warrior", 1), ClassInfo("Mage",2), ClassInfo("Rogue", 3)]

    @staticmethod
    def dispClassList():
        for i in ClassList().ClassList:
            print(f'{i}\n')

class Game:
    cbtActions = []
    defeatedCombatants = []
    specialAttacks = {}
    roundCount = 1
    # used to get special attack classes from special attack names
    specialAttackNamesDictionary = SpecialAttackNamesDictionary()
    
    @staticmethod
    def createCombatants():
        combatants = []
        idCount = 1
        while True:
            print("Enter \"1\" to create a new character, any other key to continue")
            choice = str(input())
            if choice == "1":
                print("---- Character " + str(idCount) + " ----")
                print("Enter the name of your character")
                nameChoice = Game.getNameChoice(combatants)
                print()
                print("Select a class by entering its corresponding number:")
                ClassList.dispClassList()
                classChoice = int(input())
                combatant = None
                className = classNames[classChoice - 1]
                combatantClass = getattr(importlib.import_module("class_combatant"), className)
                combatant = combatantClass(idCount, nameChoice)
                #MyClass = getattr(importlib.import_module("module.submodule"), "MyClass")
                Game.getAttributes(combatant)
                combatants.append(combatant)
                idCount += 1
                if idCount == 7:
                    return combatants

            elif len(combatants)<2:   
                print("You must create at least 2 combatants.")   
                
            else:
                return combatants       

    #checks that each character has a unique name
    @staticmethod
    def getNameChoice(combatants):
        while True:
            nameChoice = str(input())
            names = map(lambda x: x.getName(),combatants)
            if nameChoice in names:
                print("That name is already in use. Please choose another.")
                continue
            return nameChoice

    @staticmethod
    def getAttributes(cbt):
        while cbt.getPoints() > 0:
            print()
            print("Points left: " + str(cbt.getPoints()))
            print()
            Game.dispAttributes(cbt)
            print()
            print("Select the attribute to which you want to allocate points: \n1. Vitality\n2. Endurance\n3. Strength\n4. Dexterity\n5. Intelligence\n6. Faith")
            attributeChoice = int(input())
            while True:
                    print("Enter the amount of points to allocate (attributes may not exceed 30):")
                    pointChoice = int(input())
                    if pointChoice > cbt.getPoints():
                        print("You don't have enough points remaining. Points left: " + str(cbt.getPoints()))
                        continue
                    else:
                        if not cbt.applyPoints(attributeChoice, pointChoice):
                            print("Attributes may not exceed 30")
                            continue
                    break
        print()
        print(f'--Final Stats of {cbt}--')
        Game.dispAttributes(cbt)
        print()
                
    @staticmethod
    def dispAttributes(cbt):
        print(f'Vitality: {cbt.getAdjustedVitality()}\nEndurance: {cbt.getAdjustedEndurance()}\nStrength: {cbt.getAdjustedStrength()}\nDexterity: {cbt.getAdjustedDexterity()}\nIntelligence: {cbt.getAdjustedIntelligence()}\nFaith: {cbt.getAdjustedFaith()}')

    @staticmethod
    def getAction(cbt):
        while True:
            selectionNumber = 1
            actionList = []
            print("Select an action by entering its corresponding number:")
            for a in Combatant.actions:
                actionList.append((selectionNumber,a))
                print(f'{selectionNumber}. {a}')
                selectionNumber += 1
            actionChoice = int(input())
            actionString = Utils.getElementFromChoice(actionChoice,actionList)
            if actionString == None:
                print("Selected action is not valid. Please enter another number.")
            else:
                return actionString

    @staticmethod
    def doBattle(combatants):
        global seeEffects
        print("--------------------")
        print("The battle begins!")
        print("--------------------")
        print()
        Rules.getPlayerOrder(combatants)
        while True:
            print("---------------")
            print(f'Round {str(Game.roundCount)} begins!')
            print("---------------")
            Game.processEffects(combatants)
            if seeEffects and Game.roundCount != 1:
                print()
                print("-----Combatant effects-----")
                print()
                Game.displayEffects(combatants)
            print("")
            Game.collectRoundActions(combatants)
            gameOver = Game.processRound(combatants)
            if gameOver:
                Game.displayFinal(combatants)
                break
            print()
            print("-----Statuses after round " + str(Game.roundCount) + "-----")
            print()
            Game.displayStatuses(combatants)
            Game.roundCount += 1

    
    @staticmethod
    def processEffects(combatants):
        for c in combatants:
            c.setTemporaryVitality(0)
            c.setTemporaryEndurance(0)
            c.setTemporaryStrength(0)
            c.setTemporaryDexterity(0)
            c.setTemporaryIntelligence(0)
            c.setTemporaryFaith(0)
            c.getEffects().clear()
            c.getLatentEffects().clear()
        

        for i in range(len(Rules.effects)-1, -1, -1):
            effect = Rules.effects[i]
            affected = effect.getAffected()
            effectName = effect.getName()
            if Game.roundCount > effect.getEndRound():
                Rules.effects.remove(effect)
            else:
                """ we are checking if any one effect has been applied already to the same character in the round.
                if it has, we do not want to apply it more than once """
                needsToBeApplied = (not any(effect.getName() == e.getName() for e in affected.getEffects()))
                if needsToBeApplied:
                    affected.getEffects().append(effect)
                    affected.setTemporaryVitality(affected.getTemporaryVitality() + effect.getVitalityScoreAdjustment())
                    affected.setTemporaryEndurance(affected.getTemporaryEndurance() + effect.getEnduranceScoreAdjustment())
                    affected.setTemporaryStrength(affected.getTemporaryStrength() + effect.getStrengthScoreAdjustment())
                    affected.setTemporaryDexterity(affected.getTemporaryDexterity() + effect.getDexterityScoreAdjustment())
                    affected.setTemporaryIntelligence(affected.getTemporaryIntelligence() + effect.getIntelligenceScoreAdjustment())
                    affected.setTemporaryFaith(affected.getTemporaryFaith() + effect.getFaithScoreAdjustment())
                    
                    hpAdjustment = effect.getHpAdjustment()
                    if hpAdjustment != 0:
                        word = "reduced"
                        if hpAdjustment > 0:
                            word = "increased"
                        affected.setHp(affected.getHp() + hpAdjustment)
                        print(f'{effect.getName()} has {word} {affected.getName()}\'s HP by {str(abs(hpAdjustment))}.')
                        print()
                    """ some special attacks have effects that must be executed in between rounds.
                    we do so here"""
                    if effect.getIsExecutableEffect():
                        effectName = effect.getName()
                        indexList = []
                        #formatting the name of the effect to convert to file and class names
                        for i in range(len(effectName)):
                            character = effectName[i]
                            if character == " ":
                                indexList.append(i+1)
                        for i in indexList:
                            effectName = effectName[:i] + effectName[i].upper() + effectName[i+1:]
                            
                        className = effectName.replace(' ','')
                        fileName = className[0].lower() + className[1:]
                        specialAttackClass = getattr(importlib.import_module(fileName), className)
                        specialAttack = specialAttackClass()
                        specialAttack.executeEffect(affected)
                #latent effects are not applied
                else:
                    affected.getLatentEffects().append(effect)

                        

    @staticmethod
    def processRound(combatants):
        for a in Game.cbtActions:
            print()
            Rules.doAction(a, Game.cbtActions, Game.roundCount, Game.specialAttackNamesDictionary)
        
        for c in combatants:
            if c.getHp() == 0:
                Game.defeatedCombatants.append(c)
                print(f'{c.getName()} has been defeated!')
        
        for c in Game.defeatedCombatants:
            if c in combatants:
                combatants.remove(c)
        
        if len(combatants) <= 1:
            return True

        return False


    def displayStatus(combatant):
        print(f'{combatant.getName()}\'s status:')
        if combatant.getHp() == 0:
            print("Defeated")
        else:
            print(f'Health: {combatant.getHp()}')
            print(f'Stamina: {combatant.getStamina()}')

    def displayStatuses(combatants):
        for c in combatants:
            Game.displayStatus(c)
            print()

    def displayFinal(combatants):
        print("------------")
        print("Game over!")
        print("------------")
        print()

        if len(combatants) == 1:
            winner = combatants[0]
            print(f'{winner} is the victor!')
         
        #if all remaining combatants die in the same round, we have a draw
        else:
            print("The battle ended in a draw!")

    @staticmethod
    def collectRoundActions(combatants):
        while True:
            Game.cbtActions.clear()
            for c in combatants:
                if not any(e.getIsIncapacitated() for e in c.getEffects()):
                    Game.getCombatantAction(c, combatants)
                else:
                    print()
                    print(f'{c.getName()} is incapacitated!')
                    print()
            break
    
    @staticmethod
    def getCombatantAction(combatant, combatants):
        print(f'It is {combatant.getName()}\'s turn')
        action = None
        while True:
            actionChoice = Game.getAction(combatant)
            specialAttack = None
            if actionChoice == "Special Attack":
                specialAttack = Game.getSpecialAttack(combatant)
            check = Game.validateAction(combatant, actionChoice, specialAttack)
            if check == False:
                print("You do not have enough stamina to perform that action.")
                continue
            targets = None
            if actionChoice == "Special Attack" or actionChoice == "Attack":
                if actionChoice == "Attack" or (specialAttack != None and specialAttack.getNeedsTarget()):
                    targets = Game.getAttackTargets(combatant, combatants, specialAttack)
            action = ActionInfo(combatant, targets, actionChoice, specialAttack)
            break
        Game.cbtActions.append(action)


    def getAttackTargets(cbt, combatants, specialAttack):
        potentialTargets = Game.getPotentialTargets(cbt, combatants)
        targetChoices = []
        targets = []
        targetNumber = 1
        needsTargetOrder = False
        if specialAttack != None:
            targetNumber = specialAttack.getMaxTargets()
            needsTargetOrder = specialAttack.getNeedsTargetOrder()
        """everyone is automatically a target if the attack takes the same or 
        more targets than are in the game and order does not have to be specified 
        for the special attack. Same if there is only one target left."""
        if (targetNumber >= len(combatants) - 1 and not needsTargetOrder) or len(combatants)==2:
            return potentialTargets

        choiceNumber = 1
        for t in potentialTargets:
            targetChoices.append(TargetInfo(t,choiceNumber))
            choiceNumber += 1
            
        for i in range(targetNumber):
            #players do not have to choose the last target if there is just one left
            if len(targetChoices) == 1:
                lastTarget = Game.getTarget(targetChoices, targetChoices[0].getTargetNumber())
                targets.append(lastTarget)
                break
            else:
                print()
                for t in targetChoices:
                    print(f'{t.getTargetNumber()}. {t.getTarget().getName()}')

                while True:
                    print("Select the number of the combatant you want to attack:")            
                    targetChoice = int(input())
                    print()
                    target = Game.getTarget(targetChoices, targetChoice)
                    if target != None:
                        targets.append(target)
                        break
                    else:
                        print("That is not a valid target. Please enter another number")
        return targets

    def getTarget(targetL, targetC):
        #iterating backwards so that we can remove the target once it is found
        for i in range(len(targetL)-1, -1, -1):
            target = targetL[i]
            if target.getTargetNumber() == targetC:
                targetL.remove(target)
                return target.getTarget()
        return None

    def getPotentialTargets(cbt, combatants):
        potentialTargets = []
        for c in combatants:
            if c != cbt:
                potentialTargets.append(c)
        return potentialTargets
                
    #checks to see if combatant has enough stamina to perform the action
    def validateAction(cbt, actionChoice, specialAttack):
        if actionChoice == "Attack":
            stamCost = Rules.getStamCost(cbt, actionChoice, None)
            if stamCost > cbt.getStamina():
                return False
        elif actionChoice == "Special Attack":
            if specialAttack == None:
                raise "Special attack is None and this shouldn't happen"
            stamCost = Rules.getStamCost(cbt, actionChoice, specialAttack)
            if stamCost > cbt.getStamina():
                return False
        return True 

    @staticmethod
    def loadSpecialAttacks():
        f = open("SpecialAttacks.csv", "r")
        while True:
            line = f.readline()
            if line == '' or line == None:
                break
            line = line.strip('\n')
            values = line.split(",")
            s = SpecialAttack(values[1], int(values[2]), values[3], Utils.parseBoolString(values[4]), Utils.parseBoolString(values[6]), int(values[7]), Utils.parseBoolString(values[8]))
            cbtType = values[0]
            #populating a dictionary of special attacks by combatant class/type
            if cbtType in Game.specialAttacks:
                Game.specialAttacks[cbtType].append(s)
            else:
                Game.specialAttacks[cbtType] = [s]
            #populating dictionary with special attack names and special attack class names
            Game.specialAttackNamesDictionary.add(values[1],values[5])
        f.close()

    def getSpecialAttack(combatant):
        sAttackList = []
        sAttacks = Game.specialAttacks[combatant.getClassName()]
        while True:
            number = 1
            print("Select a special attack by entering its corresponding number:")
            for s in sAttacks:
                sAttackList.append((number, s))
                print(f'{number}. {s.getName()}')
                number += 1
            choice = int(input())
            sAttack = Utils.getElementFromChoice(choice, sAttackList)
            if sAttack != None:
                return sAttack
            print("The action you selected was not valid")
            print()
    
    @staticmethod
    def getOptions():
        global seeEffects
        print("Enter \"Y\" to display combatant effects at the end of each round.")
        #using negatives here so that our unittest has seeEffects as True
        if input() != "Y":
            seeEffects = False


    @staticmethod
    def displayEffects(combatants):
        
        for combatant in combatants:
            effects = combatant.getEffects()
            if len(effects) != 0:
                print()
                print(f'{combatant.getName()}:')

            for effect in effects:
                effectData = Game.getAffectedStat(effect)
                statAffected = effectData[0]
                adjustment = effectData[1]
                string = f'{effect.getName()}- End round: {str(effect.getEndRound())}'
                if statAffected != None:
                    string += f', {statAffected} adjustment: {str(adjustment)}'
                elif effect.getIsIncapacitated() == True:
                    string += f', Incapacitated'
                print(string)

            #latent effects are not in play, but they are present
            for effect in combatant.getLatentEffects():
                print(f'*Inactive* {effect.getName()}- End round: {str(effect.getEndRound())}')


    #returns the stat that an effect adjusts and the adjustment value
    @staticmethod
    def getAffectedStat(effect):
        affectedStat = None
        adjustment = 0

        if effect.getVitalityScoreAdjustment() != 0:
            affectedStat = "Vitality"
            adjustment = effect.getVitalityScoreAdjustment()
        elif effect.getEnduranceScoreAdjustment() != 0:
            affectedStat = "Endurance"
            adjustment = effect.getEnduranceScoreAdjustment()
        elif effect.getStrengthScoreAdjustment() != 0:
            affectedStat = "Strength"
            adjustment = effect.getStrengthScoreAdjustment()
        elif effect.getDexterityScoreAdjustment() != 0:
            affectedStat = "Dexterity"
            adjustment = effect.getDexterityScoreAdjustment()
        elif effect.getIntelligenceScoreAdjustment() != 0:
            affectedStat = "Intelligence"
            adjustment = effect.getIntelligenceScoreAdjustment()
        elif effect.getFaithScoreAdjustment() != 0:
            affectedStat = "Faith"
            adjustment = effect.getFaithScoreAdjustment()

        return (affectedStat, adjustment)

    @staticmethod
    def run():
        Game.loadSpecialAttacks()
        Game.getOptions()
        combatants = Game.createCombatants()
        Game.doBattle(combatants)