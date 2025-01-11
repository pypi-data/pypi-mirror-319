import aiohttp
import json

API_TIMEOUT = 10
WSS_TIMEOUT = 10


class Apollo(object):
    def __init__(
            self,
            serial_number: str = None,
            host: str = None,
            password: str = "cyber2019",
            api_timeout: int = API_TIMEOUT,
            wss_timeout: int = WSS_TIMEOUT,
    ):
        self.api_timeout = api_timeout
        self.wss_timeout = wss_timeout
        self.serial_number = serial_number
        self.host = host
        self.uuid_url = "http://{}/register"
        self.sync_url = "http://{}/sync"
        self.data_url = "http://{}/data-ctrl"
        self.main_info_url = "http://{}/system-info"
        self._client_session = aiohttp.ClientSession()
        self.apollo_type = None
        self.password = password

    async def register_uuid(self):
        """Register a UUID."""
        data = {"user": self.serial_number,
                "password": self.password}
        json_data = json.dumps(data)
        for ind in range(3):
            if ind == 0:
                url = self.uuid_url.format("econest-hems-" + self.serial_number)
                self.apollo_type = "serial_number"
            elif ind == 1:
                url = self.uuid_url.format("econest-hems-" + self.serial_number + ".local")
                self.apollo_type = "serial_number_local"
            else:
                url = self.uuid_url.format(self.host)
                self.apollo_type = "host"
            try:
                async with self._client_session.post(url, timeout=self.api_timeout, data=json_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        res = data.get("uuid", None)
                        break
                    else:
                        res = None
                        continue
            except aiohttp.ClientError as e:
                res = None
                continue
        return res

    async def sync_data(self, device_uuid):
        """Sampling data synchronization settings"""
        data = {"uuid": device_uuid,
                "timestampFrom": 0,
                "timestampTo": 0}
        json_data = json.dumps(data)
        for ind in range(3):
            if ind == 0:
                url = self.sync_url.format("econest-hems-" + self.serial_number)
            elif ind == 1:
                url = self.sync_url.format("econest-hems-" + self.serial_number + ".local")
            else:
                url = self.sync_url.format(self.host)
            try:
                async with self._client_session.post(url, timeout=self.api_timeout, data=json_data) as response:
                    if response.status == 200:
                        res = True
                        break
                    else:
                        res = False
                        continue
            except aiohttp.ClientError as e:
                # 处理网络错误
                res = False
                continue
        return res

    async def data_ctrl(self, device_uuid):
        """Data transmission control"""
        data = {"uuid": device_uuid,
                "rtdataEnable": 1,
                "syncEnable": 0,
                "logdataEnable": 0}
        json_data = json.dumps(data)
        for ind in range(3):
            if ind == 0:
                url = self.data_url.format("econest-hems-" + self.serial_number)
            elif ind == 1:
                url = self.data_url.format("econest-hems-" + self.serial_number + ".local")
            else:
                url = self.data_url.format(self.host)
            try:
                async with self._client_session.post(url, timeout=self.api_timeout, data=json_data) as response:
                    if response.status == 200:
                        res = True
                        break
                    else:
                        res = False
                        continue
            except aiohttp.ClientError as e:
                # 处理网络错误
                res = False
                continue
        return res

    async def check_connection(self) -> bool:
        """Test connection."""
        for ind in range(3):
            if ind == 0:
                url = self.main_info_url.format("econest-hems-" + self.serial_number)
            elif ind == 1:
                url = self.main_info_url.format("econest-hems-" + self.serial_number + ".local")
            else:
                url = self.main_info_url.format(self.host)
            try:
                async with self._client_session.get(url, timeout=self.api_timeout) as response:
                    if response.status == 200:
                        res = True
                        break
                    else:
                        res = False
                        continue
            except aiohttp.ClientError as e:
                # 处理网络错误
                res = False
                continue
        return res


