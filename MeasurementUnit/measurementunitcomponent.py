from threading import Thread, Event
import logging

class MeasurementUnitComponent(Thread):

    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event):
        super(MeasurementUnitComponent, self).__init__()
        
        self.name = name
        self.start_measurement_event = start_measurement_event
        self.terminated_event = terminated_event

    def run(self):
        """Waiting for incoming control events and start associated functions."""
        logging.info("Ready to start measurement.")
        while(not self.terminated_event.is_set()):
            self.start_measurement_event.wait(timeout=1)
            if self.start_measurement_event.is_set():
                logging.info("Start measurement.")
                self.measurement_loop()
                logging.info("Finish measurement.")
        
        self.clean_up()

    def measurement_loop(self):
        """Interface function. Must be implemented from subclasses.

        Function is called, when measurement event is set.
        Reads the sensor sensor data, save them in internal lists
        and write them to file, when measurement event is cleared.
        Returns after writing the measurements to file."""

        raise NotImplementedError(
            "Function record_sensor_data of interface was called."
            )

    def clean_up(self):
        pass