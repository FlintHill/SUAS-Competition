import numpy 
import Random.Random as Random

class KMeans:
    
    '''takes a list of tuples, num clusters to round to, num times to run'''
    def __init__(self, data_in, num_clusters_in, times_to_run_in, step=1):
        self.data = data_in
        self.num_clusters = num_clusters_in
        self.times_to_run = times_to_run_in
        self.clusters = Clusters(data_in, num_clusters_in)
        self.step_count = 0
        for i in range(0, times_to_run_in):
            self.clusters.cycle(step, self.step_count)
            self.step_count += 1
            if self.step_count > step:
                self.step_count = 0

    @classmethod
    def init_with_img(cls, img, image, num_clusters_in, times_to_run_in, step_count=1):
        vectors = []
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                vectors.append(image[x,y])
        return KMeans(vectors, num_clusters_in, times_to_run_in, step_count)

    @classmethod
    def init_with_numpy(cls, numpy_data, num_clusters_in, times_to_run_in, step=1):
        data = []
        for i in range(0, numpy_data.shape[0]):
            data.append(tuple(numpy_data[i]))
        return KMeans(data, num_clusters_in, times_to_run_in, step)

    def get_clusters(self):
        return self.clusters

    def get_cluster_origins(self):
        origins = []
        for i in range(0, len(self.clusters)):
            origins.append(self.clusters[i].get_origin())
        return origins
    
    def get_cluster_origins_int(self):
        origins = self.get_cluster_origins()
        for i in range(0, len(origins)):
            origins[i] = tuple(int(origins[i][j]) for j in range(0, len(origins[i])))
        return origins

class Clusters:
    
    def __init__(self, data_in, clusters_in):
        self.data = data_in
        if type(clusters_in) is int:
            self.clusters = [Cluster(Random.get_random_value_from_list(data_in)) for i in range(0, clusters_in)]
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
            if len(self.clusters[i].get_vectors()) == 0:
                self.clusters[i] = Cluster(Random.get_random_value_from_list(self.data))
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

class Cluster:
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