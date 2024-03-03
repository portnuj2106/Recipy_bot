
class GlobalVars:
    def __init__(self):
        self.call_index = 0
        self.data = ""


class Preferences:
    def __init__(self):
        self.isVegetarian = False
        self.cookingTime = False
        self.isHealthy = False


global_vars = GlobalVars()
preferences = Preferences()