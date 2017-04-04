import EigenFit.Load.NumpyLoader as NumpyLoader
import EigenFit.Vector.EigenProjector as EigenProjector
import EigenFit.Vector.VectorMath as VectorMath
from sklearn.neighbors import KNeighborsClassifier

class OrientationSolver(object):
    NUM_NEIGHBORS = 8
    def __init__(self, eigenvectors, mean, projections_path, num_dims):
        self.eigenvectors = eigenvectors
        self.mean = mean
        self.projections_path = projections_path
        self.num_dims = num_dims
        self.init_knn_data()
        self.init_knn()

    def init_knn_data(self):
        self.projections_data = []
        self.projections_targets = []
        for i in range(0, 8):
            projections = NumpyLoader.load_numpy_arr(self.projections_path + "/Data/Projections/" + str(i) + "/projection.npy")
            print("path is: " + str(self.projections_path + "/Data/Projections/" + str(i) + "/projection.npy"))
            print("projections is: " + str(projections))
            for j in range(0, projections.shape[0]):
                self.projections_data.append(projections[j][0:self.num_dims])
                self.projections_targets.append(i)

    def init_knn(self):
        self.knn = KNeighborsClassifier(n_neighbors = OrientationSolver.NUM_NEIGHBORS)
        self.knn.fit(self.projections_data, self.projections_targets)

    def get_letter_img_orientation(self, compare_img):
        img_projection = VectorMath.gray_img_to_vector(compare_img)
        projection_weights = EigenProjector.get_projection_weights(img_projection, self.eigenvectors, self.mean)[0:self.num_dims]


        return self.knn.predict([projection_weights])[0]
