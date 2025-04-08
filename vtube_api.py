import json
import threading
import os
import time
import math
from websocket import WebSocketApp
from variables import AppName



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

    def send_auth_token_request(self):
        def on_open(ws):
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "TokenRequest123",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": AppName.strip(" "),
                    "git ": "MorganMundie"
                }
            }
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
                    "pluginName": AppName.strip(" "),
                    "pluginDeveloper": "MorganMundie",
                    "authenticationToken": token
                }
            }
            ws.send(json.dumps(payload))

        self._run_ws(on_open)


    def create_param(self, id):
        # Check if the WebSocket is already open
        if self.ws and self.ws.sock and self.ws.sock.connected:
            print("WebSocket is already connected.")
            # Send the payload over the existing WebSocket connection
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "tesstcreate",
                "messageType": "ParameterCreationRequest",
                "data": {
                    "parameterName": "MyNewParamName",
                    "explanation": "This is my new parameter.",
                    "min": -1,
                    "max": 1,
                    "defaultValue": 0
                }
            }
            print(payload)
            self.ws.send(json.dumps(payload))
            print("Sent load")  # This should now print
        else:
            print("WebSocket is not connected. Attempting to connect...")
            # If the WebSocket isn't connected, you can run the connection logic
            self._run_ws(self.on_open, self.on_message)


    def start_continuous_input(self, input_id="MyNewParamName", interval=0.1):
        print("started")
        def send_input(val):
            print(f"sending {val}")
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "mode": "set",
                    "parameterValues": [
                        {
                            "id": "MyNewParamName",
                            "value": val
                        }
                    ]
                }
            }
            self.ws.send(json.dumps(payload))


#fix this make it loop
        def send_loop():
            print("loop")
            t = 0
            while True:
                value = (math.sin(t) + 1) / 2  # Range: 0 to 1
                send_input(value)
                time.sleep(interval)
                t += 0.1

        # Start the input loop in the background only once
        if self.ws and self.ws.sock and self.ws.sock.connected:
            send_loop()
        else:
            print("WebSocket is not connected. Attempting to connect...")
            # If the WebSocket isn't connected, you can run the connection logic
            self._run_ws(self.on_open, self.on_message)



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
                self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=False)
                self.ws_thread.start()
