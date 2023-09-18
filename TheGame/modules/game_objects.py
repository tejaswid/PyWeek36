import pyglet
from modules import utils


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
        self.type = (
            None  # Specifies the type of the object - player, enemies, bullets etc.
        )
        self.child_objects = []  # List of objects that can be spawned by this object
        self.sim_state = None  # State of the object - useful in a state machine
        self.dead = False  # whether this object has to be removed from screen or not
        self.collision_radius = 0  # circle collider radius
        self.collider_type = None  # "circle" or "polygon"
        self.event_handlers = []  # Tell the game handler about any event handlers

        self.max_health = 100  # maximum health of the object
        self.current_health = self.max_health  # current health of the object
        self.damage = 0  # damage that this object can cause to other objects
        self.damage_taken = 0  # damage that this object has taken from other objects

        self.score = 0  # score that this object gives when it dies
        self.died_by_player = False  # whether this object was killed by the player or not

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
        distance = utils.distance((self.x, self.y), (other_object.x, other_object.y))
        if distance < self.collision_radius + other_object.collision_radius:
            # add a rebound effect to the objects
            no_rebound_list = ["bullet", "powerup"]
            if not (self.type in no_rebound_list or other_object.type in no_rebound_list):
                old_self_x = self.x
                old_self_y = self.y
                old_other_object_x = other_object.x
                old_other_object_y = other_object.y
                rebound_factor = 5
                self.x += (old_self_x - old_other_object_x) * rebound_factor
                self.y += (old_self_y - old_other_object_y) * rebound_factor

                other_object.x += (old_other_object_x - old_self_x) * rebound_factor
                other_object.y += (old_other_object_y - old_self_y) * rebound_factor

            return True
        return False

    def take_damage(self, damage):
        """
        Function to handle damage to this object
        :param damage: damage caused by the other object
        """
        self.damage_taken = damage
        self.current_health -= damage
        if self.current_health <= 0:
            self.dead = True

    def draw_damage_label(self, health_bar_batch):
        # draw damage label
        if self.damage_taken > 0:
            print("drawing damage label")
            damage_label = pyglet.text.Label(
                f"-{self.damage_taken}",
                font_name="Arial",
                font_size=12,
                x=self.x,
                y=self.y + self.height + 50,
                anchor_x="center",
                anchor_y="center",
                color=(255, 0, 0, 255),
                batch=health_bar_batch,  # Use the health_bar_batch for rendering
            )
            self.damage_taken = 0
            return damage_label
        # draw heal label
        if self.damage_taken < 0:
            print("drawing heal label")
            heal_label = pyglet.text.Label(
                f"+{-self.damage_taken}",
                font_name="Arial",
                font_size=12,
                x=self.x,
                y=self.y + self.height + 50,
                anchor_x="center",
                anchor_y="center",
                color=(0, 255, 0, 255),
                batch=health_bar_batch,  # Use the health_bar_batch for rendering
            )
            self.damage_taken = 0
            return heal_label
        return None

    def die(self, dt):
        self.dead = True
