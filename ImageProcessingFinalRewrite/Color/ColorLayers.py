

class ColorLayers:
    
    def __init__(self):
        self.color_layers = []
    
    def append_color_layer(self, color_layer_in):
        self.color_layers.append(color_layer_in)
        
    def __getitem__(self,index):
        return self.color_layers[index]
    
    def __len__(self):
        return len(self.color_layers)
    
    def set_color_layers(self, layers_in):
        self.color_layers = layers_in
    '''
    def __delitem__(self, index):
        del self.color_layers[index]
    '''
    
    def remove(self, obj):
        self.color_layers.remove(obj)
        
    def clone(self):
        clone_color_layers = ColorLayers()
        for i in range(0, len(self)):
            clone_color_layers.append_color_layer(self[i].clone())
        return clone_color_layers