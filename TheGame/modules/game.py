import pyglet

def run():
    print(pyglet.version)

    # create the game window - size is 1000px x 1000px
    window = pyglet.window.Window(1000, 1000, "The game", resizable=False)

    @window.event
    def on_draw():
        window.clear()
    
    pyglet.app.run()