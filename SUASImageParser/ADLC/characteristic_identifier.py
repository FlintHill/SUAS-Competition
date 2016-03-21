from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors

import cv2
import numpy as np


class CharacteristicIdentifier:
    """
    Identify target characteristics
    """

    def __init__(self, **kwargs):
        pass

    def identify_characteristics(self, target):
        """
        Identifies the characteristics of the target "target" and returns
        them as a dictionary object
        """
        # My thoughts so far to accomplish this is to break the problem down
        #   into the following tasks:
        #   1) Segmentation
        #   2) OCR
        #   3) Pixhawk log parse to gather data about
        #       3a) GPS
        #       3b) Heading
        # I'm not really sure how to implement this process, which is why I am
        #   leaving it in this comment as a "stub" which needs to be resolved.

        # Returning the characteristics for each target
        return {}

    def segment(self, target):
        """
        Separate different important aspects of the image out. This is
        to extract the letter within the image
        """
        # @TODO: Implement segmentation here
        
        return target

    def OCR(self, target):
        """
        Use OCR to identify the character within the image "target"
        """
        # @TODO: Implement OCR here

        return ""