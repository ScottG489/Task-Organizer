import clicontroller

class UIControllerFactory():
    def __init__(self):
        pass

    def get(self,
            ui_type,
            storage_type,
            **kwargs):
        """Return a user interface instance.

        Arguments:
        ui_type -- name of the desired user interface type
        storage_type -- name of the desired storage type
        kwargs -- keyword arguments specific to each storage type


        Using the given user interface and storage type, create a user
        interface instance that uses the specified storage type with
        the given optional keyword arguments.

        """
        if ui_type == 'cli':
            return clicontroller.CLIController(
                    storage_type,
                    **kwargs)
