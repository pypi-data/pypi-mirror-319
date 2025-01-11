from typing import Dict, Any
import os
import tempfile
import shlex
from pathlib import Path
from ..utils import PrettyOutput, OutputType

class ShellTool:
    name = "execute_shell"
    description = """Execute shell commands and return the results.

Guidelines:
1. Filter outputs
   - Use grep/sed for specific data
   - Use head/tail to limit lines
   - Use -q for status checks

Examples:
✓ <START_TOOL_CALL>
name: execute_shell
arguments:
    command: ls -l file.txt  # specific file
<END_TOOL_CALL>

✗ <START_TOOL_CALL>
name: execute_shell
arguments:
    command: ps aux  # too much output
<END_TOOL_CALL>"""

    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute (filter output when possible)"
            }
        },
        "required": ["command"]
    }

    def _escape_command(self, cmd: str) -> str:
        """转义命令中的特殊字符"""
        # 将命令中的单引号替换为'"'"'
        return cmd.replace("'", "'\"'\"'")

    def execute(self, args: Dict) -> Dict[str, Any]:
        """执行shell命令"""
        try:
            command = args["command"]
            
            # 生成临时文件名
            output_file = os.path.join(tempfile.gettempdir(), f"jarvis_shell_{os.getpid()}.log")
            
            # 转义命令中的特殊字符
            escaped_command = self._escape_command(command)
            
            # 修改命令以使用script
            tee_command = f"script -q -c '{escaped_command}' {output_file}"
            
            PrettyOutput.print(f"执行命令: {command}", OutputType.INFO)
            
            # 执行命令
            return_code = os.system(tee_command)
            
            # 读取输出文件
            try:
                with open(output_file, 'r', encoding='utf-8', errors='replace') as f:
                    output = f.read()
                    # 移除script命令添加的头尾
                    if output:
                        lines = output.splitlines()
                        if len(lines) > 2:
                            output = "\n".join(lines[1:-1])
            except Exception as e:
                output = f"读取输出文件失败: {str(e)}"
            finally:
                # 清理临时文件
                Path(output_file).unlink(missing_ok=True)
            
            return {
                "success": return_code == 0,
                "stdout": output,
                "stderr": "",
                "return_code": return_code
            }
                
        except Exception as e:
            # 确保清理临时文件
            if 'output_file' in locals():
                Path(output_file).unlink(missing_ok=True)
            return {
                "success": False,
                "error": str(e)
            } 