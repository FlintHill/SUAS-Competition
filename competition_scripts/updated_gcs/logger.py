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

def log_vehicle_state(vehicle, logger_name):
    """
    Log a vehicle's state
    """
    log(logger_name, " Get all vehicle attribute values:")
    log(logger_name, " Autopilot Firmware version: %s" % vehicle.version)
    log(logger_name, "   Major version number: %s" % vehicle.version.major)
    log(logger_name, "   Minor version number: %s" % vehicle.version.minor)
    log(logger_name, "   Patch version number: %s" % vehicle.version.patch)
    log(logger_name, "   Release type: %s" % vehicle.version.release_type())
    log(logger_name, "   Release version: %s" % vehicle.version.release_version())
    log(logger_name, "   Stable release?: %s" % vehicle.version.is_stable())
    log(logger_name, " Autopilot capabilities")
    log(logger_name, "   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
    log(logger_name, "   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
    log(logger_name, "   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
    log(logger_name, "   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
    log(logger_name, "   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
    log(logger_name, "   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
    log(logger_name, "   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
    log(logger_name, "   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
    log(logger_name, "   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
    log(logger_name, "   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
    log(logger_name, "   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
    log(logger_name, "   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
    log(logger_name, "   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
    log(logger_name, "   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
    log(logger_name, " Global Location: %s" % vehicle.location.global_frame)
    log(logger_name, " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    log(logger_name, " Local Location: %s" % vehicle.location.local_frame)
    log(logger_name, " Attitude: %s" % vehicle.attitude)
    log(logger_name, " Velocity: %s" % vehicle.velocity)
    log(logger_name, " GPS: %s" % vehicle.gps_0)
    log(logger_name, " Gimbal status: %s" % vehicle.gimbal)
    log(logger_name, " Battery: %s" % vehicle.battery)
    log(logger_name, " EKF OK?: %s" % vehicle.ekf_ok)
    log(logger_name, " Last Heartbeat: %s" % vehicle.last_heartbeat)
    log(logger_name, " Rangefinder: %s" % vehicle.rangefinder)
    log(logger_name, " Rangefinder distance: %s" % vehicle.rangefinder.distance)
    log(logger_name, " Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    log(logger_name, " Heading: %s" % vehicle.heading)
    log(logger_name, " Is Armable?: %s" % vehicle.is_armable)
    log(logger_name, " System status: %s" % vehicle.system_status.state)
    log(logger_name, " Groundspeed: %s" % vehicle.groundspeed)    # settable
    log(logger_name, " Airspeed: %s" % vehicle.airspeed)    # settable
    log(logger_name, " Mode: %s" % vehicle.mode.name)    # settable
    log(logger_name, " Armed: %s" % vehicle.armed)    # settable
