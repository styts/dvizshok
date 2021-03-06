
import os
import glob
import pygame
import sys


def resource_path(relative):
    """Used by pyInstaller.
    Correct path prefix when running as frozen app/exe"""

    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS  # production
    else:
        basedir = os.path.join(os.getcwd())  # dev

    #print basedir

    return os.path.join(
        basedir,
        relative
    )


class ResourceManager():
    LOCATION_SPRITES = resource_path("data/sprites")
    LOCATION_SOUNDS = resource_path("data/sounds")
    LOCATION_LEVELS = resource_path("data/levels")

    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._sounds = {}
        self._levels = []
        self._fonts = {}
        self._load_all()

    def _load_all(self):

        ## load sprites
        ext = ".png"
        for fn in glob.glob(ResourceManager.LOCATION_SPRITES + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = {}
            self._surfaces[bn]["default"] = surf

        try:
            import pygame.mixer as mixer
        except ImportError:
            import android.mixer as mixer

        ## load sfx
        ext = ".wav"
        for fn in glob.glob(ResourceManager.LOCATION_SOUNDS + "/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            sound = mixer.Sound(fn)
            self._sounds[bn] = sound

    def fill_me(self, surf, color, alpha_decr):
        s = surf.copy()
        s.fill(color, None, pygame.BLEND_RGBA_MULT)

        sprite = s
        for a in xrange(sprite.get_width()):
            for b in xrange(sprite.get_height()):
                c = sprite.get_at((a, b))
                s = (c.r, c.g, c.b, max(0, c.a - alpha_decr)
                    if c.r or c.g or c.b else 0)
                sprite.set_at((a, b), s)

        return sprite

    def get_surface(self, name, color=None, alpha_decr=0):
        color_str = "%s-%s" % (color, alpha_decr)
        if name not in self._surfaces.keys():
            return None

        if color:
            if color_str not in self._surfaces[name].keys():
                self._surfaces[name][color_str] = self.fill_me(
                    self._surfaces[name]['default'], color, alpha_decr)
            return self._surfaces[name][color_str]
        else:
            return self._surfaces[name]["default"]

    def get_sound(self, name):
        return self._sounds[name]

    def load_font(self, name, size):
        font = pygame.font.Font(resource_path(os.path.join('data', 'fonts', '%s.ttf' % name)), size)
        self._fonts["%s_%s" % (name, size)] = font

    def get_font(self, name):
        return self._fonts[name]

    def get_levels(self):
        return self._levels
