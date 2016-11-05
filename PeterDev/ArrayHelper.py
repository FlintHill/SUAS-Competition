#Used to make simple array functionalities used often easier to call
class ArrayHelper:
    
    def fillHorizontalLine(self, arr, value, x, y, width):#fills a horizontal line on the 2D listwith the specified value from (x,y) to (x+width,y)
        for i in range(x, x+width):
            arr[i][y] = value
        return arr
    
    def fillVerticalLine(self, arr, value, x, y, height):#fills a vertical line on the 2D list with the specified value from (x,y) to (x,y+height) (height being down)
        
        for i in range(y, y+height):
            arr[x][i] = value
        return arr
    
    def fillVerticalLineIfEmpty(self, arr, value, emptyValue, x, y, height):#fills a vertical line on the 2D list with the specified value from (x,y) to (x,y+height) in ONLY the spots where the array is "empty" (an index is considered empty if it is equal to the "emptyValue" passed to the method)
        for i in range(y, y+height):
            if arr[x][i] == emptyValue:
                arr[x][i] = value
        return arr