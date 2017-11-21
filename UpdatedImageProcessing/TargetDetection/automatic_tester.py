import json

class AutomaticTester(object):

    @staticmethod
    def run_automatic_tester(positive_list, path_to_answer_sheet):
        """
        Compare the positive_list with the answers of the a target map and
        return the list of the true and false positives.

        :param positive_list: the list holding the information of the blobs.
        :param path_to_answer_sheet: the path to the json file of the answers of
                                     the background image under detection.

        :type positive_list: a list of lists containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        :type path_to_answer_sheet: a json file
        """
        answer_sheet = json.load(open(path_to_answer_sheet))

        true_positive_list = []
        false_positive_list = []
        true_positive_found = False

        for index_1 in range(len(positive_list)):
            for index_2 in range(len(answer_sheet["targets"])):
                blob_center_x = positive_list[index_1][0] + (positive_list[index_1][2] / 2)
                blob_center_y = positive_list[index_1][1] + (positive_list[index_1][3] / 2)
                target_center_x = answer_sheet["targets"][index_2]["target_center_coordinates"][0]
                target_center_y = answer_sheet["targets"][index_2]["target_center_coordinates"][1]

                if ((abs(blob_center_x - target_center_x) <= 20) and (abs(blob_center_y - target_center_y) <= 20)):
                    true_positive_list.append(positive_list[index_1])
                    true_positive_found = True
            if (true_positive_found == False):
                false_positive_list.append(positive_list[index_1])

        return [true_positive_list, false_positive_list]
