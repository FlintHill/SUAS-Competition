'''
Created on Feb 7, 2017

@author: phusisian
'''
from math import sqrt
from root.nested.MatrixMath import MatrixMath
from root.nested.Vector import Vector
class Stat:
    @staticmethod
    def getCovariance(vars1, vars2, means):
        sum = 0
        for i in range(0, len(vars1)):
            sum += (vars1[i] - means[0])*(vars2[i] - means[1])
        return sum/float(len(vars1)-1)
    
    @staticmethod
    def get2dEigenvectors(matrix):
        eigenvalues = Stat.get2dEigenvalues(matrix)
        print("eigenvalues: " + str(eigenvalues))
        vectors = []
        x2 = 1
        for i in range(0, len(eigenvalues)):
            x1 = (eigenvalues[i]*x2 - matrix[1][1]*x2)/matrix[0][1]
            addVector = Vector([x1, x2])
            vectors.append(addVector)
        return vectors
    
    
    @staticmethod
    def get2dEigenvalues(matrix):
        ''''a = matrix[0][0]
        b = matrix[1][0]
        c = matrix[0][1]
        d = matrix[1][1]'''
        val1 = 0.5 * ((matrix[0][0] + matrix[1][1]) + sqrt(4*matrix[0][1]*matrix[1][0] + (matrix[0][0] - matrix[1][1])**2 ))#sqrt((a-c)**2 + 4*b**2)/2.0
        val2 = 0.5 * ((matrix[0][0] + matrix[1][1]) - sqrt(4*matrix[0][1]*matrix[1][0] + (matrix[0][0] - matrix[1][1])**2 ))
        return (val1, val2)