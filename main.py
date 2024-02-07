import asyncio

from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration

from display import Inky


async def main():
    Registry.register_resource_creator(
        Inky.SUBTYPE, Inky.MODEL, ResourceCreatorRegistration(Inky.new)
    )
    module = Module.from_args()

    module.add_model_from_registry(Inky.SUBTYPE, Inky.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
