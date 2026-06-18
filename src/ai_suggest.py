# =============================================================
# ai_suggest.py  —  AI 健康建议模块
# 职责：读取 .env 中的 API 密钥，调用 AI 接口，生成菜品健康建议
# 负责人：组员 3（member3-ai 分支）
# =============================================================

import os
from typing import Optional

# 第三方依赖（运行前请确认已安装）：
#   pip install python-dotenv openai
try:
    from dotenv import load_dotenv   # 用于读取 .env 文件中的环境变量
except ImportError:
    load_dotenv = None               # 若未安装则降级处理

try:
    from openai import OpenAI        # OpenAI 官方 Python SDK
except ImportError:
    OpenAI = None                    # 若未安装则降级处理


# ──────────────────────────────────────────────────────────────
# 提示词模板（Prompt Templates）
# ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "你是一位专业的营养师和饮食健康顾问。"
    "根据用户提供的菜品名称，从以下三个维度给出简短的健康饮食建议（总字数不超过 150 字）：\n"
    "1. 口味特点（是否重油重盐/清淡/辛辣）；\n"
    "2. 营养价值（主要营养素及适合人群）；\n"
    "3. 健康搭配方案（建议搭配哪些食物或饮品更均衡）。"
)

USER_PROMPT_TEMPLATE = "今天抽中的菜品是：{food_name}，请给出健康饮食建议。"


class AISuggest:
    """AI 健康建议模块，封装 OpenAI 接口调用与错误处理。"""

    def __init__(self):
        self.client: Optional[object] = None   # OpenAI 客户端实例
        self.api_key: Optional[str] = None     # 从 .env 加载的密钥
        self.model: str = "gpt-3.5-turbo"      # 默认使用的模型

    # ──────────────────────────────────────────────────────────
    # 初始化 & 密钥加载
    # ──────────────────────────────────────────────────────────
    def init_api_key(self, env_path: str = ".env") -> bool:
        """读取项目根目录下的 .env 文件，初始化 OpenAI 客户端。

        .env 文件格式示例：
            OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
            OPENAI_BASE_URL=https://api.openai.com/v1   # 可选，默认使用官方地址
            AI_MODEL=gpt-3.5-turbo                      # 可选，覆盖默认模型

        Args:
            env_path: .env 文件相对路径，默认为项目根目录下的 .env。

        Returns:
            初始化成功返回 True，失败（缺少密钥或依赖未安装）返回 False。
        """
        # TODO: 检查 load_dotenv 是否已导入
        # TODO: 调用 load_dotenv(env_path) 加载环境变量
        # TODO: 从 os.environ 读取 OPENAI_API_KEY，赋值给 self.api_key
        # TODO: 读取可选变量 OPENAI_BASE_URL 和 AI_MODEL，覆盖默认值
        # TODO: 实例化 OpenAI(api_key=..., base_url=...) 赋给 self.client
        # TODO: 若任何步骤异常，打印友好错误提示并返回 False
        pass

    # ──────────────────────────────────────────────────────────
    # AI 建议生成（拓展功能 2）
    # ──────────────────────────────────────────────────────────
    def get_suggestion(self, food_name: str) -> str:
        """调用 AI 接口，为指定菜品生成健康饮食建议。

        Args:
            food_name: 抽中的菜品名称（如 "红烧肉"、"清炒西兰花"）。

        Returns:
            AI 生成的健康建议文本；若接口异常则返回降级提示文字。
        """
        # TODO: 校验 self.client 是否已初始化
        # TODO: 构造消息列表：[system_prompt, user_prompt_template.format(food_name)]
        # TODO: 调用 self.client.chat.completions.create(model, messages, max_tokens=300)
        # TODO: 提取并返回 response.choices[0].message.content
        # TODO: 捕获网络异常、超时、API 错误，返回友好降级文字
        pass

    def get_suggestion_stream(self, food_name: str, callback):
        """流式调用 AI 接口（逐字输出），适合在界面中实现打字机效果。

        Args:
            food_name: 抽中的菜品名称。
            callback:  每收到一段文字就调用 callback(chunk: str)，供界面实时更新。
        """
        # TODO: 使用 stream=True 调用 API
        # TODO: 逐块迭代 response，调用 callback(chunk.choices[0].delta.content)
        pass

    # ──────────────────────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────────────────────
    def is_ready(self) -> bool:
        """判断 AI 模块是否已完成初始化（密钥已加载且客户端已实例化）。"""
        # TODO: return self.client is not None and self.api_key is not None
        pass

    def set_model(self, model_name: str) -> None:
        """动态切换使用的 AI 模型（如从 gpt-3.5-turbo 切换到 gpt-4o）。"""
        # TODO: self.model = model_name
        pass
