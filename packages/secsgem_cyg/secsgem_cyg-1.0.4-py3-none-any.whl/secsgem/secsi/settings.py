"""SECS-I settings class."""
from __future__ import annotations

import secsgem.common


class SecsISettings(secsgem.common.Settings):
    """Settings for SECS-I connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.secsi
        >>>
        >>> settings = secsgem.secsi.SecsISettings(port="COM1")
        >>> settings.port
        'COM1'
        >>> settings.speed
        9600

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._port = kwargs.get("port", "")
        self._speed = kwargs.get("speed", 9600)

    @property
    def port(self) -> str:
        """Serial port.

        Default: ""
        """
        return self._port

    @property
    def speed(self) -> int:
        """Serial port baud rate.

        Default: 9600
        """
        return self._speed

    def create_protocol(self) -> secsgem.common.Protocol:
        """Protocol class for this configuration."""
        from .protocol import SecsIProtocol  # pylint: disable=import-outside-toplevel

        return SecsIProtocol(self)

    def create_connection(self) -> secsgem.common.Connection:
        """Connection class for this configuration."""
        return secsgem.common.SerialConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"SECSI-{self.port}"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_SecsI_{functionality}_{self.port}@{self.speed}"
