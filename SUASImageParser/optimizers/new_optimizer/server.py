from hurricane import MasterNode
from SUASImageParser.utils.color import bcolors

class OptimizerServer:
    """
    Creates a server to run an optimization through
    """

    def __init__(self, debug):
        """
        Initializes the server
        """
        self.server = MasterNode(debug=True, starting_task_port=12228)
        self.server.initialize()
        self.debug = debug

    def serve(self, images, scenarios):
        """
        Run the optimization server to optimize the scenarios to a set
        of images.

        :param images: The images to optimize the scenarios to
        :param scenarios: The scenarios to use during optimization
        """
        if self.debug:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Waiting for a connection...")
        self.server.wait_for_connection()
        if self.debug:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Connection to at least one worker has been established")

        for i in range(len(scenarios)):
            task = {"scenario_index" : i}#, "images" : images, "scenario" : scenarios[i]}
            self.server.send_task(task)

        completed_scenarios = []
        for i in range(len(scenarios)):
            completed_task = self.server.wait_for_any_task_completion()

            if completed_task:
                if self.debug:
                    print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Completed task number " + str(i))
                completed_scenarios.append(completed_task.get_generated_data()["result"])

        return completed_scenarios
