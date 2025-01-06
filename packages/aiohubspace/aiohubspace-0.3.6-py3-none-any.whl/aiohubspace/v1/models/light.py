from contextlib import suppress
from dataclasses import dataclass, field

from ..models import features
from .resource import DeviceInformation, ResourceTypes


@dataclass
class Light[HubspaceResource]:
    """Representation of a Hubspace Light"""

    id: str  # ID used when interacting with Hubspace
    available: bool

    on: features.OnFeature
    color: features.ColorFeature
    color_mode: features.ColorModeFeature
    color_temperature: features.ColorTemperatureFeature
    dimming: features.DimmingFeature
    effect: features.EffectFeature

    # Defined at initialization
    instances: dict = field(default_factory=lambda: dict(), repr=False, init=False)
    device_information: DeviceInformation = field(default_factory=DeviceInformation)

    type: ResourceTypes = ResourceTypes.LIGHT

    def __init__(self, functions: list, **kwargs):
        for key, value in kwargs.items():
            if key == "instances":
                continue
            setattr(self, key, value)
        instances = {}
        for function in functions:
            with suppress(KeyError):
                if function["functionInstance"]:
                    instances[function["functionClass"]] = function["functionInstance"]
        self.instances = instances

    def get_instance(self, elem):
        """Lookup the instance associated with the elem"""
        return self.instances.get(elem, None)

    @property
    def supports_color(self) -> bool:
        """Return if this light supports color control."""
        return self.color is not None

    @property
    def supports_color_temperature(self) -> bool:
        """Return if this light supports color_temperature control."""
        return self.color_temperature is not None

    @property
    def supports_dimming(self) -> bool:
        """Return if this light supports brightness control."""
        return self.dimming is not None

    @property
    def supports_effects(self) -> bool:
        """Return if this light supports brightness control."""
        return self.effect is not None

    @property
    def supports_on(self):
        return self.on is not None

    @property
    def is_on(self) -> bool:
        """Return bool if light is currently powered on."""
        if self.on is not None:
            return self.on.on
        return False

    @property
    def brightness(self) -> float:
        """Return current brightness of light."""
        if self.dimming is not None:
            return self.dimming.brightness
        return 100.0 if self.is_on else 0.0


@dataclass
class LightPut[HubspaceResource]:
    """States that can be updated for a light"""

    on: features.OnFeature | None = None
    color: features.ColorFeature | None = None
    color_mode: features.ColorModeFeature | None = None
    color_temperature: features.ColorTemperatureFeature | None = None
    dimming: features.DimmingFeature | None = None
    effect: features.EffectFeature | None = None
