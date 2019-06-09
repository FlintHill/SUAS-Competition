class GCSSettings(object):

    """
    Contains constants used in codebase.
    """

    CAMERA_NORTH_OFFSET = 20

    UAV_CONNECTION_STRING = "tcp:127.0.0.1:14551"
    INTEROP_URL = "http://10.43.4.247:8000"
    #INTEROP_URL = "http://192.168.1.86:8000"

    INTEROP_USERNAME = "testuser"   #"img_proc_test"
    INTEROP_PASSWORD = "testpass" #robotics

    INTEROP_DISCONNECT_RETRY_RATE = 0.5

    #Flint hill mean sea level:
    #MSL_ALT = 446.42
    #Competition mean sea level:
    MSL_ALT = 22
    SDA_MIN_ALT = 50

    GENERATED_DATA_LOCATION = "image_data"
    '''
    BASE_LETTER_CATEGORIZER_PCA_PATH
    Vale's path: /Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA
    '''
    VALE_BASE_LETTER_CATEGORIZER_PATH = "/Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA"
    BASE_LETTER_CATEGORIZER_PCA_PATH = VALE_BASE_LETTER_CATEGORIZER_PATH
    '''
    BASE_ORIENTATION_CLASSIFIER_PCA_PATH:
    Vale's path: /Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA
    '''
    VALE_BASE_ORIENTATION_CLASSIFIER_PCA_PATH = "/Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA"
    BASE_ORIENTATION_CLASSIFIER_PCA_PATH = VALE_BASE_ORIENTATION_CLASSIFIER_PCA_PATH

    SD_CARD_NAME = "Untitled"

    SEARCH_AREA_ALT = 350.0

    MIN_DIST_BETWEEN_TARGETS_KM = 30.0/1000.0
    KNOTS_PER_METERS_PER_SECOND = 1.94384448

    IMAGE_PROC_PPSI = 1.5
    
    AIRDROP_POINT = [(38.084510, -76.253500)]
    AIRDROP_POINT_SCHOL = [(__, __)]

    RUNWAY_POINTS = [(38.141528, -76.425203), (38.141794, -76.424801), (38.141827, -76.424840), (38.141917, -76.424805), (38.142017, -76.424822), (38.142138, -76.424900), (38.142219, -76.425022), (38.142318, -76.425324), (38.144586, -76.427587), (38.144608, -76.427575), (38.147814, -76.418490), (38.148175, -76.418751),
    (38.148324, -76.418913), (38.148441, -76.419127), (38.148523, -76.419409), (38.148541, -76.419733), (38.148490, -76.420000), (38.148431, -76.420177), (38.146397, -76.425948), (38.146397, -76.426050), (38.146167, -76.426684), (38.146117, -76.426727), (38.145529, -76.428387), (38.145553, -76.428546), (38.152078, -76.435063),
    (38.152243, -76.435054), (38.152358, -76.435109), (38.152471, -76.435243), (38.152517, -76.435377), (38.152523, -76.435509), (38.152562, -76.435537), (38.152320, -76.435963), (38.152325, -76.435977), (38.152199, -76.436160), (38.151993, -76.436289), (38.151785, -76.436334), (38.151523, -76.436275), (38.151401, -76.436173),
    (38.149219, -76.433995), (38.149071, -76.433991), (38.148651, -76.434661), (38.148647, -76.434730), (38.148426, -76.434518), (38.148476, -76.434504), (38.148886, -76.433847), (38.148877, -76.433643), (38.145131, -76.429905), (38.144973, -76.429973), (38.143476, -76.434223), (38.143345, -76.434455), (38.143141, -76.434633),
    (38.142849, -76.434707), (38.142587, -76.434590), (38.142236, -76.434300), (38.142200, -76.434166), (38.142195, -76.434049), (38.142232, -76.433907), (38.142292, -76.433791), (38.142488, -76.433603), (38.144408, -76.428148), (38.144407, -76.428072)]

    GRASS1_POINTS = [(38.145270, -76.428265), (38.145431, -76.428216), (38.145923, -76.426830), (38.145916, -76.426740), (38.146140, -76.426125), (38.146192, -76.426082), (38.148339, -76.419970), (38.148388, -76.419642), (38.148334, -76.419296), (38.148170, -76.419225), (38.148087, -76.419358), (38.147937, -76.419441),
    (38.144950, -76.427893), (38.144964, -76.427962)]

    GRASS2_POINTS = [(38.144797, -76.428458), (38.144745, -76.428483), (38.144563, -76.429000), (38.144597, -76.429148), (38.144865, -76.429413), (38.145027, -76.429368), (38.145167, -76.428979), (38.145147, -76.428808)]

    GRASS3_POINTS = [(38.144843, -76.429622), (38.144881, -76.429785), (38.143370, -76.434070), (38.143220, -76.434313), (38.143041, -76.434442), (38.142776, -76.434465), (38.142702, -76.434272), (38.144423, -76.429405), (38.144574, -76.429358)]

    GRASS4_POINTS = [(38.145151, -76.429700), (38.145116, -76.429577), (38.145275, -76.429136), (38.145434, -76.429092), (38.149294, -76.432950), (38.149323, -76.433143), (38.149113, -76.433495), (38.148952, -76.433495)]

    GRASS5_POINTS = [(38.149297, -76.433838), (38.149270, -76.433676), (38.149493, -76.433318), (38.149655, -76.433307), (38.152109, -76.435761), (38.152126, -76.435949), (38.151911, -76.436095), (38.151674, -76.436107), (38.151472, -76.436003)]
