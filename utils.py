class Utils:

    @staticmethod
    def getElementFromChoice(choice, cList):
        for c in cList:
            if c[0] == choice:
                return c[1]
        return None

    # method found at https://codecomments.wordpress.com/2008/04/08/converting-a-string-to-a-boolean-value-in-python/
    @staticmethod
    def parseBoolString(theString): 
        return theString[0].upper()== 'T'

    @staticmethod
    def checkMinValue(value, minimum):
        if value < minimum:
            value = minimum
        return value