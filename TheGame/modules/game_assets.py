import pyglet


class GameAssets(object):
    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(GameAssets, self).__init__(*args, **kwargs)

        self.image_assets = dict()  # dictionary of game assets

        self.load_assets()

    @staticmethod
    def set_anchor_at_centre(image):
        """
        Sets the anchor of an image to its centre
        :param image: Image whose anchor has to be set
        """
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def create_image_asset(self, keyword, file, centered=True):
        """
        Creates an image asset from the specified file and adds it to the
        dictionary of image assets using the specified keyword
        :param keyword: Keyword with which to name the asset
        :param file: File from which to create the asset
        :param centered: Boolean indicating if the anchor has to be centered.
                        Default is True. If False, anchor is at bottom left.
        """
        image_asset = pyglet.resource.image(file)
        if centered:
            self.set_anchor_at_centre(image_asset)
        self.image_assets.update({keyword: image_asset})

    def load_assets(self):
        pyglet.resource.path = ["resources"]
        pyglet.resource.reindex()

        # load images
        self.create_image_asset("img_player_ship", "images/player_ship.png", True)
        self.create_image_asset("img_player_ship_with_shield", "images/player_ship_with_shield.png", True)
        self.create_image_asset("img_bullet", "images/bullet.png", True)
        self.create_image_asset("img_bullet_player", "images/bullet_player.png", True)
        self.create_image_asset("img_bullet_enemy", "images/bullet_enemy.png", True)
        self.create_image_asset("img_bullet_tracer", "images/bullet_tracer.png", True)
        self.create_image_asset("img_enemy", "images/enemy.png", True)
        self.create_image_asset("img_enemy_seeker", "images/enemy_seeker.png", True)
        self.create_image_asset("img_enemy_spear", "images/enemy_spear.png", True)
        self.create_image_asset("img_enemy_shooter", "images/enemy_shooter.png", True)
        self.create_image_asset("img_asteroid", "images/asteroid.png", True)
        self.create_image_asset("img_asteroid_2", "images/asteroid_2.png", True)
        self.create_image_asset("img_powerup", "images/powerup.png", True)
        self.create_image_asset("img_powerup_damage", "images/powerup_damage.png", True)
        self.create_image_asset("img_powerup_speed", "images/powerup_speed.png", True)
        self.create_image_asset("img_powerup_health", "images/powerup_health.png", True)
        self.create_image_asset("img_powerup_shield", "images/powerup_shield.png", True)
        self.create_image_asset("img_bkg_1_1", "images/bkg_1_1.png", True)
        self.create_image_asset("img_bkg_1_2", "images/bkg_1_2.png", True)
        self.create_image_asset("img_bkg_2_1", "images/Purple_Nebula_06-1024x1024.png", True)
        self.create_image_asset("img_bkg_2_2", "images/Purple_Nebula_07-1024x1024.png", True)
        self.create_image_asset("img_dark_matter", "images/dark_matter.png", True)
        self.create_image_asset("img_dark_matter_invisible", "images/dark_matter_invisible.png", True)
        self.create_image_asset("img_dark_matter_revealed_1", "images/dark_matter_revealed_1.png", True)
        self.create_image_asset("img_dark_matter_revealed_2", "images/dark_matter_revealed_2.png", True)
        self.create_image_asset("img_boss_1", "images/boss_1.png", True)
        self.create_image_asset("img_boss_2", "images/boss_2.png", True)
        self.create_image_asset("img_boss_3", "images/boss_3.png", True)
        self.create_image_asset("img_boss_with_shield", "images/boss_with_shield.png", True)
        self.create_image_asset("img_boss_shield", "images/boss_shield.png", True)

