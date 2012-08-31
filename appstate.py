

class AppState(object):
    """The App class takes care of the state transitions between the
    finite state automaton which consists of AppStates
    Those could be: Menu, InGame, LevelComplete, GameOver, HighScores, etc.
    They should all implement the following methods.
    """
    i_wait = 0  # gets decremented every frame if > 0 (used for pausing)
    next_state = None  # holds None or a string with classname of the place 2go
    CLICK_DELAY = 3  # nr of frames (3 ~ 100ms)

    def process(self):
        if self.needs_wait():
            return None

        if self.next_state:
            return self.next_state

    def resume(self, arg):
        """Called form App when being switched to"""
        self.next_state = None

    def _reset_background(self):
        """ draw the background"""
        self.app.screen.blit(self.app.background, (0, 0))
        self.app.dirty(self.app.background.get_rect())

    def needs_wait(self):
        """Handles paused state"""
        if self.i_wait > 0:
            self.i_wait = self.i_wait - 1
            return True
        return False

    def process_input(self, event):
        """Handles the mouse and keyboard"""
        raise NotImplementedError("Should be implemented in AppState subclass")

    def draw(self):
        """Draws stuff on app.screen ( don't forget to call app.dirty(rect))"""
        raise NotImplementedError("Should be implemented in AppState subclass")

    def wait(self, cycles):
        self.i_wait = cycles

    def __init__(self, app):
        self.app = app
