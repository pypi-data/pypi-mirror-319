import logging
from entity import Entity
from component import ComponentManager
from system import SystemManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class World:
    def __new__(cls, name):
        if not hasattr(cls, "_instances"):
            cls._instances = {}
        name = name.lower()

        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            setattr(cls._instances[name], "name", name)

        return cls._instances[name]

    def __init__(self, name):
        if hasattr(self, "_init"):
            return
        self._init = True

        name = name.lower()

        # Create holding class for all Entities
        self._entities = type(f"Ent_{name}", (Entity, ), {})
        self._entities.hard_reset()

        # Create holding class for all Components
        self._components = type(f"Comp_{name}", (ComponentManager, ), {})
        self._components.hard_reset()

        # Create holding class for all Systems
        self._systems = type(f"Sys_{name}", (SystemManager, ), {})
        self._systems.hard_reset()
        update_event = self._systems("update", self)

    def create_entity(self):
        """
        Create a new Entity for this World
        """

        # Create new instance of an Entity
        ent = self._entities()

        # Return the ID of the new Entity
        return ent.id

    def delete_entity(self, ent_id):
        """
        Delete the Entity from this World
        """
        try:
            self._entities(ent_id).delete()
        except Exception as e:
            logger.error (f"Could not delete Entity: {ent_id}")
            logger.debug(e)

    def add_component(self, ent_id, component):
        """
        Register the Component with the Entity in this World
        """
        try:
            # Extract the component name
            component_name = component.__class__.__name__.lower()
            # Register Component Name with Entity
            self._entities(ent_id).add_component(component_name)
            # Save instance of the Component
            self._components(component_name).add(ent_id, component)
        except Exception as e:
            logger.error (f"Could not add {component_name} to Entity {ent_id}")
            logger.debug (e)

    def delete_component(self, ent_id, component):
        """
        Remove the Component from the Entity
        """
        try:
            self._entities(ent_id).delete_component(component)
            self._components(component).delete(ent_id)
        except Exception as e:
            logger.error (f"Failed to delete {component} from {ent_id}")
            logger.debug (e)

    def get_all_components(self, ent_id):
        """
        Retrieve all Components for this specific Entity
        """
        retVal = {"id": ent_id}
        for comp_name in self._entities(ent_id).get_all_components():
            retVal[comp_name] = self._components(comp_name).get(ent_id)
        return retVal

    def add_system(self, system, event="update"):
        # Register system with event
        self._systems(event).add(system)

        # Check is system has world to query
        if self._systems(event)._world is None:
            self._systems(event).register_world(self)

    def remove_system(self, system):
        raise NotImplementedError

    def update(self):
        self._systems("update").run()

    def query(self, components):
        """
        Retrieve all Entities that match the Components listed
        """
        # Normalize input to be a list of component names
        if not isinstance(components, list):
            components = [components]

        retVal = {}
        ent_list = {}
        for comp in components:
            comp = comp.lower()
            if ent_list:
                ent_list &= set(self._components(comp).get_entities())
            else:
                ent_list = set(self._components(comp).get_entities())

        for ent in ent_list:
            retVal[ent] = []
            for comp in components:
                retVal[ent].append(self._components(comp).get(ent))

        return retVal
