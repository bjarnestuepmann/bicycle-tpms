from threading import Thread, Event

class BaseThread(Thread):

    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event):
        super(BaseThread, self).__init__()
        
        self.name = name
        self.start_measurement_event = start_measurement_event
        self.terminated_event = terminated_event

    def run(self):
        """Waiting for incoming control events and start associated fuctions"""
        while(not self.terminated_event.is_set()):        
            # wait for next measurement event
            self.start_measurement_event.wait(timeout=10)
            if self.start_measurement_event.is_set():
                self.measurement_loop()
        
        self.clean_up()

    def measurement_loop(self):
        pass

    def clean_up(self):
        pass