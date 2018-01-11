import json

class ResultRecorder(object):

    @staticmethod
    def record_result(positive_list):
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

        data["positive_list"] = []
        for index in range(len(positive_list)):
            data["positive_list"].append(positive_list[index])

        return data
