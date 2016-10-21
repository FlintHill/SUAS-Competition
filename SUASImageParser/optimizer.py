from SUASImageParser.optimizers import ADLCOptimizer

class Optimizer:
    """
    Optimizer for SUAS Image parser. Use this to tune parameters to get the best results.

    author: Vale Tolpegin
    """

    def __init__(self, **kwargs):
        self.output_file = kwargs.get("output_file", None)
        self.image_directory = kwargs.get("img_directory", None)

        if self.output_file == None:
            raise ValueError('Please specify an output file to save tuned parameters to')

        if self.image_directory == None:
            raise ValueError('Please specify a data directory to get images from')

        self.adlc_optimizer = ADLCOptimizer()

    def optimize(self, **kwargs):
        """
        Optimize the parameters
        """
        mode = kwargs.get("mode", None)

        if mode == None:
            raise ValueError('Please specify a mode to use (i.e. "ADLC" if you would like to use the ADLC optimizer)')

    def save_params(self):
        """
        Save the parameters to a file.
        """
        pass
