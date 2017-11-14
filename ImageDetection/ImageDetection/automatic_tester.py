import json

class AutomaticTester(object):

    def __init__(self, positive_list, path_to_answer_sheet):
        self.positive_list = positive_list
        self.answer_sheet = json.load(open(path_to_answer_sheet))

    def run_automatic_tester(self):
        true_positive_list = []
        false_positive_list = []
        true_positive_found = False

        for index_1 in range(len(self.positive_list)):
            for index_2 in range(len(self.answer_sheet["targets"])):
                blob_center_x = self.positive_list[index_1][0] + (self.positive_list[index_1][2] / 2)
                blob_center_y = self.positive_list[index_1][1] + (self.positive_list[index_1][3] / 2)
                target_center_x = self.answer_sheet["targets"][index_2]["target_center_coordinates"][0]
                target_center_y = self.answer_sheet["targets"][index_2]["target_center_coordinates"][1]

                if ((abs(blob_center_x - target_center_x) <= 10) and (abs(blob_center_y - target_center_y) <= 10)):
                    true_positive_list.append(self.positive_list[index_1])
                    true_positive_found = True
            if (true_positive_found == False):
                false_positive_list.append(self.positive_list[index_1])

        print "True positives: "
        if (len(true_positive_list) == 0):
            print "None"
        else:
            for index in range(len(true_positive_list)):
                print true_positive_list[index]
            print "\nNumber of true positives: " + str(len(true_positive_list))

        print "\nFalse positives: "
        if (len(false_positive_list) == 0):
            print "None"
        else:
            for index in range(len(false_positive_list)):
                print false_positive_list[index]
            print "\nNumber of false positives: " + str(len(false_positive_list))




    #print data["targets"][-2]["target_center_coordinates"]
    #print len(data["targets"][-2]["target_center_coordinates"])
