import asyncio
import base64
from io import BytesIO
from typing import ClassVar, List, Mapping, Optional

from inky import auto
from PIL import Image
from typing_extensions import Self
from viam.components.generic import Generic
from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import RESOURCE_TYPE_COMPONENT, Model, ModelFamily
from viam.utils import ValueTypes

LOGGER = getLogger(__name__)


class Inky(Generic):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("agavram", RESOURCE_TYPE_COMPONENT), "inky"
    )

    def __init__(self, name: str):
        self.dispatch = {
            "set_image": self.set_image,
            "set_border": self.set_border,
            "set_pixels": self.set_pixels,
            "get_resolution": self.get_resolution,
            "show": self.show,
        }
        super().__init__(name)

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        output = cls(config.name)
        output.reconfigure(config, dependencies)
        return output

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        self.display = auto()

    async def set_image(self, image: str):
        self.display.set_image(Image.open(BytesIO(base64.b64decode(image))))

    async def set_border(self, color: int):
        self.display.set_border(color)

    async def set_pixels(self, pixels: List[List[int]]):
        for x, y, v in pixels:
            self.display.set_pixel(int(x), int(y), int(v))

    async def get_resolution(self):
        return {
            "width": self.display.width,
            "height": self.display.height,
        }

    async def show(self):
        await asyncio.get_event_loop().run_in_executor(None, self.display.show)

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        args = dict(command)
        if args.get("command") in self.dispatch:
            result = await self.dispatch[args.pop("command")](**args)
            return {} if result is None else result
        raise ValueError(f"Unknown command received: {command}")
