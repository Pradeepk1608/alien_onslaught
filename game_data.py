class GameData():
    # Track the data of the game

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = True
        self.reset_stats()

        # start the game n inactive state
        self.game_active = False

        # high should never be reset
        self.high_score = 0
    def reset_stats(self):
        # reseting the stats that can change during the game
        self.ship_remain = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0
        
        