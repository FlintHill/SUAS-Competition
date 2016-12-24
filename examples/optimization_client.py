from SUASImageParser.optimizers import ADLCOptimizer
from SUASImageParser.optimizers import OptimizerWorker

if __name__ == '__main__':
    worker = OptimizerWorker(debug=True)
    worker.run(ADLCOptimizer)
