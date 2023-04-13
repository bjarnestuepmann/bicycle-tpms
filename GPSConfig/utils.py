

SensorTypeTranslator = {
    5: "GYRO-Z",
    13: "GYRO-Y",
    14: "GYRO-X",
    16: "ACCEL-X",
    17: "ACCEL-Y",
    18: "ACCEL-Z"
}

FixTypeTranslator = {
    0: "NO",
    1: "DR",
    2: "2D",
    3: "3D",
    4: "COM",
    5: "TM"
}

SensorToIndexTranlator = {
    "GYRO-Y" : (0,1), "ACCEL-X": (1,1),
    "GYRO-X" : (0,0), "ACCEL-Y": (1,0),
    "GYRO-Z" : (0,2), "ACCEL-Z": (1,2)
}

CalibstatusToColorTranslator = {
    0: (0xef,0x43, 0x47), # not calibrated - red
    1: (0xf9,0xc7, 0x50), # calibrating - yellow
    2: (0x90,0xbe, 0x6d)  # calibrated - green
}

class GPSConfig():

    def __init__(self) -> None:
        self.fusion_mode = 0
        self.fix_type = 0
        self.alg_status = 0
        self.clk_h = 0
        self.clk_min = 0
        self.sv = 0

        self.calib_states = {
            "GYRO-Z": 0,
            "GYRO-Y": 0,
            "GYRO-X": 0,
            "ACCEL-X": 0,
            "ACCEL-Y": 0,
            "ACCEL-Z": 0
        }