# =============================================================
# main.py  —  程序总入口
# 职责：初始化应用、整合界面模块、数据模块、AI模块并启动主循环
# 负责人：组长（leader-main 分支）
# =============================================================

import tkinter as tk
from gui_ui import FoodWheelApp      # 界面模块（member1 负责）
from data_file import FoodDataManager  # 数据模块（member2 负责）
from ai_suggest import AISuggest       # AI 建议模块（member3 负责）


def main():
    """程序主入口，负责初始化各模块并启动 Tkinter 主循环。"""

    # ── 1. 初始化数据管理器 ─────────────────────────────────────
    data_manager = FoodDataManager()
    # TODO: 加载本地菜品库（data/food_list.txt）
    # data_manager.load_from_file("data/food_list.txt")

    # ── 2. 初始化 AI 建议模块 ───────────────────────────────────
    ai = AISuggest()
    # TODO: 读取 .env 中的 API 密钥并完成鉴权初始化
    # ai.init_api_key()

    # ── 3. 创建 Tkinter 根窗口 ─────────────────────────────────
    root = tk.Tk()
    root.title("美食转盘 AI 助手 🍜")
    root.resizable(False, False)

    # ── 4. 实例化主界面，传入数据与 AI 模块 ────────────────────
    app = FoodWheelApp(root, data_manager=data_manager, ai=ai)
    # TODO: 绑定转盘旋转完成事件 → 触发 AI 建议回调
    # app.on_spin_done = lambda food: print(ai.get_suggestion(food))

    # ── 5. 启动主循环 ───────────────────────────────────────────
    root.mainloop()


if __name__ == "__main__":
    main()
