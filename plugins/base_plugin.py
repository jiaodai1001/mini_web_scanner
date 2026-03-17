class BasePlugin:

    name = "BasePlugin"

    def __init__(self):
        pass

    def run(self, target, urls):
        """
        Each plugin must implement this method
        """
        raise NotImplementedError("Plugin must implement run()")