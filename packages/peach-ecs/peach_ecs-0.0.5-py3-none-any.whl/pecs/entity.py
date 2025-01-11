from component import ComponentManager
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Entity:

    def __new__(cls, id = None):
        """
        Each new Entity is an instance of this class.
        Existing Entities can be accessed by passing the ID in when instantiating.
        This base class is a unique singleton for each World
        """
        # Set defaults
        if not hasattr(cls, "_instances"):
            cls._instances = {}
        if not hasattr(cls, "_next_id"):
            cls._next_id = 0
        if not hasattr(cls, "_id_list"):
            cls._id_list = []

        # Create ID if none is provided
        if id is None:
            id = cls.next_id()

        # Create new instance is none exists
        if id not in cls._instances:
            cls._instances[id] = super().__new__(cls)
            setattr(cls._instances[id], "id", id)
            cls._id_list.append(id)

        # Return the Entity instance
        return cls._instances[id]

    def __init__(self, id = None):
        # Check if already initialized
        if hasattr(self, "_init"):
            return
        self._init = True

        # Default list of components
        self._components = []

    def __del__(self):
        del self.__class__._instances[self.id]

    @classmethod
    def hard_reset(cls):
        # TODO: Rename to "new", create new "type()", reset to defaults
        cls._instances = {}
        cls._next_id = 0
        cls._id_list = []

    # TODO: @classmethod def clone(cls):

    @classmethod
    def next_id(cls):
        # Get the next available id
        retVal = cls._next_id
        # Increment the id counter
        cls._next_id += 1

        # Check if id is already taken
        if retVal in cls._id_list:
            # _next_id is already take, try again
            retVal = cls.next_id()

        return retVal

    def has_component(self, component_name):
        return component_name in self._components

    def add_component(self, component_name):
        # Add component name to list
        self._components.append(component_name)

    def get_components(self):
        """
        Returns a list of all Components that compose this Entity
        """
        return self._components

    def delete_component(self, component_name):
        idx = None
        for i, c in enumerate(self._components):
            if c == component_name:
                idx = i
                break
        del self._components[idx]
