import os
import EigenFit.Load.FileFunctions as FileFunctions
from PIL import Image
import json
import ImgProcessingCLI.Runtime.TargetCropper as TargetCropper
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
from math import sqrt
import numpy
from ImgProcessingCLI.Geometry.Rectangle import Rectangle
import ImgProcessingCLI.Runtime.TargetCropper2 as TargetCropper2
class CropTester(object):

    DEFAULT_PPSI = 6.0#3.567
    DEFAULT_GEOSTAMPS = GeoStamps([GeoStamp((100, 100), 0), GeoStamp((100, 150), 1)])

    def __init__(self, set_path, image_type):
        self.init_img_paths(set_path, image_type)


    def init_img_paths(self, set_path, image_type):
        answer_path = set_path + "/Answers"
        images_path = set_path + "/Images"
        image_names = os.listdir(images_path)
        answer_names = os.listdir(answer_path)
        FileFunctions.remove_names_without_extension(answer_names, ".json")
        FileFunctions.remove_names_without_extension(image_names, image_type)
        self.image_paths = [set_path + "/Images/" + image_names[i] for i in range(0, len(image_names))]
        self.answer_paths = [set_path + "/Answers/" + answer_names[i] for i in range(0, len(answer_names))]


    def test_set(self, max_pixel_distance_to_correct):

        total_score = 0
        total_possible = 0
        tot_positives = 0
        tot_false_positives = 0
        tot_missing = 0
        tot_possible = 0
        for i in range(0, len(self.image_paths)):
            #try:
            img, answer = self.load_img_and_answers(i)
            actual_crops, target_centers = TargetCropper2.get_target_crops_from_img(img, CropTester.DEFAULT_GEOSTAMPS, CropTester.DEFAULT_PPSI, get_centers = True)
            #print("json answer is: ", answer[0])
            answer_centers = []
            for j in range(0, len(answer)):
                answer_centers.append(answer[j]["midpoint"])
            #print("answer centers: ", answer_centers)
            iter_positives, iter_false_positives, iter_missing_targets, iter_possible = self.check_centers(target_centers, answer_centers, max_pixel_distance_to_correct, img, i, actual_crops)
            tot_positives += iter_positives
            tot_false_positives += iter_false_positives
            tot_missing += iter_missing_targets
            tot_possible += iter_possible


            for j in range(0, len(actual_crops)):
                #actual_crops[j].get_crop_img().show()
                actual_crops[j].get_crop_img().save("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full/Test Outputs Multiple Backgrounds 2/" + str(i) + "," + str(j) + ".png")

            print("tot positives: ", tot_positives, ", tot false positives: ", tot_false_positives, ", tot missing: ", tot_missing, ", tot possible: ", tot_possible)
            if iter_false_positives > 0:
                self.check_centers(target_centers, answer_centers, max_pixel_distance_to_correct, img = img)
            #except:
            #    print('some kind of error occurred in CropTester')

            #print("iter positives: ", iter_positives, ", iter false positives: ", iter_false_positives, ", iter missing targets: ", iter_missing_targets)
        return tot_positives, tot_false_positives, tot_missing, tot_possible


    def check_centers(self, target_centers, answer_centers, max_pixel_distance_to_correct, img = None, index = None, actual_crops = None):

        positives = 0
        missing_targets = 0
        false_positives = 0
        i = 0

        tot_possible = len(answer_centers)
        while i < len(target_centers) and len(answer_centers) > 0:
            target_center = target_centers[i]
            answers_sorted_by_proximity = sorted(answer_centers, key = lambda center : numpy.linalg.norm(numpy.asarray(target_center)-numpy.asarray(center)))
            shortest_dist = numpy.linalg.norm(numpy.asarray(target_center)-numpy.asarray(answers_sorted_by_proximity[0]))
            if shortest_dist < max_pixel_distance_to_correct:
                positives += 1
                '''only removes if the answer is correct because it is possible for a false positive to remove a later correct answer.
                Currently doesn't remove at all, but probably should'''
                #del answer_centers[answer_centers.index(answers_sorted_by_proximity[0])]
            else:
                false_positives += 1
            i += 1


        missing_targets = tot_possible - positives
        '''i = 0
        while i < len(answer_centers) and len(target_centers) > 0:
            answer_center = answer_centers[i]
            targets_sorted_by_proximity = sorted(target_centers, key = lambda center : numpy.linalg.norm(numpy.asarray(answer_center) - numpy.asarray(center)))
            shortest_dist = numpy.linalg.norm(numpy.asarray(target_center) - numpy.asarray(targets_sorted_by_proximity))
            if shortest_dist > max_pixel_distance_to_correct:
                missing_targets += 1
            i += 1'''

        '''if img != None and index != None:
            img_copy = img.copy()
            image_copy = img_copy.load()

            for i in range(0, len(target_centers)):
                blue_rect = Rectangle(int(actual_crops[i].get_crop_loc()[0]-actual_crops[i].get_crop_img().size[0]//2), int(actual_crops[i].get_crop_loc()[1]-actual_crops[i].get_crop_img().size[1]//2), actual_crops[i].get_crop_img().size[0], actual_crops[i].get_crop_img().size[1])
                blue_rect.draw(img_copy, image_copy, (0,0,255), stroke_width = 15)
            img_copy.save("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full/DotsAtCrops/" + str(index) + ".png")
        '''
        #img_copy.show()
        #img_copy.show()
        return positives, false_positives, missing_targets, tot_possible




    def load_img_and_answers(self, img_index):
        img = Image.open(self.image_paths[img_index]).convert('RGB')
        answer = None
        with open(self.answer_paths[img_index]) as json_data:
            answer = json.load(json_data)
        return img, answer
