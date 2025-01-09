import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseDevice:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _post_request(self, endpoint, data, json=False):
        try:
            url = self.base_url + endpoint
            data["auth_key"] = self.api_key
            response = requests.post(url, json=data if json else data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

class Relay(BaseDevice):
    def get_device(self, device_id):
        return self._post_request("device/status", {"id": device_id})

    def control_device(self, channel, turn, device_id):
        return self._post_request("device/relay/control", {
            "channel": channel,
            "turn": turn,
            "id": device_id,
        })

    def bulk_control_relays(self, devices):
        return self._post_request("device/relay/bulk_control", {"devices": devices}, json=True)

class Rollers(BaseDevice):
    def control_roller_direction(self, direction, device_id):
        return self._post_request("device/relay/roller/control", {
            "direction": direction,
            "id": device_id,
        })

    def control_roller_position(self, pos, device_id):
        if not (0 <= pos <= 100):
            raise ValueError("Position must be in the range [0..100]")
        return self._post_request("device/relay/roller/control", {
            "pos": pos,
            "id": device_id,
        })

    def bulk_control_rollers(self, devices):
        return self._post_request("device/roller/bulk_control", {"devices": devices}, json=True)

class Lights(BaseDevice):
    def control_light(self, device_id, **kwargs):
        data = {"id": device_id}
        for key, value in kwargs.items():
            if key in ["turn"] and value not in ["on", "off"]:
                raise ValueError(f"{key} must be 'on' or 'off'")
            if key in ["white", "red", "green", "blue"] and not (0 <= value <= 255):
                raise ValueError(f"{key} must be in the range [0..255]")
            if key == "gain" and not (0 <= value <= 100):
                raise ValueError(f"{key} must be in the range [0..100]")
            data[key] = value
        return self._post_request("device/light/control", data)

    def bulk_control_lights(self, devices):
        return self._post_request("device/light/bulk_control", {"devices": devices}, json=True)

class Connect:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        if not self.authenticate():
            raise ConnectionError("Failed to authenticate with the provided API key.")
        self.relays = Relay(base_url, api_key)
        self.rollers = Rollers(base_url, api_key)
        self.lights = Lights(base_url, api_key)

    def authenticate(self):
        response = requests.post(
            self.base_url + "/device/all_status?show_info=true&no_shared=true",
            data={"auth_key": self.api_key},
        )
        if response.status_code == 200:
            logger.info("Authentication successful.")
            return True
        else:
            logger.error("Authentication failed. Check your API key or base URL.")
            return False
