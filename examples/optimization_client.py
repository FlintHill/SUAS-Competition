from SUASImageParser.optimizers.new_optimizer import ADLCOptimizer
from SUASImageParser.optimizers.new_optimizer import OptimizerWorker

if __name__ == '__main__':
    worker = OptimizerWorker(debug=True)
    worker.run(ADLCOptimizer)
