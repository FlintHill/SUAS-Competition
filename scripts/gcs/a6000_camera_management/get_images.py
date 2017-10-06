from pysony import SonyAPI

class ClassName(threading.Thread):
    """docstring for ."""
    def __init__(self, arg):
        super(, self).__init__()
        self.arg = arg

    def run(self):
        if options.debug:
            print "searching for camera"

        search = ControlPoint()
        cameras =  search.discover(1)

        if len(cameras):
            camera = SonyAPI(QX_ADDR=cameras[0])
        else:
            print "No camera found, aborting"
            return

        setContShootingSpeet("")

        camera.setSelfTimer("5")
