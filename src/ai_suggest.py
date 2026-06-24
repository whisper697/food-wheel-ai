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
        self._cache: dict[str, str] = {}        # 建议本地缓存，避免重复调用

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
                      运行命令为 python src/main.py 时，CWD 为项目根目录，
                      默认值 ".env" 即可正确找到文件。

        Returns:
            初始化成功返回 True，失败（缺少密钥或依赖未安装）返回 False。
        """
        # 检查 python-dotenv 是否已安装
        if load_dotenv is None:
            print("[AI] 缺少依赖：python-dotenv，请运行 pip install python-dotenv")
            return False

        # 检查 openai SDK 是否已安装
        if OpenAI is None:
            print("[AI] 缺少依赖：openai，请运行 pip install openai")
            return False

        # 加载 .env 文件（override=False：不覆盖已存在的系统环境变量）
        load_dotenv(env_path, override=False)

        # 读取必填变量 OPENAI_API_KEY
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key or api_key == "your_openai_api_key_here":
            print(
                "[AI] 未找到有效的 OPENAI_API_KEY。\n"
                "     请将 .env.example 复制为 .env 并填入真实密钥，AI 功能暂不可用。"
            )
            return False

        # 读取可选变量
        base_url: Optional[str] = os.getenv("OPENAI_BASE_URL", "").strip() or None
        model: str = os.getenv("AI_MODEL", "").strip()
        if model:
            self.model = model

        # 实例化 OpenAI 客户端
        try:
            kwargs: dict = {"api_key": api_key}
            if base_url:
                kwargs["base_url"] = base_url
            self.client = OpenAI(**kwargs)
            self.api_key = api_key
            print(f"[AI] 初始化成功 ✅  模型：{self.model}")
            return True
        except Exception as e:
            print(f"[AI] 客户端初始化失败：{e}")
            self.client = None
            self.api_key = None
            return False

    # ──────────────────────────────────────────────────────────
    # AI 建议生成（拓展功能 2）
    # ──────────────────────────────────────────────────────────
    def get_suggestion(self, food_name: str) -> str:
        """调用 AI 接口，为指定菜品生成健康饮食建议。

        - 已查询过的菜品直接命中本地缓存，不重复调用 API。
        - 网络异常、超时或 API 报错时返回友好降级文字，不崩溃。

        Args:
            food_name: 抽中的菜品名称（如 "红烧肉"、"清炒西兰花"）。

        Returns:
            AI 生成的健康建议文本；若接口异常则返回降级提示文字。
        """
        # 校验客户端是否已初始化
        if not self.is_ready():
            return (
                f"🍽️  今天吃：{food_name}\n\n"
                "⚠️  AI 建议功能未启用。\n"
                "请将项目根目录下的 .env.example 复制为 .env，\n"
                "填入 OPENAI_API_KEY 后重新运行程序。"
            )

        # 命中缓存则直接返回，节省 API 调用
        if food_name in self._cache:
            return self._cache[food_name]

        # 构造消息列表
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT_TEMPLATE.format(food_name=food_name)},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                timeout=15,
            )
            result: str = response.choices[0].message.content.strip()
            # 写入缓存，相同菜品下次不再请求
            self._cache[food_name] = result
            return result

        except Exception as e:
            err_msg = str(e)[:80]
            return (
                f"🍽️  今天吃：{food_name}\n\n"
                f"⚠️  AI 建议获取失败：{err_msg}\n"
                "请检查网络连接与 API 配置。"
            )

    def get_suggestion_stream(self, food_name: str, callback) -> None:
        """流式调用 AI 接口（逐字输出），适合在界面中实现打字机效果。

        全部内容输出完毕后自动写入本地缓存。

        Args:
            food_name: 抽中的菜品名称。
            callback:  每收到一段文字就调用 callback(chunk: str)，供界面实时更新。
        """
        if not self.is_ready():
            callback("⚠️  AI 功能未初始化，请检查 .env 配置。")
            return

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT_TEMPLATE.format(food_name=food_name)},
        ]

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                stream=True,
                timeout=20,
            )
            full_text = ""
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_text += delta.content
                    callback(delta.content)   # 逐块回调，供界面实时显示

            # 流式完成后写入缓存
            if full_text:
                self._cache[food_name] = full_text

        except Exception as e:
            callback(f"\n⚠️  流式请求出错：{str(e)[:60]}")

    # ──────────────────────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────────────────────
    def is_ready(self) -> bool:
        """判断 AI 模块是否已完成初始化（密钥已加载且客户端已实例化）。"""
        return self.client is not None and self.api_key is not None

    def set_model(self, model_name: str) -> None:
        """动态切换使用的 AI 模型（如从 gpt-3.5-turbo 切换到 gpt-4o）。"""
        self.model = model_name
        print(f"[AI] 模型已切换为：{model_name}")

    def clear_cache(self) -> None:
        """清空本地建议缓存（调试用）。"""
        self._cache.clear()
        print("[AI] 建议缓存已清空")

    def cache_size(self) -> int:
        """返回当前缓存条目数。"""
        return len(self._cache)
