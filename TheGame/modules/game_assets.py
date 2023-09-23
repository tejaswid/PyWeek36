import pyglet


class GameAssets(object):
    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(GameAssets, self).__init__(*args, **kwargs)

        self.image_assets = dict()  # dictionary of image assets
        self.sound_assets = dict()  # dictionary of sound assets

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

    def create_sound_asset(self, keyword, file, shouldStream=False):
        """
        Creates an audio asset from the specified file and adds it to the
        dictionary of sound assets using the specified keyword
        :param keyword: Keyword with which to name the asset
        :param file: File from which to create the asset
        :param shouldStream: True if the source should be streamed from disk
                          False if it should be entirely decoded into memory immediately.
        """
        sound_asset = pyglet.resource.media(file, streaming=shouldStream)
        self.sound_assets.update({keyword: sound_asset})


    def load_assets(self):
        pyglet.resource.path = ["resources"]
        pyglet.resource.reindex()

        # load images
        self.create_image_asset("img_player_ship", "images/player_ship.png", True)
        # self.create_image_asset("img_player_ship_with_shield", "images/player_ship_with_shield.png", True)
        self.create_image_asset("img_player_ship_with_shield_s1", "images/player_ship_with_shield_s1.png", True)
        self.create_image_asset("img_player_ship_with_shield_s2", "images/player_ship_with_shield_s2.png", True)
        self.create_image_asset("img_player_ship_with_shield_s3", "images/player_ship_with_shield_s3.png", True)
        self.create_image_asset("img_player_ship_with_shield_s4", "images/player_ship_with_shield_s4.png", True)
        self.create_image_asset("img_player_ship_with_shield_s5", "images/player_ship_with_shield_s5.png", True)
        self.create_image_asset("img_player_ship_flame_s1", "images/ship_flame_1.png", True)
        self.create_image_asset("img_player_ship_flame_s2", "images/ship_flame_2.png", True)
        self.create_image_asset("img_player_ship_long_flame_s1", "images/ship_long_flame_1.png", True)
        self.create_image_asset("img_player_ship_long_flame_s2", "images/ship_long_flame_2.png", True)
        self.create_image_asset("img_bullet", "images/bullet.png", True)
        self.create_image_asset("img_bullet_player", "images/bullet_player.png", True)
        self.create_image_asset("img_bullet_enemy", "images/bullet_enemy.png", True)
        self.create_image_asset("img_bullet_tracer", "images/bullet_tracer.png", True)
        self.create_image_asset("img_enemy", "images/enemy.png", True)
        # self.create_image_asset("img_enemy_seeker", "images/enemy_seeker.png", True)
        self.create_image_asset("img_enemy_seeker_s1", "images/enemy_seeker_s1.png", True)
        self.create_image_asset("img_enemy_seeker_s2", "images/enemy_seeker_s2.png", True)
        self.create_image_asset("img_enemy_seeker_s3", "images/enemy_seeker_s3.png", True)
        # self.create_image_asset("img_enemy_spear", "images/enemy_spear.png", True)
        self.create_image_asset("img_enemy_spear_s1", "images/enemy_spear_s1.png", True)
        self.create_image_asset("img_enemy_spear_s2", "images/enemy_spear_s2.png", True)
        self.create_image_asset("img_enemy_spear_s3", "images/enemy_spear_s3.png", True)
        # self.create_image_asset("img_enemy_shooter", "images/enemy_shooter.png", True)
        self.create_image_asset("img_enemy_shooter_s1", "images/enemy_shooter_s1.png", True)
        self.create_image_asset("img_enemy_shooter_s2", "images/enemy_shooter_s2.png", True)
        self.create_image_asset("img_enemy_shooter_s3", "images/enemy_shooter_s3.png", True)
        self.create_image_asset("img_enemy_shooter_s4", "images/enemy_shooter_s4.png", True)
        self.create_image_asset("img_enemy_shooter_s5", "images/enemy_shooter_s5.png", True)
        self.create_image_asset("img_asteroid", "images/asteroid.png", True)
        self.create_image_asset("img_asteroid_2", "images/asteroid_2.png", True)
        self.create_image_asset("img_powerup", "images/powerup.png", True)
        self.create_image_asset("img_powerup_damage", "images/powerup_damage.png", True)
        self.create_image_asset("img_powerup_speed", "images/powerup_speed.png", True)
        self.create_image_asset("img_powerup_health", "images/powerup_health.png", True)
        self.create_image_asset("img_powerup_shield", "images/powerup_shield.png", True)
        self.create_image_asset("img_bkg_title", "images/screen_title.png", True)
        self.create_image_asset("img_bkg_default", "images/screen_default.png", True)
        self.create_image_asset("img_bkg_game_over", "images/screen_game_over.png", True)
        self.create_image_asset("img_bkg_won", "images/screen_won.png", True)
        self.create_image_asset("img_bkg_instructions", "images/screen_instructions.png", True)
        self.create_image_asset("img_bkg_1_1", "images/bkg_1_1.png", True)
        self.create_image_asset("img_bkg_1_2", "images/bkg_1_2.png", True)
        self.create_image_asset("img_bkg_2_1", "images/Purple_Nebula_06-1024x1024.png", True)
        self.create_image_asset("img_bkg_2_2", "images/Purple_Nebula_07-1024x1024.png", True)
        self.create_image_asset("img_foreground_1", "images/foreground_1.png", True)
        self.create_image_asset("img_foreground_2", "images/foreground_2.png", True)
        self.create_image_asset("img_dark_matter", "images/dark_matter.png", True)
        self.create_image_asset("img_dark_matter_invisible", "images/dark_matter_invisible.png", True)
        self.create_image_asset("img_dark_matter_revealed_1", "images/dark_matter_revealed_1.png", True)
        self.create_image_asset("img_dark_matter_revealed_2", "images/dark_matter_revealed_2.png", True)
        self.create_image_asset("img_dark_matter_revealed_3", "images/dark_matter_revealed_3.png", True)
        # self.create_image_asset("img_boss_1", "images/boss_1.png", True)
        self.create_image_asset("img_boss_1_s1", "images/boss_1_s1.png", True)
        self.create_image_asset("img_boss_1_s2", "images/boss_1_s2.png", True)
        self.create_image_asset("img_boss_1_s3", "images/boss_1_s3.png", True)
        self.create_image_asset("img_boss_1_s4", "images/boss_1_s4.png", True)
        self.create_image_asset("img_boss_1_with_shield_s1", "images/boss_1_with_shield_s1.png", True)
        self.create_image_asset("img_boss_1_with_shield_s2", "images/boss_1_with_shield_s2.png", True)
        self.create_image_asset("img_boss_1_with_shield_s3", "images/boss_1_with_shield_s3.png", True)
        # self.create_image_asset("img_boss_2", "images/boss_2.png", True)
        self.create_image_asset("img_boss_2_s1", "images/boss_2_s1.png", True)
        self.create_image_asset("img_boss_2_s2", "images/boss_2_s2.png", True)
        self.create_image_asset("img_boss_2_with_shield_s1", "images/boss_2_with_shield_s1.png", True)
        self.create_image_asset("img_boss_2_with_shield_s2", "images/boss_2_with_shield_s2.png", True)
        self.create_image_asset("img_boss_3", "images/boss_3.png", True)
        self.create_image_asset("img_boss_with_shield", "images/boss_with_shield.png", True)
        self.create_image_asset("img_boss_shield", "images/boss_shield.png", True)
        self.create_image_asset("img_story", "images/story.png", True)
        
        ## load audio assets
        self.create_sound_asset("snd_default_bkg", "sounds/Dafault_bgm_428858__supervanz__duskwalkin_loop.wav", True)
        self.create_sound_asset("snd_boss_bkg", "sounds/Boss_bgm_198415__divinux__ambientdanger.wav", True)
        self.create_sound_asset("snd_bullet_fire", "sounds/Bullet_fire_697730__sustainededed__small-laser.mp3", True)
        self.create_sound_asset("snd_bullet_hit", "sounds/Bullet_impact_319226__worthahep88__single-rock-hitting-wood.wav", True)
        self.create_sound_asset("snd_explosion", "sounds/Explosion_536548__cascoes__explosion.wav", True)
        self.create_sound_asset("snd_collision", "sounds/", True)
        self.create_sound_asset("snd_asteroid_destroyed", "sounds/Asteroid_explosion_546957__sieuamthanh__nolonduoinuoc1.wav", True)
        self.create_sound_asset("snd_powerup_spawn", "sounds/Powerup_spawn_657938__matrixxx__scifi-popup-warning-notice-or-note.wav", True)
        self.create_sound_asset("snd_powerup_pickup", "sounds/Powerup_pickup_523649__matrixxx__powerup-07.wav", True)
        self.create_sound_asset("snd_win", "sounds/win_341984__unadamlar__winning.wav", True)
        self.create_sound_asset("snd_gameover", "sounds/gameover.wav", True)
        self.create_sound_asset("snd_darkmatter_collide", "sounds/Hit_Darkmatter_455215__matrixxx__cartoon-stunned-02.wav", True)
