"""Dataclasses for feeder data."""

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from pypetkitapi.const import DEVICE_DATA, PetkitEndpoint
from pypetkitapi.containers import Device, FirmwareDetail, Wifi


class Settings(BaseModel):
    """Dataclass for settings data."""

    auto_work: int | None = Field(None, alias="autoWork")
    lack_notify: int | None = Field(None, alias="lackNotify")
    light_mode: int | None = Field(None, alias="lightMode")
    light_range: list[int] | None = Field(None, alias="lightRange")
    log_notify: int | None = Field(None, alias="logNotify")
    manual_lock: int | None = Field(None, alias="manualLock")
    sound: int | None = None
    temp_unit: int | None = Field(None, alias="tempUnit")


class State(BaseModel):
    """Dataclass for state data."""

    humidity: int | None = None
    left_day: int | None = Field(None, alias="leftDay")
    liquid: int | None = None
    mode: int | None = None
    ota: int | None = None
    overall: int | None = None
    pim: int | None = None
    power: int | None = None
    refresh: float | None = None
    temp: int | None = None
    wifi: Wifi | None = None


class Purifier(BaseModel):
    """Dataclass for feeder data."""

    data_type: ClassVar[str] = DEVICE_DATA

    bt_mac: str | None = Field(None, alias="btMac")
    created_at: str | None = Field(None, alias="createdAt")
    firmware: str | None = None
    firmware_details: list[FirmwareDetail] | None = Field(None, alias="firmwareDetails")
    hardware: int | None = None
    id: int | None = None
    locale: str | None = None
    mac: str | None = None
    name: str | None = None
    relation: dict[str, str]
    secret: str | None = None
    settings: Settings | None = None
    share_open: int | None = Field(None, alias="shareOpen")
    signup_at: str | None = Field(None, alias="signupAt")
    sn: str | None = None
    state: State | None = None
    timezone: float | None = None
    work_time: list[tuple[int, int]] | None = Field(None, alias="workTime")
    device_nfo: Device | None = None

    @classmethod
    def get_endpoint(cls, device_type: str) -> str:
        """Get the endpoint URL for the given device type."""
        return PetkitEndpoint.DEVICE_DETAIL

    @classmethod
    def query_param(
        cls,
        device: Device,
        device_data: Any | None = None,
    ) -> dict:
        """Generate query parameters including request_date."""
        return {"id": int(device.device_id)}
