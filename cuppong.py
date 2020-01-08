from cup import Cup, Colour
import logging

logger = logging.getLogger(__name__)

class Game(object):
    '''Base object for a cup game.
    '''
    self._running = False
    self._cancelled = False
    self._ball_detection_thread = None

    def __init__(self, cups):
        '''
        '''
        # the _cups field is a dictionary with cups as keys and empty dictionaries as values
        # each game may use the cup dictionary as required
        self._cups = { cup : {} for cup in cups }

    @property
    def cups(self):
        '''Dictionary of cups.
        '''
        return self._cups

    def start(self):
        '''Starts a game. Calling this class initialises a new thread which monitors all cups.
        '''
        if self._running:
            raise RuntimeError('The game is already running.')
        self._cancelled = False
        self._initialise()
        self._ball_detection_thread = threading.Thread(target=self._check_ball_detection, args=(self.cups.keys(),), daemon=True)
        self._ball_detection_thread.start()

    def stop(self):
        '''Cancel the game.
        '''
        self._cancelled = True
        if self._ball_detection_thread:
            self._ball_detection_thread.join()

    def _initialise(self):
        '''Called before the ball detection thread is started. May be used to
        initialise cup colours.
        '''
        pass

    def _ball_detected(self, cup):
        '''Called by the ball detection thread when a ball is detected in a cup.
        Games should implement this function.
        '''
        pass

    def _is_game_over(self, cup):
        '''Called by the ball detection thread to check whether the game is over.
        The thread is stopped when this is true.
        '''
        raise NotImplementedError

    def _check_ball_detection(self, cups):
        self._running = True
        count = 0
        try:
            while not self._cancelled:
                with SMBus(I2C_BUS) as bus:
                    for cup in cups:
                        if cup.check_ball_detected(bus):
                            self._ball_detected(cup)

                        # time delay required for I2C connection
                        time.sleep(0.01)

                if self._is_game_over():
                    break
        finally:
            self._running = False

class ClassicBeerPong(Game):
    '''The classic beer pong game, where a player must land balls in the cups.
    '''

    def __init__(self, colour, cups):
        super().__init__(self, cups)
        self._colour = colour

    def _initialise(self):
        logger.debug('Initialising ClassicBeerPong')
        for cup, cup_info in self.cups:
            cup.SET_COLOUR(Colour(0, 0, 0))
            cup_info['hit'] = False

    def _ball_detected(self, cup):
        cup_info = self.cups[cup]
        
        if not cup_info['hit']:
            logger.debug('%s hit for first time', cup)
            cup.SET_COLOUR(self._colour)
            cup_info['hit'] = True
        else:
            logger.debug('%s hit', cup)

    def _is_game_over(self):
        return all([cup_info['hit'] for cup, cup_info in self.cups])