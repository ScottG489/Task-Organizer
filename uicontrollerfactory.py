import clicontroller

class UIControllerFactory():
    def __init__(self):
        pass

    def getUI(self):
        return clicontroller.CLIController()
