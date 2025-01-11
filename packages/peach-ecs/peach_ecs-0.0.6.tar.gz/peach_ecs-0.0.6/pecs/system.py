import logging

class System:
    # Default Priority
    priority = 0

    def __init__(self, world):
        # Include a logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        # Set the world for the system
        self.world = world

    def run (self):
        raise NotImplementedError

class SystemManager:
    def __new__(cls, name, world = None):
        if not hasattr(cls, "_instances"):
            cls._instances = {}

        name = name.lower()

        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name].name = name

        return cls._instances[name]

    def __init__(self, name, world = None):
        if hasattr(self, "_init"):
            return
        self._init = True

        # Include a logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        # Register with world if one is provided
        if world is not None and not hasattr(self, "_world"):
            self._world = world
        else:
            self._world = None
            self.logger.warning("No world detected")

        self._systems = []

    @classmethod
    def hard_reset(cls):
        # TODO: Rename "new", create new "type()", reset defaults
        cls._instances = {}

    # TODO: @classmethod def clone(cls):

    def register_world(self, world):
        self._world = world

    def add(self, system):
        # Check if subclass
        if not issubclass(system, System):
            self.logger.error(f"Invalid Base Class: system.__base__")

        self._systems.append(system(self._world))
        # TODO: Sort by priority

    def run(self):
        for sys in self._systems:
            try:
                sys.run()
            except Exception as e:
                self.logger.error(f"Failed to run {sys.__class__.__name__}")
                self.logger.debug(e)
