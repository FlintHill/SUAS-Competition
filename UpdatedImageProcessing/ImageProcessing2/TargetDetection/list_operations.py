from collections import Counter

class ListOperations(object):

    @staticmethod
    def find_2nd_most_common_element_from_2d_list(two_dimentional_list):
        horizontal_2nd_most_common_list = []

        for index_1 in range(len(two_dimentional_list)):
            horizontal_most_common_value = max(two_dimentional_list[index_1], key=Counter(two_dimentional_list[index_1]).get)

            horizontal_list_without_most_common_value = []

            index_2 = len(two_dimentional_list[index_1]) - 1
            while(index_2 >= 0):
                if (two_dimentional_list[index_1][index_2] != horizontal_most_common_value):
                    horizontal_list_without_most_common_value.append(two_dimentional_list[index_1][index_2])

                index_2 = index_2 - 1

            if (len(horizontal_list_without_most_common_value) > 0):
                horizontal_2nd_most_common_value = max(horizontal_list_without_most_common_value, key=Counter(horizontal_list_without_most_common_value).get)
                horizontal_2nd_most_common_list.append(horizontal_2nd_most_common_value)

        return max(horizontal_2nd_most_common_list, key=Counter(horizontal_2nd_most_common_list).get)
