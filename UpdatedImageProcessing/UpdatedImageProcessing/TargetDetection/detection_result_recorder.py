import json

class DetectionResultRecorder(object):

    @staticmethod
    def record_detection_result(positive_list):
        """
        Return the result of target detection.

        :param positive_list: the list holding the information of the
                              detected targets

        :type positive_list: a list of four-tuples containing four elements
                             for each target: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        data = {}

        data["image_processing_results"] = []
        for index in range(len(positive_list)):
            data["image_processing_results"].append({
                "target_index": {},
                "target_location": (positive_list[index][0], positive_list[index][1], positive_list[index][2], positive_list[index][3]),
                "target_shape_type": {},
                "target_shape_color": {},
                "target_letter_color": {}
            })

        return data
