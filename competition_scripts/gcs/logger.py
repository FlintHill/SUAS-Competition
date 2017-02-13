import logging
import logging.handlers

log_file = "./data/log.log"

logging.basicConfig(format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
	filename=log_file, filemode='w',
	level=logging.INFO)

class QueueHandler(logging.Handler):
    """
    This is a logging handler which sends events to a multiprocessing queue.

    The plan is to add it to Python 3.2, but this can be copy pasted into
    user code for use with earlier Python versions.
    """

    def __init__(self, queue):
        """
        Initialise an instance, using the passed queue.
        """
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue.
        """
        try:
            ei = record.exc_info
            if ei:
                dummy = self.format(record) # just to get traceback text into record.exc_text
                record.exc_info = None  # not needed any more
            self.queue.put_nowait(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def logger_listener_configurer():
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler(log_file, 'w')
    f = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

def logger_worker_configurer(queue):
    h = QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.INFO)

def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:')
            traceback.print_exc(file=sys.stderr)

def log(name, message):
    logger_instance = logging.getLogger(name)
    logger_instance.info(message)
    print(message)
