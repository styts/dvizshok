import pygame


def make_shadow(surface, alpha=150):
    siz = surface.get_size()
    shadow = pygame.Surface(siz, pygame.SRCALPHA)
    # for each pixel in button glyph
    for a in xrange(siz[0]):
        for b in xrange(siz[1]):
            # set corresponding value in shadow surface to be semi-transparent
            c = surface.get_at((a, b))
            s = c if all(c) == 0 else (0, 0, 0, alpha)
            shadow.set_at((a, b), s)
    return shadow
