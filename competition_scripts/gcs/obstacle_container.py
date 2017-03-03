class ObstacleContainer:

    def __init__(self, stationary_obstacles, moving_obstacles):
        self.stationary_obstacles = stationary_obstacles
        self.moving_obstacles = moving_obstacles

    def get_stationary_obstacles(self):
        """
        Return the stationary obstacles
        """
        return self.stationary_obstacles

    def get_moving_obstacles(self):
        """
        Return the moving obstacles
        """
        return self.moving_obstacles
