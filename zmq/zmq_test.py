from threading import Thread
from time import sleep

from zmq import Context, SUB, SUBSCRIBE, PUB, SNDMORE

def sub_thread_routine():
    context = Context()
    socket = context.socket(SUB)
    socket.connect("ipc://my-endpoint")
    socket.setsockopt(SUBSCRIBE, b'MyTopic')
    print("Subscriber connected.")
    
    sleep(2)

    msgs = socket.recv_multipart()
    print(msgs)


def main():
    # Create subscriber thread.
    sub_thread = Thread(target=sub_thread_routine)
    sub_thread.start()

    # Publish 
    context = Context()
    socket = context.socket(PUB)
    socket.bind("ipc://my-endpoint")
    
    sleep(2)

    socket.send_multipart([b"MyTopic", b"Hello World!"])

    print("Wait for subscriber...")
    sub_thread.join()
    print("Exit program.")


if __name__ == "__main__":
    main()