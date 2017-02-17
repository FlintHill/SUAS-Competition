

def search(array, search_value, key=lambda x: x):
    for i in range(0, len(array)):
        if key(array[i]) == search_value:
            print(str(key(array[i])) + ", " + str(search_value))
            return i
    return None

    