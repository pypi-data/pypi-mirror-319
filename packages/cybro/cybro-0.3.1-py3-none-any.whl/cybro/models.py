"""Models for Cybro scgi server objects."""  # fmt: skip
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any

from .exceptions import CybroError
from .exceptions import CybroPlcNotFoundError


@dataclass
class ServerInfo:  # pylint:
    """Cybro scgi server information."""

    server_uptime: str
    """server uptime, returned as "dd days, hh:mm:ss"""
    scgi_request_count: int
    """total number of requests served since server is started"""
    push_port_status: str
    """- "error", port already used by another application
    - "inactive", push disabled by configuration file
    - "active", push server is up and running"""
    push_count: int
    """total number of push messages received from controllers"""
    push_ack_errors: int
    """total number of push acknowledge errors"""
    push_list_count: int
    """total number of controllers in push list"""
    cache_request: int
    """configured read request time [s]"""
    cache_valid: int
    """configured cache validity time [s]"""
    server_version: str
    """returns "major.minor.release" """
    udp_rx_count: int
    """total number of messages received through UDP proxy"""
    udp_tx_count: int
    """total number of messages transmitted through UDP proxy"""
    nad_list: list[str]
    """active controllers, including static, push and autodetect"""
    push_list: str = ""
    """list of controllers in push list
    (nad, ip:port, plc status, plc program, alc file, resp time)"""
    datalogger_list: str = ""
    """list of variables for sample and alarm"""
    proxy_activity_list: str = ""
    """data for proxy activity"""

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ServerInfo:
        """generate ServerInfo object out of name / value dictionary

        Args:
            data: Received data from SCGI server.

        Returns:
            ServerInfo data.

        Raises:
            CybroError: The Cybro SCGI server returned no or incomlete Server info data.
        """
        try:
            return ServerInfo(
                server_uptime=data["sys.server_uptime"],
                scgi_request_count=data["sys.scgi_request_count"],
                push_port_status=data["sys.push_port_status"],
                push_count=data["sys.push_count"],
                push_ack_errors=data["sys.push_ack_errors"],
                push_list_count=data["sys.push_list_count"],
                cache_request=data["sys.cache_request"],
                cache_valid=data["sys.cache_valid"],
                server_version=data["sys.server_version"],
                udp_rx_count=data["sys.udp_rx_count"],
                udp_tx_count=data["sys.udp_tx_count"],
                nad_list=data["sys.nad_list"].get("item"),
            )
        except KeyError:
            raise CybroError("Not all ServerInfo tags found in data") from KeyError

    @staticmethod
    def from_vars(variables: dict[str, Var]) -> ServerInfo:
        """generate ServerInfo object out of name / Var object dictionary

        Args:
            variables: Received data from SCGI server.

        Returns:
            ServerInfo data.

        Raises:
            CybroError: The Cybro scgi server returned no or incomlete Server info data.
        """
        try:
            return ServerInfo(
                server_uptime=variables.get("sys.server_uptime").value,
                scgi_request_count=variables.get("sys.scgi_request_count").value,
                push_port_status=variables.get("sys.push_port_status").value,
                push_count=variables.get("sys.push_count").value,
                push_ack_errors=variables.get("sys.push_ack_errors").value,
                push_list_count=variables.get("sys.push_list_count").value,
                cache_request=variables.get("sys.cache_request").value,
                cache_valid=variables.get("sys.cache_valid").value,
                server_version=variables.get("sys.server_version").value,
                udp_rx_count=variables.get("sys.udp_rx_count").value,
                udp_tx_count=variables.get("sys.udp_tx_count").value,
                nad_list=variables.get("sys.nad_list").value.get("item"),
            )
        except AttributeError:
            raise CybroError(
                "Not all ServerInfo tags found in data"
            ) from AttributeError


@dataclass
class PlcInfo:  # pylint:
    """Cybro PLC information."""

    nad: int
    """Cybro PLC NAD"""
    ip_port: str
    """ip address and port, returned as "xxx.xxx.xxx.xxx:yyyy" """
    timestamp: str
    """time and date when the program is sent to controller"""
    plc_status: str
    """- "ok", controller is running
    - "pgm missing", controller has no plc program
    - "alc missing", controller has no alc file
    - "offline", controller does not respond
    - "?", status of the controller is unknown"""
    response_time: str
    """number of milliseconds elapsed between request and response"""
    bytes_transferred: int
    """number of bytes, read and write, transferred between server and controller"""
    com_error_count: int
    """total number of communication errors encountered by controller"""
    alc_file: str
    """allocation file, directly from the Cybro file system"""
    plc_vars: dict[str, str]
    """holds all plc vars (needs to be filled after generating PLCInfo object by calling parse_alc_file())"""

    @staticmethod
    def from_dict(data: dict[str, Any], plc_nad: int) -> PlcInfo:
        """generate PlcInfo object out of name / value dictionary

        Args:
            data: Received data from SCGI server.
            plc_nad: Address of PLC

        Returns:
            PlcInfo data.

        Raises:
            CybroPlcNotFoundError: The Cybro scgi server returned no or incomlete PLC data.
        """
        try:
            return PlcInfo(
                nad=plc_nad,
                ip_port=data["c" + str(plc_nad) + ".sys.ip_port"],
                timestamp=data["c" + str(plc_nad) + ".sys.timestamp"],
                plc_status=data["c" + str(plc_nad) + ".sys.plc_status"],
                response_time=data["c" + str(plc_nad) + ".sys.response_time"],
                bytes_transferred=data["c" + str(plc_nad) + ".sys.bytes_transferred"],
                com_error_count=data["c" + str(plc_nad) + ".sys.com_error_count"],
                alc_file=data["c" + str(plc_nad) + ".sys.alc_file"],
                plc_vars={},
            )
        except KeyError:
            raise CybroPlcNotFoundError(
                "Not all ServerInfo tags found in data"
            ) from KeyError

    @staticmethod
    def from_vars(variables: dict[str, Var], plc_nad: int) -> PlcInfo:
        """generate PlcInfo object out of name / Var object dictionary

        Args:
            variables: Force a full update from the device Device.
            plc_nad: Address of PLC

        Returns:
            PlcInfo data.

        Raises:
            CybroPlcNotFoundError: The Cybro scgi server returned no or incomlete PLC data.
        """
        nad = plc_nad
        try:
            return PlcInfo(
                nad=nad,
                ip_port=variables.get("c" + str(plc_nad) + ".sys.ip_port", "").value,
                timestamp=variables.get(
                    "c" + str(plc_nad) + ".sys.timestamp", ""
                ).value,
                plc_status=variables.get(
                    "c" + str(plc_nad) + ".sys.plc_status", ""
                ).value,
                response_time=variables.get(
                    "c" + str(plc_nad) + ".sys.response_time", ""
                ).value,
                bytes_transferred=variables.get(
                    "c" + str(plc_nad) + ".sys.bytes_transferred", ""
                ).value,
                com_error_count=variables.get(
                    "c" + str(plc_nad) + ".sys.com_error_count", ""
                ).value,
                alc_file=variables.get("c" + str(plc_nad) + ".sys.alc_file", "").value,
                plc_vars={},
            )
        except AttributeError:
            raise CybroPlcNotFoundError(
                f"Cybro PLC with NAD {nad} not found"
            ) from AttributeError

    def parse_alc_file(self) -> dict[str, str]:
        """Shall be called after update of PlcInfo to refresh list of all plc vars"""
        prefix = f"c{self.nad}."
        res: dict[str, str] = {}
        if self.alc_file is None:
            self.plc_vars = res
            return res
        alc_lines = self.alc_file.splitlines()
        for line in alc_lines[2:]:
            typ = line[37:43].rstrip()
            name = line[43:-1].split()[0].rstrip()
            res[f"{prefix}{name}"] = typ
            self.plc_vars = res
        return res


@dataclass
class Var:
    """object representing a scgi server variable"""

    name: str
    """name of variable"""
    value: str
    """value as string of variable"""
    description: str
    """description of the variable"""

    def __init__(self, name: str, value: str, description: str) -> None:
        self.name = name
        self.value = value
        self.description = description

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Var:
        """split a dict with "name", "value" and "description" into a Var object"""
        return Var(
            name=data.get("name"),
            value=data.get("value"),
            description=data.get("description"),
        )

    def value_string(self) -> str:
        """get current value"""
        return self.value

    def value_int(self) -> int:
        """get current value"""
        return int(self.value)

    def value_bool(self) -> bool:
        """get current value"""
        return bool(self.value == "1")

    def value_float(self) -> float:
        """get current value"""
        return float(self.value)


class Device:
    """Object holding all information of Cybro scgi server."""

    info: str
    server_info: ServerInfo
    plc_info: PlcInfo | None
    vars: dict[str, Var] = {}
    """list of variable / value / descriptions (after read/write)"""
    user_vars: dict[str, str] = {}
    """list of all variables to periodically update"""
    vars_types: dict[str, int] = {}
    """list of variable types"""

    def __init__(self, data: dict, plc_nad: int = 0) -> None:
        """Initialize an empty Cybro scgi server device class.

        Args:
            data: The full API response from a Cybro scgi server device.
            plc_nad: the Cybro PLC NAD

        Raises:
            CybroError: In case the given API response is incomplete in a way
                that a Device object cannot be constructed from it.
        """
        # Check if all elements are in the passed dict, else raise an Error
        try:
            if "var" in data:
                self.update_from_dict(data, plc_nad=plc_nad)
            else:
                raise CybroError(
                    "Cybro data is incomplete, cannot construct device object"
                )
        except TypeError as exc:
            raise CybroError(
                "Cybro data is incomplete, cannot construct device object"
            ) from exc

    def update_from_dict(self, data: dict, plc_nad: int = 0) -> Device:
        """Return Device object from Cybro scgi server response.

        Args:
            data: Update the device object with the data received from a
                Cybro scgi server request.
            plc_nad: Cybro PLC NAD

        Returns:
            The updated Device object.
        """
        # update server info
        for var in data["var"]:
            self.vars.update({var["name"]: Var.from_dict(var)})
            self.vars_types.update({var["name"]: 0})
        self.server_info = ServerInfo.from_vars(self.vars)
        self.info = "CybrotechScgiServer v" + self.server_info.server_version

        if plc_nad != 0:
            self.plc_info = PlcInfo.from_vars(self.vars, plc_nad)
            self.plc_info.parse_alc_file()

        return self

    def update_user_var_from_dict(self, data: dict) -> Device:
        """Parses user variables from Cybro scgi server response.

        Args:
            data: object with the data received from a
                Cybro scgi server request.

        Returns:
            The updated Device object.
        """
        # update user variable
        try:
            for _var in data["var"]:
                if _var == "name":
                    self.vars.update({data["var"]["name"]: Var.from_dict(data)})
                else:
                    self.vars.update({_var["name"]: Var.from_dict(_var)})
        except (KeyError, TypeError):
            pass
        return self

    def update_var(self, data: dict, var_type: VarType = 0) -> str | bool | int | float:
        """Return Value of a single var response.

        Args:
            data: Update the variable object with the data received from a
                Cybro scgi request.
            var_type: Type of read variable (default = str)

        Returns:
            The value of the var
        """
        try:
            for _var in data["var"]:
                if _var == "name":
                    # single var entry found
                    _var = data["var"]
                self.vars.update({_var["name"]: Var.from_dict(_var)})
                self.vars_types.update({_var["name"]: var_type})
                self.user_vars.update({_var["name"]: ""})
                return self.vars[_var["name"]].value
        except (KeyError, TypeError):
            pass
        return "?"

    def add_var(
        self, name: str, var_type: VarType = 0, allow_all: bool = False
    ) -> None:
        """Adds a variable to the update list.

        Args:
            name: Variable name to read eg: c1000.scan_time
            var_type: Optionally defines a Variable Type
            allow_all: Optionally allow to add also non existing variables"""
        if allow_all or name in self.plc_info.plc_vars or name.find(".sys.") != -1:
            self.user_vars.update({name: ""})
            self.vars_types.update({name: var_type})

    def remove_var(self, name: str) -> None:
        """Removes a variable from the read list.

        Args:
            name: Variable name to delete from user_vars"""
        self.user_vars.pop(name, "")
        self.vars_types.pop(name, "")


class VarType(IntEnum):
    """Enumeration representing variable types"""

    STR = 0
    INT = 1
    FLOAT = 2
    BOOL = 3
