import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Component:
    def __new__(cls, name, data=None):
        """
        Creates a new component from the provided name and data.
        Components come in three "flavors":
        Tag: A Component with no data
        Component: A Component with data
        Relation: A Component that relates two Components together
        """

        # Create a new class
        obj = super().__new__(type(name, (object, ), {}))

        # Set the attributes for the new object
        setattr(obj, "name", name)

        if isinstance(data, dict):
            for key, value in data.items():
                setattr(obj, key, value)
        elif data is not None:
            setattr(obj, "value", data)

        # Return the new object
        return obj

class ComponentManager:
    def __new__(cls, obj):
        """
        A new instance of a ComponentManager is created for each Component "type"
        ComponentManager class is unique to each World
        """
        # Create map to hold a manager for each Component type
        if not hasattr(cls, "_instances"):
            cls._instances = {}

        # Normalize Component Names
        name = obj
        if not isinstance(obj, str):
            name = obj.__class__.__name__
        name = name.lower()

        # Create new instance of manager, if name is not registered
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            setattr(cls._instances[name], "name", name)

        # Return the manager instance for the component type
        return cls._instances[name]

    def __init__(self, obj):
        # Check if already initialized
        if hasattr(self, "_init"):
            return
        self._init = True

        # Empty map of components indexed by Entity Id
        self._components = {}

    def __del__(self):
        del self.__class__._instances[self.name]

    @classmethod
    def hard_reset(cls):
        """
        TODO: Rename "new", create new "type()", and reset _instances
        Resets the entire class and all instances.
        Used when creating a new World to ensure a unique singleton of the ComponentManager exists
        """
        cls._instances = {}

    # TODO: @classmethod def clone(cls):

    def add(self, ent_id, component):
        """
        Add a component to the manager, registered to an ent_id
        """
        if ent_id in self._components:
            logger.warning(f"Entity {ent_id} already has component {self.name}, nothing added")
            return

        self._components[ent_id] = component

    def get_entities(self):
        """
        Return a list of Entities that have this Component
        """
        return list(self._components.keys())

    def get(self, ent_id):
        """
        Retrieve a component registered to an Entity
        Returns None is no Component is registered
        """
        if ent_id not in self._components:
            logger.warning (f"No Component {self.name} for Entity {ent_id}")
            return None

        return self._components[ent_id]

    def update(self, ent_id, component):
        """
        Update the value of a component for an Entity
        """

        if ent_id not in self._components:
            logger.warning(f"No Component {self.name} to update for Entity {ent_id}")
            return

        self._components[ent_id] = component


    def delete(self, ent_id):
        """
        Remove the Component for an Entity
        """

        if ent_id not in self._components:
            logger.warning(f"No Component {self.name} to delete for Entity {ent_id}")
            return

        del self._components[ent_id]
