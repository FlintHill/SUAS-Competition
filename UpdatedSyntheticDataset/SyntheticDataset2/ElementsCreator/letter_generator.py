from abc import ABCMeta, abstractmethod

class LetterGenerator(object):

    __metaclass__ = ABCMeta

    def __init__(self, font_type, font_size, color):
        """
        Construct the RandomLetterGenerator class
        :param font_type: the intended font_type of the letter
        :param font_size: the intended font_size of the letter
        :param color: the intended color of the letter
        :type font_type: a font file
        :type font_size: int
        :type color: (R, G, B, A)
        :type R, G, B, and A: int from 0 to 255
        """
        self.font_type = font_type
        self.font_size = font_size
        self.letter_color = color
        self.letter_ratio = 10000.0 / 6832.0
        self.background_color = (255, 255, 255, 0)
