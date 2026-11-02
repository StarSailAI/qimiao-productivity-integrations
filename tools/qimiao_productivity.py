from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from qimiao_client import invoke


class QimiaoProductivityTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        result = invoke(tool_parameters.get("operation", "list_tools"), tool_parameters.get("arguments_json", "{}"))
        yield self.create_json_message(result)
