from UpdatedImageProcessing import ColorClassifier
import unittest
import os

class ColorClassifierTestCase(unittest.TestCase):

	def test_get_color(self):
		cc = ColorClassifier(os.path.realpath(__file__)[0:-24] + "test_color_classifier.png")
		result = cc.get_color()

		self.assertEqual(result, ["purple", "blue"])

	def test_three_dimesional_distance(self):
		cc = ColorClassifier("")

		three_d_dist_1 = cc.three_dimesional_distance([0, 0, 0], [0, 0, 0])
		three_d_dist_2 = cc.three_dimesional_distance([0, 0, 0], [1, 1, 1])
		three_d_dist_3 = cc.three_dimesional_distance([1, 1, 1], [1, 1, 1])
		three_d_dist_4 = cc.three_dimesional_distance([1, 1, 1], [0, 0, 0])
		three_d_dist_5 = cc.three_dimesional_distance([0, 0, 0], [-1, -1, -1])
		three_d_dist_6 = cc.three_dimesional_distance([-1, -1, -1], [-1, -1, -1])
		three_d_dist_7 = cc.three_dimesional_distance([-1, -1, -1], [0, 0, 0])
		three_d_dist_8 = cc.three_dimesional_distance([-1, -1, -1], [1, 1, 1])
		three_d_dist_9 = cc.three_dimesional_distance([123, 456, 789], [123, 456, 789])
		three_d_dist_10 = cc.three_dimesional_distance([-192, -492, -1], [0, -1, 1])

		self.assertEqual(round(three_d_dist_1, 3), round(0.0000, 3))
		self.assertEqual(round(three_d_dist_2, 3), round(1.732051, 3))
		self.assertEqual(round(three_d_dist_3, 3), round(0.0000, 3))
		self.assertEqual(round(three_d_dist_4, 3), round(1.732051, 3))
		self.assertEqual(round(three_d_dist_5, 3), round(1.732051, 3))
		self.assertEqual(round(three_d_dist_6, 3), round(0.0000, 3))
		self.assertEqual(round(three_d_dist_7, 3), round(1.732051, 3))
		self.assertEqual(round(three_d_dist_8, 3), round(3.4641, 3))
		self.assertEqual(round(three_d_dist_9, 3), round(0.0000, 3))
		self.assertEqual(round(three_d_dist_10, 3), round(527.2086, 3))

	def test_convert_rgba_to_color_name(self):
		cc = ColorClassifier()

		test_rgba = [
			[255, 255, 255, 255],
			[0, 0, 0, 255],
			[128, 128, 128, 255],
			[255, 0, 0, 255],
			[0, 0, 255, 255],
			[0, 255, 0, 255],
			[255, 255, 0, 255],
			[128, 0, 128, 255],
			[165, 42, 42, 255],
			[255, 165, 0, 255]
		]

		test_answers = [
			"white",
			"black",
			"gray",
			"red",
			"blue",
			"green",
			"yellow",
			"purple",
			"brown",
			"orange"
		]

		test_results = []

		for rgba in test_rgba:
			test_results.append(cc.convert_rgba_to_color_name(rgba))

		i = 0

		while i < len(test_results):
			self.assertEqual(test_results[i], test_answers[i])

			i += 1

	def test_convert_color_name_to_rgba(self):
		cc = ColorClassifier()

		test_color_names = [
			"white",
			"black",
			"gray",
			"red",
			"blue",
			"green",
			"yellow",
			"purple",
			"brown",
			"orange"
		]

		test_answers = [
			[255, 255, 255, 255],
			[0, 0, 0, 255],
			[128, 128, 128, 255],
			[255, 0, 0, 255],
			[0, 0, 255, 255],
			[0, 255, 0, 255],
			[255, 255, 0, 255],
			[128, 0, 128, 255],
			[165, 42, 42, 255],
			[255, 165, 0, 255]
		]

		test_results = []

		for color_name in test_color_names:
			test_results.append(cc.convert_color_name_to_rgba(color_name))

		i = 0

		while i < len(test_results):
			self.assertEqual(test_results[i], test_answers[i])

			i += 1

	def test_no_image(self):
		cc = ColorClassifier()

		with self.assertRaises(Exception):
			cc.get_color()
