import numpy

class Clusters(object):

    def __init__(self, data_in, clusters_in):
        self.data = data_in
        if type(clusters_in) is int:
            #self.clusters = [Cluster(get_random_value_from_list(data_in)) for i in range(0, clusters_in)]
            #self.clusters = []
            cluster_origins = []
            for i in range(0, clusters_in):
                cluster_origins.append(get_random_value_from_list(data_in))
            self.clusters = [Cluster(cluster_origins[i]) for i in range(0, len(cluster_origins))]
        else:
            self.clusters = clusters_in

    def cycle(self, step, step_count):
        self.fit_data_to_clusters(step, step_count)
        self.reset_empty_clusters(step, step_count)
        self.set_clusters_origin_to_mean()
        self.clear_clusters()

    def fit_data_to_clusters(self, step, step_count):
        for i in range(step_count, len(self.data), step):
            self.get_closest_cluster_to_vector(self.data[i]).append_vector(self.data[i])

    def get_closest_cluster_to_vector(self, vector):
        sort_by_dist = sorted(self.clusters, key=lambda cluster : cluster.dist_to_origin(vector))
        return sort_by_dist[0]

    def reset_empty_clusters(self, step, step_count):
        for i in range(0, len(self.clusters)):
            cluster_origins = [self.clusters[i].get_origin() for i in range(0, len(self.clusters))]
            if len(self.clusters[i].get_vectors()) == 0:
                self.clusters[i] = Cluster(get_random_value_from_list(self.data))
        self.clear_clusters()
        self.fit_data_to_clusters(step, step_count)

    def set_clusters_origin_to_mean(self):
        for cluster in self.clusters:
            cluster.set_origin_to_mean()

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster.clear()

    def __len__(self):
        return len(self.clusters)

    def __getitem__(self, index):
        return self.clusters[index]

    def __delitem__(self, index):
        del self.clusters[index]

    def __repr__(self):
        out_str = ""
        for i in range(0, len(self.clusters)):
            out_str += str(self.clusters[i]) + ", "
        return out_str

class Cluster(object):

    def __init__(self, origin_in):
        self.origin = origin_in
        self.numpy_origin = numpy.asarray(self.origin)
        self.vectors = []

    def append_vector(self, vector):
        self.vectors.append(vector)

    def set_origin_to_mean(self):
        self.origin = self.get_mean()
        self.numpy_origin = numpy.asarray(self.origin)

    def get_mean(self):
        sums = [0 for i in range(0, len(self.origin))]
        for i in range(0, len(self.origin)):
            sum = 0
            for j in range(0, len(self.vectors)):
                sum += self.vectors[j][i]
            if(len(self.vectors) != 0):
                sums[i] = sum/float(len(self.vectors))

        return tuple(sums)

    def dist_to_origin(self, vector):
        numpy_delta = numpy.subtract(vector, self.numpy_origin)
        return numpy.linalg.norm(numpy_delta)

    def get_vectors(self):
        return self.vectors

    def get_origin(self):
        return self.origin

    def __len__(self):
        return len(self.vectors)

    def __getitem__(self, index):
        return self.vectors[index]

    def __repr__(self):
        return str(self.origin)

    def clear(self):
        self.vectors = []
