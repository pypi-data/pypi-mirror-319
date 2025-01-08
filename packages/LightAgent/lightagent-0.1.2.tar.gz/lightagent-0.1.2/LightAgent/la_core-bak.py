import json
import os
import time
import httpx
from loguru import logger
import inspect
import traceback
import requests
from typing import Callable, Any, Dict
import json
from datetime import datetime
from openai import OpenAI
from colorama import init, Fore

# Global registry for tools
from typing import List, Dict, Any, Callable
from copy import deepcopy

import os
import json
from datetime import datetime
from typing import Optional
import httpx
from openai import OpenAI
from colorama import Fore

# 全局工具注册表
_FUNCTION_MAPPINGS = {}  # 工具名称 -> 工具函数
_OPENAI_FUNCTION_SCHEMAS = []  # OpenAI 格式的工具描述
_PROMPT_FUNCTION_SCHEMAS = []  # prompt 格式的工具描述

def register_tool_manually(tools: List[Callable]) -> None:
    """
    手动注册多个工具，从函数属性中提取工具信息
    :param tools: 工具函数列表
    """
    for func in tools:
        if not hasattr(func, "tool_info"):
            raise ValueError(f"Function `{func.__name__}` does not have tool_info attribute.")

        tool_info = func.tool_info
        tool_name = tool_info["tool_name"]
        _FUNCTION_MAPPINGS[tool_name] = func  # 注册工具

        # 构建 OpenAI 格式的工具描述
        tool_params_openai = {}
        tool_required = []
        for param in tool_info["tool_params"]:
            tool_params_openai[param["name"]] = {
                "type": param["type"],
                "description": param["description"],
            }
            if param["required"]:
                tool_required.append(param["name"])

        tool_def_openai = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_info["tool_description"],
                "parameters": {
                    "type": "object",
                    "properties": tool_params_openai,
                    "required": tool_required,
                },
            }
        }

        _OPENAI_FUNCTION_SCHEMAS.append(tool_def_openai)

def dispatch_tool(tool_name: str, tool_params: Dict[str, Any]) -> str:
    """
    调用工具
    """
    if tool_name not in _FUNCTION_MAPPINGS:
        return f"Tool `{tool_name}` not found."

    tool_call = _FUNCTION_MAPPINGS[tool_name]
    try:
        print(f"Calling tool: {tool_name} with params: {tool_params}")  # 调试信息
        return str(tool_call(**tool_params))
    except Exception as e:
        print(f"Tool call failed: {e}")  # 调试信息
        return traceback.format_exc()

def get_tools() -> List[Dict[str, Any]]:
    """
    获取所有工具的描述（OpenAI 格式）
    """
    return deepcopy(_OPENAI_FUNCTION_SCHEMAS)

def get_tools_str() -> str:
    """
    将 _OPENAI_FUNCTION_SCHEMAS 转换为格式化的 JSON 字符串。
    Returns:
        str: 格式化的 JSON 字符串。
    """
    # 使用 json.dumps 将字典转换为格式化的 JSON 字符串
    tools_str = json.dumps(_OPENAI_FUNCTION_SCHEMAS, indent=4, ensure_ascii=False)
    return tools_str

class MultiAgentSystem:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("MultiAgentSystem must implement the __call__ method.")


class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Tool must implement the __call__ method.")


class LightAgent:
    # client options
    api_key: str
    organization: Optional[str]
    project: Optional[str]
    websocket_base_url: Optional[httpx.URL]

    def __init__(
            self,
            *,
            role: Optional[str] = None,
            model: str,
            api_key: str,
            base_url: Optional[httpx.URL] = None,
            websocket_base_url: Optional[httpx.URL] = None,
            memory=None,  # 支持外部传入记忆模块
            chain_of_thought: bool = False,
            debug: bool = False,  # 是否启用调试模式
            log_level: str = "INFO",  # 日志级别（INFO, DEBUG, ERROR）
            log_file: Optional[str] = None  # 日志文件路径
    ) -> None:
        """
        初始化 LightAgent。

        :param role: Agent 的角色描述。
        :param model: 使用的模型名称。
        :param api_key: API 密钥。
        :param base_url: API 的基础 URL。
        :param websocket_base_url: WebSocket 的基础 URL。
        :param memory: 外部传入的记忆模块，需实现 `retrieve` 和 `store` 方法。
        :param chain_of_thought: 是否启用思维链功能。
        :param debug: 是否启用调试模式。
        :param log_level: 日志级别（INFO, DEBUG, ERROR）。
        :param log_file: 日志文件路径。
        """
        if not model:
            raise ValueError("The 'model' parameter must be provided.")
        if not api_key:
            raise ValueError("The 'api_key' parameter must be provided.")

        self.role = role
        self.model = model
        self.memory = memory
        self.chain_of_thought = chain_of_thought
        self.debug = debug
        self.log_level = log_level.upper()
        self.log_file = log_file

        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable"
            )
        self.api_key = api_key
        self.websocket_base_url = websocket_base_url

        if base_url is None:
            base_url = os.environ.get("OPENAI_BASE_URL")
        if base_url is None:
            base_url = f"https://api.openai.com/v1"

        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key
        )

    from datetime import datetime

    def log(self, level, action, data):
        """
        记录日志。

        :param level: 日志级别（INFO, DEBUG, ERROR）。
        :param action: 日志动作（如 chat, call_tool, retrieve_memory）。
        :param data: 日志数据。
        """
        if not self.debug:
            return

        # 定义日志级别优先级
        log_levels = {"DEBUG": 1, "INFO": 2, "ERROR": 3}

        # 检查日志级别
        if log_levels.get(level, 0) < log_levels.get(self.log_level, 0):
            return

        # 获取当前时间并格式化
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构建日志信息
        log_message = f"[{current_time}] [{level}] {action}: {data}"

        # 输出到控制台
        print(log_message)

        # 输出到文件（如果指定了文件路径）
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(log_message + "\n")

    def run(self, query: str, stream=False, tools=None, max_retry=5, user_id="default_user", metadata=None):
        self.log("INFO", "run", {"query": query, "user_id": user_id, "metadata": metadata})

        if tools is None:
            tools = []
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        system_prompt = f"{self.role} /n 请一步一步思考来完成用户的要求。尽可能完成用户的回答，如果有补充信息，请参考补充信息来调用工具，直到获取所有满足用户的提问所需的答案。 /n 今日的日期: {current_date} 当前时间: {current_time}"
        params = dict(model=self.model, stream=stream)

        # 1. 从记忆中检索相关内容
        if self.memory:
            related_memories = self.memory.retrieve(query=query, user_id=user_id)
            query = self._build_context(query, related_memories)
            self.memory.store(data=query, user_id=user_id)
        else:
            query = query

        # 2. 拼接工具
        if tools:
            register_tool_manually(tools)
            self.log("DEBUG", "register_tools", {"tools": list(_FUNCTION_MAPPINGS.keys())})
            tools = get_tools()
            params["tools"] = tools

        # 3. 思维链
        if self.chain_of_thought:
            tot_response = self.run_thought(query=query)
            system_prompt = system_prompt + f" /n ##以下是问题的补充说明 /n {tot_response}"
            self.log("DEBUG", "chain_of_thought", {"response": tot_response})

        params["messages"] = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]
        response = self.client.chat.completions.create(**params)

        # agent核心运行逻辑
        for _ in range(max_retry):
            if not stream:
                if response.choices[0].message.tool_calls:
                    function_call = response.choices[0].message.tool_calls[0].function
                    self.log("DEBUG", "function_call", {"function_call": function_call.model_dump()})

                    function_args = json.loads(function_call.arguments)
                    tool_response = dispatch_tool(function_call.name, function_args)
                    self.log("INFO", "tool_response", {"tool_response": tool_response})

                    params["messages"].append(
                        {
                            "role": "assistant",
                            "content": json.dumps(function_call.model_dump()),
                        }
                    )
                    params["messages"].append(
                        {
                            "role": "user",
                            "content": tool_response,
                        }
                    )
                else:
                    reply = response.choices[0].message.content
                    self.log("INFO", "final_reply", {"reply": reply})
                    return reply

            else:
                output = ""
                function_call = []
                function_call_name = ""
                function_call_arguments = ""
                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    print(Fore.BLUE + content, end="", flush=True)
                    output += content

                    try:
                        if chunk.choices and chunk.choices[0].delta.tool_calls:
                            argumentsTxt = chunk.choices[0].delta.tool_calls[0].function.arguments
                            if argumentsTxt:
                                function_call_arguments += argumentsTxt
                    except (IndexError, AttributeError, KeyError):
                        pass

                    try:
                        if function_call_name == '' and chunk.choices[0].delta.tool_calls:
                            function_call_name = chunk.choices[0].delta.tool_calls[0].function.name
                    except (IndexError, AttributeError, KeyError):
                        pass

                    if chunk.choices[0].finish_reason == "stop":
                        self.log("INFO", "stream_response", {"output": output})
                        return output

                    elif chunk.choices[0].finish_reason == "tool_calls":
                        function_call = {
                            "name": function_call_name,
                            "arguments": function_call_arguments,
                        }
                        self.log("INFO", "tool_call", {"function_call": function_call})

                        function_args = json.loads(function_call["arguments"])
                        tool_response = dispatch_tool(function_call["name"], function_args)
                        self.log("INFO", "tool_response", {"tool_response": tool_response})

                        params["messages"].append(
                            {
                                "role": "assistant",
                                "content": output,
                            }
                        )
                        params["messages"].append(
                            {
                                "role": "function",
                                "name": function_call["name"],
                                "content": tool_response,
                            }
                        )
                        break

            response = self.client.chat.completions.create(**params)

        self.log("ERROR", "max_retry_reached", {"message": "Failed to generate a valid response."})
        return "Failed to generate a valid response."

    def _build_context(self, user_input, related_memories):
        """
        构建上下文，将用户输入和记忆内容结合。

        :param user_input: 用户输入的问题或内容。
        :param related_memories: 从记忆中检索到的相关内容。
        :return: 结合记忆后的上下文。
        """
        if not related_memories or not related_memories["memories"]:
            return user_input

        memory_context = "\n".join([m["memory"] for m in related_memories["memories"]])
        if not memory_context:
            return user_input

        prompt = f"\n用户之前提到了\n{memory_context}。\n现在用户问\n{user_input}"
        self.log("DEBUG", "related_memories", {"memory_context": memory_context})
        return prompt

    def run_thought(self, query: str, stream=False, tools=None):
        """使用思维树的方式 让大模型先根据get_tools_str生成一个解答用户query的工具使用计划"""
        tot_model = "deepseek-chat"  # self.model
        tools = get_tools_str()
        system_prompt = f"""你是一个智能助手，请根据用户输入的问题，结合工具使用计划，生成一个思维树，并按照思维树依次调用工具步骤，最终生成一个最终回答。/n 工具列表: {tools}"""
        self.log("DEBUG", "run_thought", {"system_prompt": system_prompt})

        # 第一次请求，生成初始的工具使用计划
        params = dict(model=tot_model,
                      messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query}],
                      stream=False)
        response = self.client.chat.completions.create(**params)
        initial_content = response.choices[0].message.content
        self.log("DEBUG", "initial_response", {"response": initial_content})

        # 第二次请求，请求大模型反思并生成新的工具使用规划
        reflection_prompt = "请反思你的回答，重新给出新的工具使用规划。仅输出新的工具使用规划，不要输出其他分析和回答。"
        reflection_params = dict(model=tot_model, messages=[
            {"role": "user", "content": f"{system_prompt} /n 开始思考问题: {query}"},
            {"role": "assistant", "content": initial_content},
            {"role": "user", "content": reflection_prompt}
        ], stream=False)
        self.log("DEBUG", "reflection_params", {"params": reflection_params})

        reflection_response = self.client.chat.completions.create(**reflection_params)
        refined_content = reflection_response.choices[0].message.content
        self.log("DEBUG", "refined_response", {"response": refined_content})
        return refined_content

if __name__ == "__main__":
    # Example of registering and using a tool
    print("This is LightAgent")
    # print(dispatch_tool("example_tool", {"param1": "test"}))
