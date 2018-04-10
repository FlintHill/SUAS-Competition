import timeit
from UpdatedImageProcessing import *

start_time = timeit.default_timer()

IntegratedImageProcessingTester.complete_integrated_image_processing()
IntegratedImageProcessingTester.run_integrated_image_processing_tester()

Logger.format_time_report(timeit.default_timer() - start_time)
