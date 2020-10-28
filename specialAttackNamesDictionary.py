#holds a dictionary in which keys are display names and values are class names for all special attacks
class SpecialAttackNamesDictionary:
    def __init__(self):
        self.dictionary = {}
    def add(self, displayName, className):
        if displayName not in self.dictionary.keys():
            self.dictionary[displayName] = className
        else:
            raise "That special attack has already been added"
    
    def getClassName(self, key):
        return self.dictionary[key]