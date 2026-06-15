# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project
"""Connection configuration for the object store secondary tier."""

from dataclasses import dataclass
from enum import Enum


class ObjStoreNixlBackend(str, Enum):
    """NIXL backend plugins supported by the object store secondary tier."""

    OBJ = "obj"
    DOCA_MEMOS = "doca_memos"

    @classmethod
    def from_value(cls, value: object) -> "ObjStoreNixlBackend":
        """Parse a user-provided backend selector.

        Args:
            value: Object-tier ``nixl_backend`` configuration value.

        Returns:
            The parsed NIXL backend selector.

        Raises:
            ValueError: If ``value`` is not a supported backend selector.
        """
        if isinstance(value, cls):
            return value
        try:
            return cls(value)
        except ValueError as exc:
            supported = ", ".join(repr(backend.value) for backend in cls)
            raise ValueError(
                f"Unsupported object-store NIXL backend {value!r}. "
                f"Supported values: {supported}."
            ) from exc


@dataclass
class ObjStoreConfig:
    """Connection parameters for an object store backend."""

    bucket: str
    endpoint_override: str
    access_key: str
    secret_key: str
    scheme: str = "http"
    ca_bundle: str = ""
    nixl_backend: ObjStoreNixlBackend = ObjStoreNixlBackend.OBJ

    def __post_init__(self) -> None:
        self.nixl_backend = ObjStoreNixlBackend.from_value(self.nixl_backend)

    def to_nixl_params(self) -> dict[str, str]:
        """Build the NIXL backend params dict."""
        params: dict[str, str] = {
            "bucket": self.bucket,
            "endpoint_override": self.endpoint_override,
            "scheme": self.scheme,
            "access_key": self.access_key,
            "secret_key": self.secret_key,
        }
        if self.ca_bundle:
            params["ca_bundle"] = self.ca_bundle
        return params


@dataclass
class MemosStoreConfig:
    """Connection parameters for a DOCA Memos backend."""

    device_name: str
    num_tasks: str
    n_guid: str
    ignore_read_not_found: str
    query_mem_mode: str
    nixl_backend: ObjStoreNixlBackend = ObjStoreNixlBackend.DOCA_MEMOS

    def __post_init__(self) -> None:
        self.nixl_backend = ObjStoreNixlBackend.from_value(self.nixl_backend)

    def to_nixl_params(self) -> dict[str, str]:
        """Build the NIXL backend params dict."""
        params: dict[str, str] = {
            "device_name": self.device_name,
            "num_tasks": self.num_tasks,
            "n_guid": self.n_guid,
            "ignore_read_not_found": self.ignore_read_not_found,
            "query_mem_mode": self.query_mem_mode,
            "convert_key_to_128bit": "true"
        }
        return params
