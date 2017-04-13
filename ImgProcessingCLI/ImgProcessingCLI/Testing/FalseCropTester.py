import EigenFit.Load.FileFunctions as FileFunctions
import os
from PIL import Image
import random
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher


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

        for i in range(0, 5):
            rand_pic = self.cropped_false_positive_imgs[random.randint(0, len(self.cropped_false_positive_imgs)-1)]
            rand_pic.show()

    def run_imgs(self):
        num_false_negatives = 0
        for i in range(0, len(self.target_imgs)):
            if FalseCropCatcher.get_if_is_false_positive(self.target_imgs[i].convert('RGB'), self.target_imgs[i].convert('RGB').load()):
                num_false_negatives += 1
            if i%10 == 0:
                print(str(i) + " finished of false negatives")

        num_false_positives = 0
        for i in range(0, len(self.cropped_false_positive_imgs)):
            if not FalseCropCatcher.get_if_is_false_positive(self.cropped_false_positive_imgs[i].convert('RGB'), self.cropped_false_positive_imgs[i].convert('RGB').load()):
                num_false_positives += 1
            if i%10 == 0:
                print(str(i) + " finished of false positives")
        return num_false_negatives, num_false_positives
