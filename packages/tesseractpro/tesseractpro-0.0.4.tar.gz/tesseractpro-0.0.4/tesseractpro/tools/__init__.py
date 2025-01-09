
from ..base import Base
from ..decorators.on import on
from .basetool import BaseTool
from .turningpoint import TurningPoint


class Tools (Base):
    @on("tool:add")
    def on_tools_added(self, data) -> None:
        self.emit('add', data)

    @on("tool:update")
    def on_tool_update(self, data) -> None:
        self.emit('update', data)

    @on("tool:remove")
    def on_tool_remove(self, data) -> None:
        self.emit('remove', data)

    def get_tools(
            self,
            from_unix: int,
            to_unix: int,
            timeframe: int,
            market: str,
            space_id: str
    ):
        """
        Return tools for the given parameters
        """
        data = self._tpro.rest.post("tools", {
            "to": to_unix,
            "from": from_unix,
            "timeframe": timeframe * 60,
            "market": market,
            "space_id": space_id
        })

        tools = []

        for item in data:
            match item['type']:
                case 'turningpoint':
                    tools.append(TurningPoint(item))
                case _:
                    tools.append(BaseTool(item))

        return tools
