from typing import Any, Union

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import redis


class ExecuteTool(Tool):
    conn = None
    def _conn(self, host, port, password, db=0):
        if not self.conn:
            self.conn = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)
        return self.conn

    def _invoke(self, tool_parameters: dict[str, Any]) -> Union[ToolInvokeMessage]:
        db = self.runtime.credentials.get("db")
        db = 0 if not db else int(db)
        port = int(self.runtime.credentials.get("port"))
        config = {
            "host": self.runtime.credentials.get("host"),
            "port": port,
            "password": self.runtime.credentials.get("password"),
            "db": db
        }
        command = tool_parameters.get("exec_command")
        if not command:
            # raise Exception("Error command required")
            return self.create_json_message({"msg": "执行命令必填！"})
        command = command.lower()
        command_list = command.split()
        result = self._conn(**config).execute_command(*command_list)
        result = {"result": result if result else str(result)}
        yield self.create_json_message(result)
