from abc import ABCMeta
from abc import abstractmethod

class Optimizer(object):
    """
    Base class for all optimizers. Provides the logic for optimizing
    a mode (ALDC, Emergent, etc)
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self):
        """
        Optimize() provides the logic to optimize a set of images
        with a set of parameters
        """
        raise NotImplementedError("Should implement optimize()")

    @abstractmethod
    def run_params(self):
        """
        Provides the logic to run a scenario on a set of images
        """
        raise NotImplementedError("Should implement run_params()")

    @abstractmethod
    def score(self):
        """
        Provides the logic for scoring a run of the optimizer
        """
        raise NotImplementedError("Should implement score()")
