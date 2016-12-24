from hurricane import SlaveNode
from time import sleep

class OptimizerWorker:
    """
    Provides the logic for a worker class that dynamically
    optimizes a scenario
    """

    def __init__(self, debug=False):
        """
        Initialize the worker
        """
        self.client_node = SlaveNode(debug=debug, master_node='127.0.0.1')
        self.client_node.initialize()
        self.client_node.wait_for_initialize()

        self.debug = debug
        self.images = None

    def run(self, optimizer):
        """
        Run the worker with a specific optimizer.

        :param optimizer: The optimizer to use during optimization
        """
        self.optimizer = optimizer(debug=True)

        while True:
            task_data = self.client_node.wait_for_task()

            if not self.images:
                self.images = self.optimizer.load_images(img_directory=task_data["img_directory"])
            scenario = task_data["scenario"]
            scenario_index = task_data["scenario_index"]
            score = self.optimizer.run_params(self.images, scenario)

            self.client_node.finish_task(generated_data={"result" : [scenario_index, score, scenario]})
