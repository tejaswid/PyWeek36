import math
import pyglet


class GameObject(pyglet.sprite.Sprite):
    """
    A class to define a generic object in the simulation.
    Most objects in the simulation, i.e. robot, obstacles, lights are derived from this class.
    This class itself is derived from the pyglet.sprite.Sprite class
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        """
        super(GameObject, self).__init__(*args, **kwargs)

        # Declaring all the member variables of the class
        self.type = None            # Specifies the type of the object - player, enemies, bullets etc.
        self.child_objects = []     # List of objects that can be spawned by this object
        self.sim_state = None       # State of the object - useful in a state machine
        self.dead = False           # whether this object has to be removed from screen or not
        self.collision_radius = 0   # circle collider radius
        self.collider_type = None   # "circle" or "polygon"
        self.event_handlers = []    # Tell the game handler about any event handlers
        
        self.max_health = 100       # maximum health of the object
        self.current_health = self.max_health   # current health of the object
        self.damage = 10            # damage that this object can cause to other objects

    def update_object(self, dt):
        """
        Virtual update_object function. This is not named update because the Sprite object has a
        function called update
        """
        pass

    def handle_collision_with(self, other_object):
        """
        Virtual function to handle collision with other objects
        :param other_object: the object that this object has collided with
        """
        pass

    def has_collided_with(self, other_object):
        """
        Function to check if this object has collided with another object
        :param other_object: the object that this object has collided with
        :return: True if collision has occurred, False otherwise
        """
        # calculate distance between the centres of the two objects
        distance = math.sqrt((self.x - other_object.x)**2 + (self.y - other_object.y)**2)
        if distance < self.collision_radius + other_object.collision_radius:
            return True
        return False

    def take_damage(self, other_object):
        """
        Function to handle damage to this object
        :param other_object: the object that is causing the damage
        """
        self.current_health -= other_object.damage
        if self.current_health <= 0:
            self.dead = True