import re
import time
from typing import Dict, List, Optional
from duckduckgo_search import DDGS
import ollama
from abc import ABC, abstractmethod
import yaml

from .utils import OutputType, PrettyOutput

class BaseModel(ABC):
    """大语言模型基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
        """执行对话"""
        pass

    @staticmethod
    def extract_tool_calls(content: str) -> List[Dict]:
        """从内容中提取工具调用，只返回第一个有效的工具调用"""
        # 分割内容为行
        lines = content.split('\n')
        tool_call_lines = []
        in_tool_call = False
        
        # 逐行处理
        for line in lines:
            if not line:
                continue
                
            if line == '<START_TOOL_CALL>':
                tool_call_lines = []
                in_tool_call = True
                continue
            elif line == '<END_TOOL_CALL>':
                if in_tool_call and tool_call_lines:
                    try:
                        # 解析工具调用内容
                        tool_call_text = '\n'.join(tool_call_lines)
                        tool_call_data = yaml.safe_load(tool_call_text)
                        
                        # 验证必要的字段
                        if "name" in tool_call_data and "arguments" in tool_call_data:
                            # 只返回第一个有效的工具调用
                            return [{
                                "function": {
                                    "name": tool_call_data["name"],
                                    "arguments": tool_call_data["arguments"]
                                }
                            }]
                    except yaml.YAMLError:
                        pass  # 跳过无效的YAML
                    except Exception:
                        pass  # 跳过其他错误
                in_tool_call = False
            elif in_tool_call:
                tool_call_lines.append(line)
        
        return []  # 如果没有找到有效的工具调用，返回空列表


class DDGSModel(BaseModel):
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        [1]: gpt-4o-mini
        [2]: claude-3-haiku
        [3]: llama-3.1-70b
        [4]: mixtral-8x7b
        """
        self.model_name = model_name

    def __make_prompt(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> str:
        prompt = ""
        for message in messages:
            prompt += f"[{message['role']}]: {message['content']}\n"
        return prompt

    def chat(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
        ddgs = DDGS()
        prompt = self.__make_prompt(messages, tools)
        content = ddgs.chat(prompt)
        PrettyOutput.print_stream(content, OutputType.SYSTEM)
        tool_calls = BaseModel.extract_tool_calls(content)
        return {
            "message": {
                "content": content,
                "tool_calls": tool_calls
            }
        }


class OllamaModel(BaseModel):
    """Ollama模型实现"""
    
    def __init__(self, model_name: str = "qwen2.5:14b", api_base: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_base = api_base
        self.client = ollama.Client(host=api_base)

    def chat(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
        """调用Ollama API获取响应"""
        try:
            # 使用流式调用
            stream = self.client.chat(
                model=self.model_name,
                messages=messages,
                stream=True
            )

            # 收集完整响应
            content_parts = []
            for chunk in stream:
                if chunk.message.content:
                    content_parts.append(chunk.message.content)
                    # 实时打印内容
                    PrettyOutput.print_stream(chunk.message.content, OutputType.SYSTEM)

            # 合并完整内容
            content = "".join(content_parts)
            tool_calls = BaseModel.extract_tool_calls(content)
            
            return {
                "message": {
                    "content": content,
                    "tool_calls": tool_calls
                }
            }
        except Exception as e:
            raise Exception(f"Ollama API调用失败: {str(e)}") 