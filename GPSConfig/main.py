from gpssensorreader import GPSSensorReader
from displaythread import DisplayThread
from configscreen import ConfigScreen
from threading import Event
from time import sleep

# DisplayThread
# Screen
# GPSSensorReader
# main


def main():
    """ Read the sensor data and show it on screen."""
    stop_event = Event()
    gps_reader = GPSSensorReader(stop_event)
    dsp_thread = DisplayThread(1, stop_event)
    
    dsp_thread.start()
    gps_reader.start()
    
    cfg_screen = ConfigScreen(dsp_thread)
    
    try:
        while True:
            config = gps_reader.get_config()
            print(config.clk_h)
            cfg_screen.set_config(config)
            cfg_screen.refresh()
            sleep(1)

    except KeyboardInterrupt:
        print(": Terminated by User")

    finally:
        print("Stop measurement.")
        stop_event.set()

    gps_reader.join()
    dsp_thread.join()

if __name__ == '__main__':
    main()
