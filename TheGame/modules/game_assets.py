import pyglet


class GameAssets(object):

    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(GameAssets, self).__init__(*args, **kwargs)

        self.image_assets = dict()        # dictionary of game assets

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
        pyglet.resource.path = ['resources']
        pyglet.resource.reindex()

        # load images
        self.create_image_asset("img_robot", "images/player_ship.png", True)
        
        