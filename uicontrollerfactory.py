import clicontroller

class UIControllerFactory():
    def __init__(self):
        pass

    def getUI(self,
            ui_type,
            storage_type,
            **kwargs):
        if ui_type == 'cli':
            return clicontroller.CLIController(
                    storage_type,
                    **kwargs)
