import zmq
import threading
import time

# Funktion, die im Hintergrund läuft und auf neue Nachrichten von dem Publisher wartet
def subscriber_task(running):
    thread = threading.current_thread()
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("ipc://sensor.int1")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    while running:
        msg = subscriber.recv()
        print(f"{thread.name} - Empfangen: {int.from_bytes(msg, byteorder='big')}")


# Funktion, die im Hintergrund läuft und regelmäßig Nachrichten an den Subscriber sendet
def publisher_task(running):
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("ipc://sensor.int1")
    i = 0
    while running:
        i += 1
        print("Senden: ", i)
        publisher.send(i.to_bytes(4, byteorder='big'))
        time.sleep(1)

def main():
    # Erstellen und Starten der Threads
    running = True
    threads = list()
    
    # Subscriber
    for t_idx in range(3):
        threads.append(
             threading.Thread(target=subscriber_task, args=(running,))
             )
    # Publisher
    threads.append(
         threading.Thread(target=publisher_task, args=(running,))
         )

    for thread in threads:
         thread.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
            running = False
            print("Keyboard Interrupt.")

    print("Wait for threads.")
    for thread in threads:
         thread.join()

if __name__== "__main__":
     main()