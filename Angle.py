class Angle (object):
    @staticmethod
    def format (a):
        '''in - (angle)
        Formats angle to a number from 0 to 359.
        out - angle (int/float)'''
        while a < 0:
            a += 360
        while a >= 360:
            a -= 360
        return a

    @staticmethod
    def opposite (a, n):
        '''in - (angle, normal)
        Calculates the opposite (reflected) angle of the given angle.
        out - angle (int/float)'''
        return Angle.format (2 * n - a)        # n - (a - n)
