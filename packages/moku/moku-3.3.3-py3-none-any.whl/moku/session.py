import json
from collections import namedtuple
from functools import wraps

from requests import Session

from . import exceptions


def handle_response(func):
    """
    Decorator which parses the response returned
    by Moku API Server
    """

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        return self.resolve(response)

    return func_wrapper


class RequestSession:
    "Base HTTP Requests class"
    json_headers = {"Content-type": "application/json"}
    sk_name = "Moku-Client-Key"  # session key name

    def __init__(self, ip, connect_timeout, read_timeout, **kwargs):
        self.ip_address = ip
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.rs = Session()

        # support arbitrary session arguments
        for k, v in kwargs.items():
            if k.lower().startswith("session_"):
                k = k.split("session_")[1]
                setattr(self.rs, k, v)

    def update_sk(self, response):
        key = response.headers.get(self.sk_name)
        if key:
            self.session_key = key
            self.rs.headers.update({self.sk_name: key})

    def url_for(self, group, operation):
        return f"http://{self.ip_address}/api/{group}/{operation}"

    def url_for_v2(self, location):
        return f"http://{self.ip_address}/api/v2/{location}"

    def timeout_headers(self, rt_increase=0):
        "Returns timeout headers required for http request"
        return tuple([self.connect_timeout, self.read_timeout + rt_increase])

    @handle_response
    def get(self, group, operation):
        "Executes get call and returns the response"
        return self.rs.get(
            self.url_for(group, operation), timeout=self.timeout_headers()
        )

    @handle_response
    def post(self, group, operation, params=None):
        "Executes post call and returns the response"
        # As get_data has an explicit read_timeout parameter,
        # it should be considered applicable cases, in all other
        # cases default it to 0
        _timeout = None
        if params:
            _timeout = params.get("timeout", 0)
        _to_inc = 0 if not _timeout else _timeout
        return self.rs.post(
            self.url_for(group, operation),
            json=params,
            timeout=self.timeout_headers(_to_inc),
            headers=self.json_headers,
        )

    @handle_response
    def post_raw_json(self, group, operation, data):
        "Executes post call and returns the response"
        return self.rs.post(
            self.url_for(group, operation),
            json=data,
            headers=self.json_headers,
        )

    def post_to_v2_raw(self, location, params=None):
        "Executes post call to api v2 and returns the response"
        response = self.rs.post(self.url_for_v2(location), json=params)
        return response

    def post_to_v2(self, location, params=None):
        response = self.rs.post(self.url_for_v2(location), json=params)
        if response.status_code != 200:
            raise exceptions.MokuException(
                f"Cannot fulfil request, error code " f"{response.status_code}"
            )
        return response.json()

    def get_file(self, group, operation, local_path):
        with self.rs.get(self.url_for(group, operation), stream=True) as r:
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    @handle_response
    def post_file(self, group, operation, data):
        return self.rs.post(
            self.url_for(group, operation), data=data, timeout=self.timeout_headers()
        )

    @handle_response
    def delete_file(self, group, operation):
        "Deletes the given file from the Moku"
        return self.rs.delete(
            self.url_for(group, operation), timeout=self.timeout_headers()
        )

    @staticmethod
    def _handle_error(code, messages):
        if code == "NO_PLATFORM_BIT_STREAM":
            raise exceptions.NoPlatformBitstream(messages)
        elif code == "NO_BIT_STREAM":
            raise exceptions.NoInstrumentBitstream(messages)
        elif code == "INVALID_PARAM":
            raise exceptions.InvalidParameterException(messages)
        elif code == "INVALID_REQUEST":
            raise exceptions.InvalidRequestException(messages)
        elif code == "NETWORK_ERROR":
            raise exceptions.NetworkError(messages)
        elif code == "UNEXPECTED_CHANGE":
            raise exceptions.UnexpectedChangeError(messages)
        else:
            raise exceptions.MokuException(messages)

    @staticmethod
    def echo_warnings(messages):
        "Prints any warnings received from Moku"
        for m in messages or []:
            print(f"Warning: {m}")

    @staticmethod
    def _normalize_nan_inf(arg):
        return {"-inf": -float("inf"), "inf": float("inf"), "nan": float("nan")}[arg]

    def _check_and_normalize_nan_inf(self, content):
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError:
            content = content.replace("nan", '"nan"')
            content = content.replace("inf", '"inf"')
            return json.loads(content, parse_constant=self._normalize_nan_inf)

    def resolve(self, response):
        "Resolves response received"

        def _parse_to_object(content):
            content = content.decode("utf-8")
            content = self._check_and_normalize_nan_inf(content)
            return namedtuple("_", content.keys())(*content.values())

        key = response.headers.get(self.sk_name)
        if key:
            self.rs.headers.update({self.sk_name: key})
        if response.status_code == 200:
            data = _parse_to_object(response.content)
            if data.success is True:
                self.echo_warnings(data.messages)
                return data.data
            elif data.success is False:
                self._handle_error(data.code, data.messages)
        else:
            print(response.__dict__)
            if response.status_code == 500:
                raise exceptions.MokuException("Unhandled error received from Moku.")
            if response.status_code == 502:
                raise exceptions.MokuException(
                    "Can't connect the API server. Please check your Moku has the API server app installed by running `mokucli update`"
                )
            if response.status_code == 504:
                raise exceptions.MokuException(
                    "Timeout before receiving response"
                )
            if response.status_code == 404:
                raise exceptions.OperationNotFound(
                    "Method not found. Make sure Python Client is compatible with the firmware version running"
                )  # noqa
            else:
                raise exceptions.MokuException(
                    f"Unknown exception. " f"Status code:{response.status_code}"
                )
