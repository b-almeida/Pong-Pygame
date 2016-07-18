class Circle (object):
    def __init__ (self, center, radius):
        '''in - (self, position (center), radius)'''
        self.center = center
        self.radius = radius

    @staticmethod
    def getCircle (rect):
        '''in - (Rect)
        Returns a Circle object of the given Rect.
        out - Circle'''
        return Circle (rect.center, (rect.width + rect.height) / 4)

    def isColliding_player (self, c2):
        '''in - (self, other circle)
        Determines if the 2 circles are in collision.
        out - bool'''
        distance_x = abs (self.center [0] - c2.center [0])
        distance_y = abs (self.center [1] - c2.center [1])
        distance_z = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance_z < (self.radius + c2.radius):
            return True
        return False
