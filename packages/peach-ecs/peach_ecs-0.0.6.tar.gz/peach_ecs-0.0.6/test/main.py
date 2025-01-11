#!./venv/bin/python3
import pecs
import logging
logging.basicConfig(level=logging.DEBUG)
pecs_logger = logging.getLogger("pecs")
pecs_logger.setLevel(logging.DEBUG)

class Ping(pecs.System):
    def run(self):
        for ent, comps in self.world.query("ping"):
            self.logger.info(f"{ent} - {comps}")
            self.world.delete_component(ent, "ping")
            self.world.add_component(ent, pecs.Component("pong"))

class Pong(pecs.System):
    def run(self):
        for ent, comps in self.world.query("pong"):
            self.logger.info(f"{ent} - {comps}")
            self.world.delete_component(ent, "pong")
            self.world.add_component(ent, pecs.Component("ping"))

def main():
    world = pecs.World("Ping-Pong")
    world.add_system (Ping)
    world.add_system (Pong)
    ent = world.create_entity()
    world.add_component(ent, pecs.Component("ping"))
    world.run()
    print (world.__dict__)

if __name__ == "__main__":
    main()
