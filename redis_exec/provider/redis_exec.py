from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.execute import ExecuteTool


class RedisExecProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            for _ in ExecuteTool.from_credentials(credentials).invoke(tool_parameters={}):
                pass
        except Exception as e:
            print(f"执行异常：{e}")
            raise ToolProviderCredentialValidationError(str(e))
