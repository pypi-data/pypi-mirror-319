from typing import Callable, List
from streamer import streamer_pb2
import ctypes
import threading
import os

# Load the shared library
streamer_lib_path = os.path.join(os.path.dirname(__file__), "streamer/streamer.so")
mylib = ctypes.CDLL(streamer_lib_path)

class Messenger:
    def __init__(self) -> None:
        self._listeners: List[Callable[[bytes], None]] = []
        self._out_ptr = ctypes.c_char_p()
        self._out_len = ctypes.c_size_t()
        self._running = False
        self._listen_thread = None
    
    def is_connected(self) -> bool:
        return mylib.streamer_discovery_is_connected() == 0
    
    def connect(self) -> bool:
        is_connected = self.is_connected()
        if is_connected:
            return True
        
        connection = mylib.streamer_discovery_connect()
        if connection == -1:
            print("Step 1. Unable to connect to the Streamer")
            return False
        
        offer = mylib.streamer_discovery_receive_offer(
            ctypes.byref(self._out_ptr),
            ctypes.byref(self._out_len)
        )
        if offer == 1:
            print("Step 2. The Streamer didn't send any offer, connection terminated")
            self.disconnect()
            return False
        
        # Subscribe to all messages
        answer = mylib.streamer_discover_send_answer(0x7FFFFFFF)
        if answer == 1:
            print("Step 3. Subscription to messages failed, connection terminated")
            self.disconnect()
            return False
        
        return True
    
    def disconnect(self) -> None:
        mylib.streamer_discovery_disconnect()

    def listen(self) -> None:
        """Start listening in a background thread"""
        if self._listen_thread and self._listen_thread.is_alive():
            return
        
        self._running = True
        self._listen_thread = threading.Thread(target=self._listen_loop)
        self._listen_thread.daemon = True
        self._listen_thread.start()

    def _listen_loop(self) -> None:
        """Internal method that runs the listening loop"""
        while self._running and self.is_connected():
            messages = mylib.streamer_discovery_tick()
            # print(f"Data: {messages}")

            if messages > 0:
                for i in range(messages):
                    print("there are messages")
                    response = mylib.streamer_discovery_consume_events(
                            ctypes.byref(self._out_ptr),
                            ctypes.byref(self._out_len),
                            )

                    if response == 1:
                        print("Couldn't get a message")
                        continue

                    data = ctypes.string_at(self._out_ptr.value, self._out_len.value)
                    message = streamer_pb2.Message()
                    message.ParseFromString(data)
                    print(message.messageType)

                    for listener in self._listeners:
                        listener(message)
        print("Stopped listening")
        self.stop()

    def stop(self) -> None:
        """Stop the listening thread"""
        self._running = False
        if self._listen_thread:
            self._listen_thread.join(timeout=1.0)
        self.disconnect()
    
    def add_listener(self, listener: Callable[[bytes], None]) -> None:
        self._listeners.append(listener)