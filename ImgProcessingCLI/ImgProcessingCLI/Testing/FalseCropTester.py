import EigenFit.Load.FileFunctions as FileFunctions
import os
from PIL import Image
import random
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
import numpy
from math import log

class FalseCropTester(object):
    MIN_CROP_SIZE = 40
    MAX_CROP_SIZE = 200

    def __init__(self, base_path, num_images, target_extension, false_positives_extension):
        self.base_path = base_path
        self.num_images = num_images
        self.target_extension = target_extension
        self.false_positives_extension = false_positives_extension
        self.init_sets()


    def init_sets(self):
        targets_path = self.base_path + "/Targets"
        false_positives_path = self.base_path + "/False Positives"

        targets_names = os.listdir(targets_path)
        false_positives_names = os.listdir(false_positives_path)

        FileFunctions.remove_names_without_extension(targets_names, self.target_extension)
        FileFunctions.remove_names_without_extension(false_positives_names, self.false_positives_extension)

        self.target_imgs = []
        for i in range(0, self.num_images):
            self.target_imgs.append(Image.open(targets_path + "/" + targets_names[i]).convert('RGB'))

        uncropped_false_positive_imgs = []
        for i in range(0, 5):
            uncropped_false_positive_imgs.append(Image.open(false_positives_path + "/" + false_positives_names[i]))

        self.cropped_false_positive_imgs = []
        for i in range(0 , self.num_images):
            pic_index = random.randint(0, len(uncropped_false_positive_imgs)-1)
            big_pic = uncropped_false_positive_imgs[pic_index]

            base_x = random.randint(0, big_pic.size[0]-FalseCropTester.MAX_CROP_SIZE)
            base_y = random.randint(0, big_pic.size[1]-FalseCropTester.MAX_CROP_SIZE)
            width = random.randint(FalseCropTester.MIN_CROP_SIZE, FalseCropTester.MAX_CROP_SIZE)
            self.cropped_false_positive_imgs.append(big_pic.crop((base_x, base_y, base_x + width, base_y + width)))


    def run_imgs(self):
        num_false_negatives = 0
        for i in range(0, len(self.target_imgs)):
            if FalseCropCatcher.get_if_is_false_positive(self.target_imgs[i].convert('RGB'), self.target_imgs[i].convert('RGB').load(), show = False):
                num_false_negatives += 1
            if i%10 == 0:
                print(100 * float(i)/float(len(self.target_imgs)), "% finished of target imgs")

        num_false_positives = 0
        for i in range(0, len(self.cropped_false_positive_imgs)):
            if not FalseCropCatcher.get_if_is_false_positive(self.cropped_false_positive_imgs[i].convert('RGB'), self.cropped_false_positive_imgs[i].convert('RGB').load(), show = False):
                num_false_positives += 1
            if i%10 == 0:
                print(100 * float(i)/float(len(self.target_imgs)), "% finished of non target imgs")
        return num_false_negatives, num_false_positives

    def get_avg_squared_histogram_differences_of_set(self, set):
        out_vals = []
        if set == "positives":
            for i in range(0, len(self.target_imgs)):
                out_vals.append(FalseCropCatcher.get_avg_squared_histogram_difference_of_img(self.target_imgs[i], self.target_imgs[i].load()))
        elif set == "negatives":
            for i in range(0, len(self.cropped_false_positive_imgs)):
                out_vals.append(FalseCropCatcher.get_avg_squared_histogram_difference_of_img(self.cropped_false_positive_imgs[i], self.cropped_false_positive_imgs[i].load()))
        else:
            raise ValueError("Valid set type not chosen")
        return numpy.asarray(out_vals)

    def get_best_split_spot_of_avg_squared_histogram_differences(self, positives, negatives):
        '''positives tend to be bigger, negatives tend to be smaller'''
        whole_list = positives.tolist()
        whole_list.extend(negatives.tolist())
        whole_list = sorted(whole_list)

        smallest_entropy = 2
        best_split_val = 0
        for i in range(0, len(whole_list)-1):
            split_val = (whole_list[i] + whole_list[i+1])/2.0
            iter_entropy = self.get_entropy_at_split(positives, negatives, split_val)
            if iter_entropy < smallest_entropy:
                smallest_entropy = iter_entropy
                best_split_val = split_val
            if i%10 == 0:
                print(100 * float(i)/float(len(whole_list)), "% finished")
        print("smallest entropy: ", smallest_entropy)
        return best_split_val


    def get_entropy_at_split(self, positives, negatives, split_val, print_vals = False):
        num_pos_split_smaller = 0
        num_neg_split_smaller = 0
        num_pos_split_greater = 0
        num_neg_split_greater = 0
        total_split_smaller = 0
        total_split_greater = 0
        for i in range(0, positives.shape[0]):
            if positives[i] > split_val:
                num_pos_split_greater += 1
                total_split_greater += 1
            else:
                num_pos_split_smaller += 1
                total_split_smaller += 1
        for i in range(0, negatives.shape[0]):
            if negatives[i] > split_val:
                num_neg_split_greater += 1
                total_split_greater += 1
            else:
                num_neg_split_smaller += 1
                total_split_smaller += 1

        if total_split_smaller == 0 or total_split_greater == 0 or num_pos_split_smaller == 0 or num_pos_split_greater == 0 or num_neg_split_smaller == 0 or num_neg_split_greater == 0:
            return 1.0

        if print_vals:
            print("num pos split smaller: ", num_pos_split_smaller)
            print("num neg split smaller: ", num_neg_split_smaller)
            print("num pos split greater: ", num_pos_split_greater)
            print("num neg split greater: ", num_neg_split_greater)
            print("total split smaller: ", total_split_smaller)
            print("total split greater: ", total_split_greater)

        entropy_smaller = -(float(num_pos_split_smaller)/float(total_split_smaller))*log(float(num_pos_split_smaller)/float(total_split_smaller), 2.0)
        entropy_smaller -= (float(num_neg_split_smaller)/float(total_split_smaller))*log(float(num_neg_split_smaller)/float(total_split_smaller), 2.0)

        entropy_greater = -(float(num_pos_split_greater)/float(total_split_greater))*log(float(num_pos_split_greater)/float(total_split_greater), 2.0)
        entropy_greater -= (float(num_neg_split_greater)/float(total_split_greater))*log(float(num_neg_split_greater)/float(total_split_greater), 2.0)

        entropy_out = (float(total_split_smaller)/float(total_split_smaller + total_split_greater)) * entropy_smaller + (float(total_split_greater)/float(total_split_smaller + total_split_greater)) * entropy_greater

        return entropy_out
