import requests
import logging

class UserAction:
    def __init__(self, api_key):
        self.api_key = api_key
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Common headers for all API requests
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"KISI-LOGIN {self.api_key}",
            "Content-Type": "application/json"
        }

        # Base URL for user-related actions
        self.base_url = 'https://api.kisi.io/users'

    def _send_request(self, method, endpoint='', data=None, params=None):
        url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        try:
            response = requests.request(method, url, headers=self.headers, json=data, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error with {method} request to {url}: {e}")
            return None

    def fetch_users(self, confirmed=None, group_id=None, ids=None, limit=50, offset=0, place_id=None,
                    query=None, sort=None, user_id=None):
        params = {
            "confirmed": confirmed,
            "group_id": group_id,
            "ids": ids,
            "limit": limit,
            "offset": offset,
            "place_id": place_id,
            "query": query,
            "sort": sort,
            "user_id": user_id
        }
        return self._send_request("GET", "", params=params)

    def create_user(self, name, email, image=None, send_emails=None, confirm=None, access_enabled=None,
                    password_flow_enabled=None, metadata=None, notes=None):
        data = {
            "user": {
                "name": name,
                "email": email,
                "image": image,
                "send_emails": send_emails,
                "confirm": confirm,
                "access_enabled": access_enabled,
                "password_flow_enabled": password_flow_enabled,
                "metadata": metadata,
                "notes": notes
            }
        }
        data["user"] = {k: v for k, v in data["user"].items() if v is not None}
        return self._send_request("POST", "", data=data)

    def fetch_user(self, user_id):
        return self._send_request("GET", str(user_id))

    def update_user(self, user_id, name=None, image=None, access_enabled=None, password_flow_enabled=None,
                    metadata=None, notes=None):
        data = {
            "user": {
                "name": name,
                "image": image,
                "access_enabled": access_enabled,
                "password_flow_enabled": password_flow_enabled,
                "metadata": metadata,
                "notes": notes
            }
        }
        data["user"] = {k: v for k, v in data["user"].items() if v is not None}
        return self._send_request("PATCH", str(user_id), data=data)

    def delete_user(self, user_id):
        return self._send_request("DELETE", str(user_id))

    def fetch_current_user(self):
        return self._send_request("GET", "user")

    def update_current_user(self, name=None, image=None, last_read_at=None, locale=None, current_password=None,
                            password=None, password_confirmation=None):
        data = {
            "user": {
                "name": name,
                "image": image,
                "last_read_at": last_read_at,
                "locale": locale,
                "current_password": current_password,
                "password": password,
                "password_confirmation": password_confirmation
            }
        }
        data["user"] = {k: v for k, v in data["user"].items() if v is not None}
        return self._send_request("PATCH", "user", data=data)

    def delete_current_user(self):
        return self._send_request("DELETE", "user")

    def register_user(self, name, email, password, terms_and_conditions, token=None, image=None):
        data = {
            "user": {
                "name": name,
                "email": email,
                "password": password,
                "terms_and_conditions": terms_and_conditions,
                "token": token,
                "image": image
            }
        }
        data["user"] = {k: v for k, v in data["user"].items() if v is not None}
        return self._send_request("POST", "sign_up", data=data)

class GroupAction:
    def __init__(self, api_key):
        self.api_key = api_key
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Common headers for all API requests
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"KISI-LOGIN {self.api_key}",
            "Content-Type": "application/json"
        }

        # Base URL for group-related actions
        self.base_url = 'https://api.kisi.io/groups'

    def _send_request(self, method, endpoint='', data=None, params=None):
        url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        try:
            response = requests.request(method, url, headers=self.headers, json=data, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error with {method} request to {url}: {e}")
            return None

    def fetch_groups(self, ids=None, query=None, limit=10, offset=0, scope=None, place_id=None,
                     elevator_stop_id=None, lock_id=None, sort=None):
        params = {
            "ids": ids,
            "query": query,
            "limit": limit,
            "offset": offset,
            "scope": scope,
            "place_id": place_id,
            "elevator_stop_id": elevator_stop_id,
            "lock_id": lock_id,
            "sort": sort
        }
        return self._send_request("GET", "", params=params)

    def create_group(self, name, description=None, place_id=None, login_enabled=False,
                     geofence_restriction_enabled=False, primary_device_restriction_enabled=False,
                     managed_device_restriction_enabled=False, reader_restriction_enabled=False,
                     time_restriction_enabled=False):
        payload = {
            "group": {
                "name": name,
                "description": description,
                "place_id": place_id,
                "login_enabled": login_enabled,
                "geofence_restriction_enabled": geofence_restriction_enabled,
                "primary_device_restriction_enabled": primary_device_restriction_enabled,
                "managed_device_restriction_enabled": managed_device_restriction_enabled,
                "reader_restriction_enabled": reader_restriction_enabled,
                "time_restriction_enabled": time_restriction_enabled
            }
        }
        return self._send_request("POST", "", data=payload)

    def fetch_group(self, group_id):
        return self._send_request("GET", str(group_id))

    def update_group(self, group_id, name=None, description=None, login_enabled=None,
                     geofence_restriction_enabled=None, primary_device_restriction_enabled=None,
                     managed_device_restriction_enabled=None, reader_restriction_enabled=None,
                     time_restriction_enabled=None):
        data = {
            "group": {
                "name": name,
                "description": description,
                "login_enabled": login_enabled,
                "geofence_restriction_enabled": geofence_restriction_enabled,
                "primary_device_restriction_enabled": primary_device_restriction_enabled,
                "managed_device_restriction_enabled": managed_device_restriction_enabled,
                "reader_restriction_enabled": reader_restriction_enabled,
                "time_restriction_enabled": time_restriction_enabled
            }
        }
        data["group"] = {k: v for k, v in data["group"].items() if v is not None}
        return self._send_request("PATCH", str(group_id), data=data)

    def delete_group(self, group_id):
        return self._send_request("DELETE", str(group_id))

class CardAction:
    def __init__(self, api_key):
        self.api_key = api_key
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Common headers for all API requests
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"KISI-LOGIN {self.api_key}",
            "Content-Type": "application/json"
        }

        # Base URL for card-related actions
        self.base_url = 'https://api.kisi.io/cards'

    def _send_request(self, method, endpoint='', data=None, params=None):
        url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        try:
            response = requests.request(method, url, headers=self.headers, json=data, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error with {method} request to {url}: {e}")
            return None

    def fetch_cards(self, card_id=None, card_number=None, facility_code=None, ids=None, limit=10, offset=0,
                    sort=None, token=None, uid=None, user_id=None):
        params = {
            "card_id": card_id,
            "card_number": card_number,
            "facility_code": facility_code,
            "ids": ids,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "token": token,
            "uid": uid,
            "user_id": user_id
        }
        # Remove keys with None values to avoid sending them in the query parameters
        params = {k: v for k, v in params.items() if v is not None}
        return self._send_request("GET", "", params=params)

    def create_card(self, token, card_type):
        data = {
            "card": {
                "token": token,
                "type": card_type
            }
        }
        return self._send_request("POST", "", data=data)

    def fetch_card(self, card_id):
        return self._send_request("GET", str(card_id))

    def delete_card(self, card_id):
        return self._send_request("DELETE", str(card_id))

    def update_card(self, card_id, two_factor_pin=None, send_two_factor_pin_notification=None):
        data = {}
        if two_factor_pin is not None:
            data['two_factor_pin'] = two_factor_pin
        if send_two_factor_pin_notification is not None:
            data['send_two_factor_pin_notification'] = send_two_factor_pin_notification
        return self._send_request("PATCH", str(card_id), data={"card": data})

class CalendarAction:
    def __init__(self, api_key):
        self.api_key = api_key
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Common headers for all API requests
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }

        # Base URL for calendar-related actions
        self.base_url = 'https://api.kisi.io/calendar'

    def _send_request(self, method, endpoint='', data=None, params=None):
        url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        try:
            response = requests.request(method, url, headers=self.headers, json=data, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error with {method} request to {url}: {e}")
            return None

    def fetch_summary(self, around, consequence, elevator_stop_id=None, group_id=None, lock_id=None):
        params = {
            "around": around,
            "consequence": consequence,
            "elevator_stop_id": elevator_stop_id,
            "group_id": group_id,
            "lock_id": lock_id
        }
        # Remove keys with None values to avoid sending them in the query parameters
        params = {k: v for k, v in params.items() if v is not None}
        return self._send_request("GET", "summary", params=params)

class CameraAction:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _send_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.request(method, url, headers=headers, json=data, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error with {method} request to {url}: {e}")
            return None

    def fetch_cameras(self, floor_id=None, ids=None, place_id=None, sort='name'):
        params = {
            "ids": ids,
            "floor_id": floor_id,
            "place_id": place_id,
            "sort": sort
        }
        params = {k: v for k, v in params.items() if v is not None}  # Remove None values
        return self._send_request("GET", "cameras", params=params)

    def create_camera(self, lock_id, remote_id, name=None, clip_duration=None, description=None, enabled=True,
                      number_of_snapshots=None, supports_thumbnails=True, place_id=None, snapshot_offset=None,
                      supports_clips=True, supports_images=True):
        data = {
            "camera": {
                "clip_duration": clip_duration,
                "description": description,
                "enabled": enabled,
                "lock_id": lock_id,
                "name": name,
                "number_of_snapshots": number_of_snapshots,
                "place_id": place_id,
                "remote_id": remote_id,
                "snapshot_offset": snapshot_offset,
                "supports_clips": supports_clips,
                "supports_images": supports_images,
                "supports_thumbnails": supports_thumbnails
            }
        }
        return self._send_request("POST", "cameras", data=data)

    def fetch_camera(self, camera_id):
        return self._send_request("GET", f"cameras/{camera_id}")

    def update_camera(self, camera_id, clip_duration=None, description=None, lock_id=None, name=None,
                      number_of_snapshots=None, snapshot_offset=None, supports_clips=True, supports_images=True,
                      supports_thumbnails=True, enabled=True):
        data = {
            "camera": {
                "clip_duration": clip_duration,
                "description": description,
                "enabled": enabled,
                "lock_id": lock_id,
                "name": name,
                "number_of_snapshots": number_of_snapshots,
                "snapshot_offset": snapshot_offset,
                "supports_clips": supports_clips,
                "supports_images": supports_images,
                "supports_thumbnails": supports_thumbnails
            }
        }
        data["camera"] = {k: v for k, v in data["camera"].items() if v is not None}  # Remove None values
        return self._send_request("PATCH", f"cameras/{camera_id}", data=data)

    def delete_camera(self, camera_id):
        return self._send_request("DELETE", f"cameras/{camera_id}")

    def fetch_video_link(self, camera_id, timestamp=None):
        params = {"timestamp": timestamp} if timestamp else {}
        return self._send_request("GET", f"cameras/{camera_id}/video_link", params=params)

import requests

class LockAction:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.kisi.io/locks'
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"KISI-LOGIN {self.api_key}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return None

    def _clean_params(self, params):
        """Remove None values from the parameters."""
        return {k: v for k, v in params.items() if v is not None}

    def fetch_locks(self, **params):
        params = self._clean_params(params)
        response = requests.get(self.base_url, headers=self.headers, params=params)
        return self._handle_response(response)

    def create_lock(self, name, place_id, **params):
        data = {
            "lock": {
                "name": name,
                "place_id": place_id,
                **params  # Add additional params dynamically
            }
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return self._handle_response(response)

    def fetch_lock(self, lock_id, **params):
        url = f'{self.base_url}/{lock_id}'
        params = self._clean_params(params)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def update_lock(self, lock_id, **params):
        url = f'{self.base_url}/{lock_id}'
        data = {
            "lock": self._clean_params(params)
        }
        response = requests.patch(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete_lock(self, lock_id):
        url = f'{self.base_url}/{lock_id}'
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def unlock_lock(self, lock_id, latitude, longitude, proximity_proof=None):
        url = f'{self.base_url}/{lock_id}/unlock'
        data = {
            "context": {"location": {"latitude": latitude, "longitude": longitude}},
            "lock": {"proximity_proof": proximity_proof}
        }
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def lock_down_lock(self, lock_id):
        url = f'{self.base_url}/{lock_id}/lock_down'
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response)

    def cancel_lockdown(self, lock_id):
        url = f'{self.base_url}/{lock_id}/cancel_lockdown'
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response)


class Connect:
    def __init__(self , api_key):
        self.base_url = 'https://api.kisi.io'
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {api_key}"
        }

        self._authenticate()

        # Initialize other actions
        self.group = GroupAction(api_key)
        self.calendar = CalendarAction(api_key)
        self.camera = CameraAction(self.base_url , api_key)
        self.lock = LockAction(api_key)
        self.user = UserAction(api_key)

    def _authenticate(self):
        """Handles authentication with the Kisi API."""
        url = f'{self.base_url}/organizations'
        response = requests.get(url , headers=self.headers)

        if response.status_code != 200:
            print('Error while authenticating')
            data = response.json()
            print(data)
            raise Exception('Authentication failed')
