from typing import Any
from dify_plugin import ToolProvider


class QimiaoProductivityProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # Public discovery needs no provider API key. Task credentials are per call.
        return None
