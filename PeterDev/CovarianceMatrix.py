'''
Created on Feb 7, 2017

@author: phusisian
'''
from root.nested.Stat import Stat
class CovarianceMatrix:
    
    def __init__(self, matrixIn):
        self.matrixIn = matrixIn
        #self.initMeans()
        self.initSplitValues()
        self.initMeans()
        self.initMatrix()
    
    def __getitem__(self, index):
        return self.covarMatrix[index]
    
    def __len__(self):
        return len(self.covarMatrix)
    
    def initMeans(self):
        self.means = []
        for i in range(0, len(self.splits)):
            sum = 0
            for j in range(0, len(self.splits[i])):
                sum += self.splits[i][j]
            self.means.append(float(sum)/float(len(self.splits[i])))
        '''for dimNum in range(0, self.matrixIn.getDim()):
            sum = 0
            for i in range(0, len(self.matrixIn)):
                sum += self.matrixIn[i][dimNum]
            avg = sum/float(len(self.matrixIn))
            self.means.append(avg)
        print("means: " + str(self.means))'''
    
    def getMeans(self):
        return self.means
    
    def initSplitValues(self):
        #FIRST INDEX: DIMENSION. SECOND INDEX, NUMBER
        self.splits = [[0 for j in range(0, len(self.matrixIn))]for i in range(0, self.matrixIn.getDim())]
        #self.splits = [[0 for i in range(0, self.matrixIn.getDim())] for i in range(0, len(self.matrixIn))]
        
        for dimNum in range(0, self.matrixIn.getDim()):
            for i in range(0, len(self.matrixIn)):
                self.splits[dimNum][i] = self.matrixIn[i][dimNum]
        print("splits: " + str(self.splits))
    
    def initMatrix(self):
        dims = self.matrixIn.getDim()
        self.covarMatrix = [[0 for j in range(0, dims)] for i in range(0, dims)]
        
        for i in range(0, dims):
            for j in range(0, dims):
                self.covarMatrix[i][j] = Stat.getCovariance(self.splits[i], self.splits[j], (self.means[i], self.means[j]))
        print(self.covarMatrix)