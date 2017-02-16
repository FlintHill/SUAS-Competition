'''
Created on Feb 7, 2017

@author: phusisian
'''
class MatrixMath:
    
    @staticmethod
    def getMatrixPlusScalar(matrix, scalar):
        editedMatrix = matrix
        for i in range(0, len(matrix)):
            editedMatrix[i][i] = matrix[i][i] + scalar
        return editedMatrix