import random, abc, unittest
from rules import Rules
from enums import Attribute
import constants

class Combatant(metaclass = abc.ABCMeta):
    #class variable for types of moves every combatant can make
    actions = ["Attack", "Special Attack", "Block", "Rest"]
    #universal constant that is added to attack rolls
    toHit = constants.TOHIT

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.effects = []
        #latent effects are present on the combatant but not currently active
        self.latentEffects = []
        self.points = 20
        #stats
        self.vitality = self.bVitality
        self.endurance = self.bEndurance
        self.strength = self.bStrength
        self.dexterity = self.bDexterity
        self.intelligence = self.bIntelligence
        self.faith = self.bFaith
        #temporary stat modifiers
        self.tVitality = 0
        self.tEndurance = 0
        self.tStrength = 0
        self.tDexterity= 0
        self.tIntelligence = 0
        self.tFaith = 0
        
        
    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError

    def getClassName(self):
        return self.__class__.__name__
        
    def getName(self):
        return self.name

    def getHp(self):
        return self.hp

    def setHp(self, hp):
        if hp < 0:
            self.hp = 0
        #players may not exceed their initial xp when healing
        elif hp > self.iHp:
            self.hp = self.iHp
        else:
            self.hp = hp

    @abc.abstractmethod
    def getPhysDefense(self):
        raise NotImplementedError

    @abc.abstractmethod
    def getMagDefense(self):
        raise NotImplementedError
    
    #points for stat allocation upon character creation
    def getPoints(self):
        return self.points
    
    def setPoints(self, value):
        self.points = value
    
    #adjusted stats include temporary modifiers
    def getVitality(self):
        return self.vitality
    
    def getAdjustedVitality(self):
        aVitality = self.vitality + self.tVitality
        if aVitality < 0:
            return 0
        return aVitality

    def setVitality(self, value):
        self.vitality = value

    def getEndurance(self):
        return self.endurance

    def getAdjustedEndurance(self):
        aEndurance = self.endurance + self.tEndurance
        if aEndurance < 0:
            return 0
        return aEndurance

    def setEndurance(self, value):
        self.endurance = value
    
    def getStrength(self):
        return self.strength

    def getAdjustedStrength(self):
        aStrength = self.strength + self.tStrength
        if aStrength < 0:
            return 0
        return aStrength

    def setStrength(self, value):
        self.strength = value

    def getDexterity(self):
        return self.dexterity

    def getAdjustedDexterity(self):
        aDexterity = self.dexterity + self.tDexterity
        if aDexterity < 0:
            return 0
        return aDexterity

    def setDexterity(self, value):
        self.dexterity = value

    def getIntelligence(self):
        return self.intelligence

    def getAdjustedIntelligence(self):
        aIntelligence = self.intelligence + self.tIntelligence
        if aIntelligence < 0:
            return 0
        return aIntelligence

    def setIntelligence(self, value):
        self.intelligence = value

    def getFaith(self):
        return self.faith

    def getAdjustedFaith(self):
        aFaith = self.faith + self.tFaith
        if aFaith < 0:
            return 0
        return aFaith

    def setFaith(self, value):
        self.faith = value


    #temporary stats are adjustments applied to normal stats to get adjusted stats
    def getTemporaryVitality(self):
        return self.tVitality

    def setTemporaryVitality(self, value):
        self.tVitality = value

    def getTemporaryEndurance(self):
        return self.tEndurance

    def setTemporaryEndurance(self, value):
        self.tEndurance = value
    
    def getTemporaryStrength(self):
        return self.tStrength

    def setTemporaryStrength(self, value):
        self.tStrength = value

    def getTemporaryDexterity(self):
        return self.tDexterity

    def setTemporaryDexterity(self, value):
        self.tDexterity = value

    def getTemporaryIntelligence(self):
        return self.tIntelligence

    def setTemporaryIntelligence(self, value):
        self.tIntelligence = value

    def getTemporaryFaith(self):
        return self.tFaith

    def setTemporaryFaith(self, value):
        self.tFaith = value
    
    def getStamina(self):
        return self.stamina

    #players may not exceed the stamina they started the game with
    def setStamina(self, stamina):
        if stamina > self.iStamina:
            self.stamina = self.iStamina
        else:
            self.stamina = stamina
    
    def getEffects(self):
        return self.effects

    def getLatentEffects(self):
        return self.latentEffects
    
    @abc.abstractmethod
    def getDmg(self):
        raise NotImplementedError

    def getStamCost(self):
        return self.stamCost

    #uses method pointers to apply points to a stat
    def applyPoints(self, attribute, amount):
        baseValue = 0
        if attribute == Attribute.VITALITY:
            aptr = self.setVitality
            baseValue = self.vitality
        elif attribute == Attribute.ENDURANCE:
             aptr = self.setEndurance
             baseValue = self.endurance
        elif attribute == Attribute.STRENGTH:
             aptr = self.setStrength
             baseValue = self.strength
        elif attribute == Attribute.DEXTERITY:
             aptr = self.setDexterity
             baseValue = self.dexterity
        elif attribute == Attribute.INTELLIGENCE:
             aptr = self.setIntelligence
             baseValue = self.intelligence
        elif attribute == Attribute.FAITH:
             aptr = self.setFaith
             baseValue = self.faith
        #the value of any one attribute/stat may not exceed 30
        if baseValue + amount <= 30:
            aptr(baseValue + amount)
            self.points -= amount
            return True
        else:
            return False

class Warrior(Combatant):
    def __init__(self, id, name):
        self.stamCost = 10
        #base stats
        self.bVitality = 13
        self.bEndurance = 12
        self.bStrength = 14
        self.bDexterity = 5
        self.bIntelligence = 3
        self.bFaith = 3
        super().__init__(id, name)
        self.hp = constants.WARRIORHP + self.vitality
        self.stamina = constants.WARRIORSTAMINA + self.endurance
        #regenerated hp and stamina may not exceed initial values
        self.iHp = self.hp
        self.iStamina = self.stamina

        

    def __repr__(self):
        return f'{self.name} the Warrior'

    def getDmg(self):
        return random.randint(1,12)
   
    def getPhysDefense(self):
        physDefense = constants.WARRIORPHYSDEFENSE + Rules.getModifier(self.getAdjustedDexterity())
        return physDefense

    def getMagDefense(self):
        magDefense = constants.WARRIORMAGDEFENSE + Rules.getModifier(self.getAdjustedIntelligence())
        return magDefense

class Mage(Combatant):
    def __init__(self, id, name):
        self.stamCost = 8
        self.bVitality = 8
        self.bEndurance = 10
        self.bStrength = 6
        self.bDexterity = 8
        self.bIntelligence = 15
        self.bFaith = 3
        super().__init__(id, name)
        self.hp = constants.MAGEHP + self.vitality
        self.stamina = constants.MAGESTAMINA + self.endurance
        self.iHp = self.hp
        self.iStamina = self.stamina
        
    
    def __repr__(self):
        return f'{self.name} the Mage'
    
    def getDmg(self):
        return random.randint(1,4)
   
    def getPhysDefense(self):
        physDefense = constants.MAGEPHYSDEFENSE + Rules.getModifier(self.getAdjustedDexterity())
        return physDefense

    def getMagDefense(self):
        magDefense = constants.MAGEMAGDEFENSE + Rules.getModifier(self.getAdjustedIntelligence())
        return magDefense

class Rogue(Combatant):
    def __init__(self, id, name):
        self.stamCost = 8
        self.bVitality = 10
        self.bEndurance = 9
        self.bStrength = 8
        self.bDexterity = 14
        self.bIntelligence = 7
        self.bFaith = 2
        super().__init__(id, name)
        self.hp = constants.ROGUEHP + self.vitality
        self.stamina = constants.ROGUESTAMINA + self.endurance
        self.iHp = self.hp
        self.iStamina = self.stamina
        
    
    def __repr__(self):
        return f'{self.name} the Rogue'
    
    def getDmg(self):
        return random.randint(1,6)
   
    def getPhysDefense(self):
        physDefense = constants.ROGUEPHYSDEFENSE + Rules.getModifier(self.getAdjustedDexterity())
        return physDefense

    def getMagDefense(self):
        magDefense = constants.ROGUEMAGDEFENSE + Rules.getModifier(self.getAdjustedIntelligence())
        return magDefense

    



    