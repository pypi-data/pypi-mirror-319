# Peach's Entity Component System (PECS)

An Entity-Component-System (ECS) Library.

# Entity

Don't think of this as an object in the traditional sense like in Object Oriented Design. An ECS pattern is a Data Oriented Design pattern. An `Entity` is just an identifier, think of it like a key in a map or row number in a database table.

```python
ent = world.create_entity()
```

# Component

This is the actual data associated with an `Entity`. It can take any shape or form that you wish. Typically it is kept as light as possible, think basic types (int, float, string, etc) as opposed to classes with multiple attributes. Although, it can, and does, make sense to group common data together into one class and use that as the component. For example the Position of an Entity has three elements, the X, Y, and Z coordinates. This would not make sense to keep as three different components since almost all operations on Position are going to need all three coordinates. Same for Color of an Entity, it could include Red, Green, Blue, and Alpha.

Components come in three different "flavors": Tag, Component, Relationship. All three of these "flavors" are still a Component and are all treated exactly the same. In fact, you'll never really notice the difference between them as they are being used.

## Tag

This is the simplest form, it has no data except its own existance. Think of a situation where you would normally use a boolean flag to indicate something. The existence of a Tag in an Entity indicates the flag is set to True. Having Tags is useful for setting up lightweight queries for Entities.

So instead of code like this:
```python
for item in all_items:
  if item.is_valid:
    do_something(item)
```
You would have something like this:
```python
for ent, comps in world.query(["item", "is_valid"]):
  do_something(comps[0])
```

More efficient since all data being processed is contiguous and homogonous and less branching means less bugs.

## Component

This is a basic Component in the traditional sense, it is a class that holds some data. Typically this is kept as light as possible

## Relationship

This is the most powerful form of Component since it relates one piece of data to another. The most obvious use for this is graphs. It is also dangerous as it can lead to a "back-slide" into OOP and other programming paradigms.

# System

This is the part of the design pattern that acts on the components.

When a `System` is added to a `World` an instance of the `System` is created and injected with the instance of the `World` that it belongs to.  This allows the `System` to manipulate and query the `World` in anyway needed. Including adding/removing other `Systems` or itself as well as `Entities` and `Components`. 

```python
class Ping(System):
  def run(self):
    for ent, comps in self.world.query("ping"):
      print (ent, comps)
      sleep(1)
      self.world.remove_component(ent, "ping")
      self.world.add_component(ent, "pong")

world.add_system(Ping)  
```

`Systems` are added to a `World` and subscribed to a `run` event by default if no event is provided. If another event is provided then the `System` is subscribed to that event. `Systems` can subscribe to multiple events. The `run` event is special in that it is continuously run in a loop once the call world.start() is made. Systems can also subscribe to Components. There are three types of events for every `Component`: `on_create`, `on_update`, and `on_delete`. Intuitively, when a `Component` is created, updated, or deleted the corresponding event is triggered and the corresponding function call is made to any `System` that is subscribed to that `Component`.

In the following example the Ping system is subscribed to the Pong component. When a new Pong component is created a call to Ping.create() is made, passing in the newly created Pong component and the entity that it comprises. If the Ping system had defined an update() function it would also be called whenever a Pong component is updated. Likewise for delete().

```python
class Ping(System):
  def create(self, ent, component):
    verify(component)

world.add_system(Ping, "ping")
```

`Systems` have four core functions that can be overwritten: `create`, `update`, `delete`, `run`. Each function corresponds to a subscriptable event. The `run` function is exclusively for the `run` event. This is continuously looped over from the time the world is started until it is stopped. It is possible to have a World that is executing without ever calling start(). Systems can subscribe to Component driven events. Each function is executed for the corresponding component event type. In this way a single System can behave differently depending on the type of event 

## Create
Useful for verification checks and other initialization tasks that need to be run after a component is created. When a System subscribes to an `_on_create` event for a component, this is the function that is called and the component

## Update

## Delete

## Run

# World

This is where all interaction to the ECS framework actually takes place. This ECS implementation maintains the concept of `Worlds` and allows multiple of them that can coexist with each other and even run simultaneously. `Worlds` are built prior to anything else happening, they can also be changed dynamically. The real defining thing about `Worlds` are `Systems`, as they are the behaviours of the `World` that act on the `Components` that make up the `Entities`.

`Worlds` can be cloned, this is ideal for creating reusable templates with a set of `Systems`. Be careful when cloning as the entirety of the `World` in its current state will be cloned over, this includes all `Entities`, `Components`, and `Systems`. Since `Systems` run asyncronously there is no real way to determine the state of the `World`. It is recommended to only load template `Worlds` with `Systems` and nothing else.

```python
world_template = World("main_template")
world_template.add_system(Ping)
world_template.add_system(Pong)

world_1 = world_template.clone()
```

# Ping-Pong Example
```python
class Ping(System):
  def run(self):
    for ent, comps in self.world.query("ping"):
      print (ent, comps)
      sleep(1)
      self.world.remove_component(ent, "ping")
      self.world.add_component(ent, "pong")

class Pong(System):
  def run(self):
    for ent, comps in self.world.query("pong"):
      print (ent, comps)
      sleep(1)
      self.world.remove_component(ent, "pong")
      self.world.add_component(ent, "ping")

world_1 = World("main")
world_1.add_system(Ping)
world_1.add_system(Pong)
world_1.start()

ent_1 = world_1.create_entity()
world_1.add_component(ent_1, Component("ping")
```

# Getting started

## Installation
`pip install reactives`

## Support
I don't get paid for this and it is just a fun experiment so it is provided as-is.

## Roadmap
What will we think of next?

## Contributing
This is just a fun experiment built for my own exploration, education, and entertainment so no contributions are accepted at this time.
I am open to hearing about additional features, improvements, etc..

## Authors and acknowledgment
Me, myself, and I

## License
Beerware

## Project status
Experimental
