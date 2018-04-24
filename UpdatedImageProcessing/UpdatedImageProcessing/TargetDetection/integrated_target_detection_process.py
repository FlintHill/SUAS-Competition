from PIL import Image
from .color_operations import ColorOperations
from .target_detectors import TargetDetectors
from .false_positive_eliminators import FalsePositiveEliminators

class IntegratedTargetDetectionProcess(object):

    @staticmethod
    def run_integrated_target_detection_process(target_map_image_path):
        """
        Detect the targets for one target map using both BlobDetector and
        CannyEdgeContourDetector and return all positives.

        :param target_map_image_path: the path to a target map image

        :type target_map_image_path: an image file such as JPG and PNG

        :return: a positive list
        """
        pil_target_map_image = Image.open(target_map_image_path)
        mean_blurred_target_map_image = ColorOperations.apply_mean_blur(pil_target_map_image, 3)

        #Application of BlobDetector
        positive_list_1 = TargetDetectors(mean_blurred_target_map_image).detect_blobs()

        if (len(positive_list_1) > 15):
            positive_list_1 = FalsePositiveEliminators.eliminate_overrepeated_colors(pil_target_map_image, positive_list_1)

        #Application of CannyEdgeContourDetector
        positive_list_2 = TargetDetectors(mean_blurred_target_map_image).detect_canny_edge_contours()

        if (len(positive_list_2) > 15):
            positive_list_2 = FalsePositiveEliminators.eliminate_overrepeated_colors(pil_target_map_image, positive_list_2)

        #Combine results from the two detectors
        positive_list = positive_list_1 + positive_list_2

        positive_list = FalsePositiveEliminators.eliminate_oversized_target(positive_list)

        positive_list = FalsePositiveEliminators.eliminate_overlapping_targets(positive_list)

        #Enabling combine_close_by_targets sometimes reduce the detection ratio.
        '''
        combine_close_by_targets_result = FalsePositiveEliminators.combine_close_by_targets(positive_list)
        positive_list = combine_close_by_targets_result[0]
        number_of_close_by_targets = combine_close_by_targets_result[1]

        while (number_of_close_by_targets > 0):
            combine_close_by_targets_result = FalsePositiveEliminators.combine_close_by_targets(positive_list)
            positive_list = combine_close_by_targets_result[0]
            number_of_close_by_targets = combine_close_by_targets_result[1]
        '''
        positive_list = FalsePositiveEliminators.eliminate_by_surrounding_color(pil_target_map_image, positive_list)

        return positive_list
