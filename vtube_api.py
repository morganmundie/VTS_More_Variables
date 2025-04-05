import json
import threading
import os
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

    def _load_token(self):
        print(self.token_file)
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
                    "pluginDeveloper": "MorganMundie"
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

    def _run_ws(self, on_open, on_message=None):
        def default_on_message(ws, message):
            if self.on_message_callback:
                self.on_message_callback(message)
            ws.close()

        def on_error(ws, error):
            if self.on_error_callback:
                self.on_error_callback(str(error))

        self.ws = WebSocketApp(
            self.ws_url,
            on_open=on_open,
            on_message=on_message or default_on_message,
            on_error=on_error
        )
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
