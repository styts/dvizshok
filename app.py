import pygame
import os

from resman import ResourceManager
from audman import AudioManager


class App():
    def __init__(self, title, resolution=(1024, 768), appstates=[]):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        self.screen_w, self.screen_h = resolution
        pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption(title)
        self.screen = pygame.display.get_surface()
        self.is_running = True  # used to trigger exit by ESC

        self.clock = pygame.time.Clock()

        self.resman = ResourceManager(self)
        self.audioman = AudioManager(self)

        self._appstates = []
        for asc in appstates:
            s = asc(self)
            self._appstates.append(s)
        self.appstate = self._appstates[0]

    def run(self):
        ## Main Loop
        while self.is_running:
            self.process()
        pygame.quit()  # cleanup finally

    def _get_appstate(self, s):
        for astate in self._appstates:
            if astate.__class__.__name__ == s:
                return astate

    def dirty(self, r):
        """AppStates call this when having drawed on app.screen somewhere"""
        if r not in self._dirty_rects:
            self._dirty_rects.append(r)

    def process(self):
        self.clock.tick(30)

        self._dirty_rects = []

        if not self.appstate:
            raise Exception("AppState is None")

        p = self.appstate.process()
        if p:
            next_state, state_arg = p
            if next_state:
                if next_state == "GoodBye":
                    self.is_running = False
                else:
                    # appstate wants to change!
                    self.appstate = self._get_appstate(next_state)
                    self.appstate.resume(state_arg)

        events = pygame.event.get()
        for event in events:
            p = self.appstate.process_input(event)

            # ESC quits app
            if event.type == pygame.QUIT:
                self.is_running = False

        ## DRAW
        self.appstate.draw()

        # write fps
        if "font" in self.__dict__:
            fps_surf = self.font.render("FPS: %2.2f" % self.clock.get_fps(),
                False, (255, 255, 255), (0, 0, 0))
            self.dirty(self.screen.blit(fps_surf, (0, 0)))

        pygame.display.update(self._dirty_rects)
        pygame.event.pump()
