import pygame
import os

from resman import ResourceManager
from audman import AudioManager

on_android = False
try:
    import android
    on_android = True
except ImportError:
    pass


class App():
    FULLSCREEN = True

    def __init__(self, title, resolutions=[(1024, 768), (960, 640), (854, 480), (800, 480), (640, 480), (480, 320)], appstates=[], fps=30):
        global on_android

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()

        vidinfo = pygame.display.Info()

        for r in resolutions:
            if r[0] <= vidinfo.current_w and r[1] <= vidinfo.current_h:
                break

        self.screen_w, self.screen_h = r

        if App.FULLSCREEN:
            pygame.display.set_mode((vidinfo.current_w, vidinfo.current_h),  pygame.FULLSCREEN)
            self.fullscreen = pygame.display.get_surface()
            self.screen = pygame.Surface((self.screen_w, self.screen_h))
            self.x = 0
            self.y = 0
        else:
            pygame.display.set_mode((self.screen_w, self.screen_h))
            self.screen = pygame.display.get_surface()

        pygame.display.set_caption(title)

        self.is_running = True  # used to trigger exit by ESC

        # Map the back button to the escape key.
        if on_android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        self.clock = pygame.time.Clock()
        self._fps = fps

        self.resman = ResourceManager(self)
        self.audioman = AudioManager(self)

        self._dirty_rects = []
        self.init()

        self._appstates = []
        for asc in appstates:
            s = asc(self)
            self._appstates.append(s)
        self.appstate = self._appstates[0]

    def init(self):
        pass

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
        global on_android
        self.clock.tick(self._fps)

        # Android-specific:
        if on_android:
            if android.check_pause():
                android.wait_for_resume()

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
            try:  # hack to enable fullscreen coordinates
                pos_x, pos_y = event.pos
                event.pos = tuple([pos_x - self.x, pos_y - self.y])
            except:
                print "silly event:", event
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

        #pygame.display.update(self._dirty_rects)
        self.x = self.fullscreen.get_width() / 2 - self.screen.get_width() / 2
        self.y = self.fullscreen.get_height() / 2 - self.screen.get_height() / 2
        self.fullscreen.blit(self.screen, (self.x, self.y))
        #pygame.display.flip()
        pygame.display.update(self._dirty_rects)
        #print self._dirty_rects
        pygame.event.pump()
