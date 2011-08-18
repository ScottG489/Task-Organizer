import clicontroller

class UIControllerFactory():
    def __init__(self):
        pass

    def getUI(self,
            ui_type,
            storage_type,
            task_filename='taskfile',
            key_filename='keyfile'):
        if ui_type == 'cli':
            return clicontroller.CLIController(
                    storage_type,
                    task_filename=task_filename,
                    key_filename=key_filename)
