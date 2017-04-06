import os
from PIL import Image, ImageOps
import EigenFit.Load.FileFunctions as FileFunctions
import ImgProcessingCLI.ImageOperation.Crop as Crop
import ImgProcessingCLI.NoiseReduction.NeighborhoodReduction as NeighborhoodReduction
from random import randint, random
import numpy
import string
from ImgProcessingCLI.General.TargetTwo import TargetTwo

class LetterGenerator:
    PCA_DIM = (40,40)
    ROTATION_RANGE = (-5.0, 5.0)
    def __init__(self, base_path, img_extension):
        self.base_path = base_path
        self.img_extension = img_extension
        self.init_imgs_and_answers()
        self.resize_imgs_to_PCA_specs()

    def init_imgs_and_answers(self):
        self.answers = os.listdir(self.base_path)
        FileFunctions.remove_dirs_that_arent_folders(self.answers)
        self.answers = tuple(self.answers)
        print("answers are: " + str(self.answers))
        self.imgs = [[] for i in range(0, len(self.answers))]
        for i in range(0, len(self.imgs)):
            base_letter_img_path = self.base_path + "/" + self.answers[i] + "/Training"
            img_names = os.listdir(base_letter_img_path)
            FileFunctions.remove_names_without_extension(img_names, self.img_extension)
            iter_imgs = [Image.open(base_letter_img_path + "/" + img_names[j]).convert('L') for j in range(0, len(img_names))]
            self.imgs[i].extend(iter_imgs)


    def resize_imgs_to_PCA_specs(self):
        for i in range(0, len(self.imgs)):
            for j in range(0, len(self.imgs[i])):
                self.imgs[i][j] = self.get_img_resized_to_PCA_specs(self.imgs[i][j])

    def get_img_resized_to_PCA_specs(self, img_in):
        img = ImageOps.invert(img_in)
        image = img.load()
        img = Crop.get_bw_img_cropped_to_bounds(img, image, margin=0)
        img = img.resize(LetterGenerator.PCA_DIM)
        return img

    def generate_test_set(self, base_path, num_imgs):
        save_imgs = []
        save_answers = []
        for i in range(0, num_imgs):
            letter_index = randint(0, 25)
            letter_img_index = randint(0, len(self.imgs[letter_index])-1)
            rand_img = self.imgs[letter_index][letter_img_index]
            rand_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(rand_img, rand_img.load(), TargetTwo.MODE_REDUCTION_KERNEL_SIZE)
            rand_img = rand_img.rotate(self.get_random_rotation_in_range(LetterGenerator.ROTATION_RANGE), expand = True)
            rand_img = self.get_img_resized_to_PCA_specs(ImageOps.invert(rand_img))
            save_imgs.append(rand_img)
            save_answers.append(self.answers[letter_index])

        for i in range(0, len(save_imgs)):
            save_imgs[i].save(base_path + "/Images/" + str(i) + ".png")

        numpy.save(base_path + "/Answers/answers.npy", numpy.asarray(save_answers))

    def generate_orientation_test_set(self, base_path, num_imgs):
        save_imgs = []
        save_answers = []
        for i in range(0, num_imgs):
            letter_index = randint(0, 25)
            letter_img_index = randint(0, len(self.imgs[letter_index])-1)
            rand_img = self.imgs[letter_index][letter_img_index]
            rand_rotation_index = randint(0, 7)
            rand_rotation_base = rand_rotation_index * 45
            rand_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(rand_img, rand_img.load(), TargetTwo.MODE_REDUCTION_KERNEL_SIZE)
            rand_img = rand_img.rotate(self.get_random_rotation_in_range(LetterGenerator.ROTATION_RANGE) + rand_rotation_base, expand = True)
            rand_img = self.get_img_resized_to_PCA_specs(ImageOps.invert(rand_img))
            save_imgs.append(rand_img)
            save_answers.append(rand_rotation_index)
            
        for i in range(0, len(save_imgs)):
            save_imgs[i].save(base_path + "/Images/" + str(i) + ".png")

        numpy.save(base_path + "/Answers/answers.npy", numpy.asarray(save_answers))

    def generate_training_set(self, base_path, num_instances_per_letter):
        letters = string.ascii_uppercase
        save_letter_imgs = [[] for i in range(0, len(letters))]
        for i in range(0, len(letters)):
            for j in range(0, num_instances_per_letter):
                letter_img_index = randint(0, len(self.imgs[i])-1)
                rand_img = self.imgs[i][letter_img_index]
                rand_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(rand_img, rand_img.load(), TargetTwo.MODE_REDUCTION_KERNEL_SIZE)
                rand_img = rand_img.rotate(self.get_random_rotation_in_range(LetterGenerator.ROTATION_RANGE), expand = True)
                rand_img = self.get_img_resized_to_PCA_specs(ImageOps.invert(rand_img))
                save_letter_imgs[i].append(rand_img)
            print("letter finished")

        for i in range(0, len(save_letter_imgs)):
            os.makedirs(base_path + "/All Letters/" + letters[i])
            for letter_index in range(0, len(save_letter_imgs[i])):
                save_letter_imgs[i][letter_index].save(base_path + "/All Letters/" + letters[i] + "/" + str(letter_index) + ".png")
                save_letter_imgs[i][letter_index].save(base_path + "/Individual Letters/" + str(i*num_instances_per_letter + letter_index) + ".png")

    def get_random_rotation_in_range(self, rotation_range):
        return rotation_range[0] + random()*(rotation_range[1]-rotation_range[0])
