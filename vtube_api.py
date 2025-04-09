import json
import threading
import os
import time
import math
from websocket import WebSocketApp
from variables import AppName
from equations import RandomWave


class VTubeStudioAPI:
    def __init__(self, on_message_callback=None, on_error_callback=None):
        self.ws_url = "ws://localhost:8001"
        self.token_file = "vtube_token.json"
        self.token = self._load_token()
        self.ws = None
        self.on_message_callback = on_message_callback
        self.on_error_callback = on_error_callback
        self.ws_thread = None  # Store the WebSocket thread for management

    def _load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                data = json.load(f)
                return data.get("authenticationToken")
        return None

    def _save_token(self, token):
        with open(self.token_file, "w") as f:
            json.dump({"authenticationToken": token}, f)

    def auto_authenticate(self):
        if self.token:
            self.send_authentication(self.token)
        else:
            self.send_auth_token_request()

#todo connect websocket after initial auth TEST
    def send_auth_token_request(self):
        def on_open(ws):
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "TokenRequest",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": AppName,
                    "pluginDeveloper": "Morgan Mundie"
                }
            }
            print(f" App name {payload}")

            ws.send(json.dumps(payload))

        def on_message(ws, message):
            data = json.loads(message)
            token = data.get("data", {}).get("authenticationToken")
            if token:
                self._save_token(token)
                self.send_authentication(token)
            if self.on_message_callback:
                self.on_message_callback(message)
            ws.close()

        self._run_ws(on_open, on_message)

    def send_authentication(self, token):
        def on_open(ws):
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "AuthRequest",
                "messageType": "AuthenticationRequest",
                "data": {
                    "pluginName": AppName,
                    "pluginDeveloper": "Morgan Mundie",
                    "authenticationToken": token
                }
            }
            ws.send(json.dumps(payload))

        self._run_ws(on_open)


    def create_param(self, name, min, max):
        # Check if the WebSocket is already open
        print(self)  #todo fixme this doesnt have a ws for some reason
        if self.ws and self.ws.sock and self.ws.sock.connected:
            print("WebSocket is already connected.")
            # Send the payload over the existing WebSocket connection
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "tesstcreate",
                "messageType": "ParameterCreationRequest",
                "data": {
                    "parameterName": name,
                    "explanation": "This is my new parameter.",
                    "min": min,
                    "max": max,
                    "defaultValue": 0
                }
            }
            print(name)
            self.ws.send(json.dumps(payload))
            print("Sent load")  # This should now print
        else:
            print("WebSocket is not connected. Attempting to connect...")
            # If the WebSocket isn't connected, you can run the connection logic
            self._run_ws(self.on_open, self.on_message)


    def start_continuous_input(self, input_id="WaveParam", interval=0.05):
        """
        Starts a loop sending dynamic random wave output values through a WebSocket.
        The loop automatically stops after 10 seconds.
        """
        print("started")
        
        wave = RandomWave(seed=42)
        # todo move to class
        speed_multiplier = 1

        def send_input(val):
            # print(f"sending {val}")
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "mode": "set",
                    "parameterValues": [
                        {
                            "id": input_id,
                            "value": val
                        }
                    ]
                }
            }
            self.ws.send(json.dumps(payload))

        def send_loop():
            print("loop")
            start_time = time.time()
            while True:
                # todo remove: for testing only
                if time.time() - start_time > 25:
                    break
                
                dt = interval * speed_multiplier
                raw_value = wave.get_value(dt)
                # Normalize to the range 0-1 (change later to dynamic range)
                normalized_value = (raw_value + 1) / 2
                send_input(normalized_value)
                time.sleep(interval)

        # Check if the WebSocket is connected before starting the loop.
        if self.ws and self.ws.sock and self.ws.sock.connected:
            thread = threading.Thread(target=send_loop)
            thread.daemon = True  
            thread.start()
        else:
            print("WebSocket is not connected. Attempting to connect...")
            #no self on open todo fixme
            self._run_ws(self.on_open, self.on_message)


    #todo fix and check this
    def _run_ws(self, on_open, on_message=None):
        def default_on_message(ws, message):
            if self.on_message_callback:
                self.on_message_callback(message)

        def on_error(ws, error):
            if self.on_error_callback:
                self.on_error_callback(str(error))

        print(self.ws)
        if not self.ws:  # Only create a WebSocket if it doesn't exist already
            self.ws = WebSocketApp(
                self.ws_url,
                on_open=on_open,
                on_message=on_message or default_on_message,
                on_error=on_error
            )

            # Start WebSocket in a new thread
            print(self.ws_thread)
            if not self.ws_thread:
                self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
                self.ws_thread.start()
