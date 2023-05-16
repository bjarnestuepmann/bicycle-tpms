from threading import Event
import logging

from measurementunitcomponent import MeasurementUnitComponent

class SensorReader(MeasurementUnitComponent):

    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event):
        super(SensorReader, self).__init__()

    def run(self):
        """Waiting for incoming control events and start associated functions."""
        logging.info("Ready to start measurement.")
        while(not self.terminated_event.is_set()):
            # Stream sensor data via zmq
            # until measurement event is set.
            self.streaming_loop()
            if self.start_measurement_event.is_set():
                logging.info("Start measurement.")
                self.measurement_loop()
                logging.info("Finish measurement.")
        
        self.clean_up()

    def streaming_loop(self):
        """Interface function. Must be implemented from subclasses.

        Reads the sensor data, preprocess them and publish them
        via zmq ipc.
        Returns when measurement event is set."""

        raise NotImplementedError(
            "Function stream_sensor_data of interface was called."
            )