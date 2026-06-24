# =============================================================
# main.py  —  程序总入口
# 职责：初始化应用、整合界面模块、数据模块、AI模块并启动主循环
# 负责人：组长（leader-main 分支）
# =============================================================

import tkinter as tk
from tkinter import messagebox
import sys
import os

# ── 将 src 目录加入搜索路径，确保模块能互相导入 ──────────────
sys.path.insert(0, os.path.dirname(__file__))


# ── 安全导入各模块（给出友好报错提示）────────────────────────
def _import_modules():
    """尝试导入三个子模块，任何一个失败都给出明确提示。"""
    errors = []

    try:
        from gui_ui import FoodWheelApp
    except ImportError as e:
        FoodWheelApp = None
        errors.append(f"[界面模块] gui_ui.py 导入失败：{e}")

    try:
        from data_file import FoodDataManager
    except ImportError as e:
        FoodDataManager = None
        errors.append(f"[数据模块] data_file.py 导入失败：{e}")

    try:
        from ai_suggest import AISuggest
    except ImportError as e:
        AISuggest = None
        errors.append(f"[AI模块] ai_suggest.py 导入失败：{e}")

    return FoodWheelApp, FoodDataManager, AISuggest, errors


# ── 主程序入口 ────────────────────────────────────────────────
def main():
    """程序主入口，负责初始化各模块并启动 Tkinter 主循环。"""

    # ── 1. 导入模块 ─────────────────────────────────────────────
    FoodWheelApp, FoodDataManager, AISuggest, errors = _import_modules()

    if errors:
        print("=" * 60)
        print("⚠️  以下模块尚未完成，程序将在受限模式下运行：")
        for err in errors:
            print(f"   {err}")
        print("=" * 60)

    # ── 2. 初始化数据管理器 ─────────────────────────────────────
    if FoodDataManager:
        try:
            data_manager = FoodDataManager()
            print(f"✅ 数据模块加载成功，共 {len(data_manager.get_foods())} 道菜品")
        except Exception as e:
            print(f"⚠️  数据模块初始化失败：{e}")
            data_manager = None
    else:
        data_manager = None

    # ── 3. 初始化 AI 建议模块 ───────────────────────────────────
    if AISuggest:
        try:
            ai = AISuggest()
            # 自动查找 .env 文件（main.py 上一级即项目根目录）
            env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
            ai_ready = ai.init_api_key(env_path=env_path)
            if ai_ready:
                print("✅ AI模块加载成功，密钥已就绪")
            else:
                print("⚠️  AI模块：.env 密钥未配置，AI建议功能将不可用")
        except Exception as e:
            print(f"⚠️  AI模块初始化失败：{e}")
            ai = None
    else:
        ai = None

    # ── 4. 创建 Tkinter 根窗口 ─────────────────────────────────
    root = tk.Tk()
    root.title("🍜 美食转盘 AI 助手")
    root.resizable(False, False)

    # 窗口居中显示
    window_width, window_height = 900, 560
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ── 5. 若界面模块未完成，显示占位提示窗口 ─────────────────
    if not FoodWheelApp:
        _show_placeholder(root)
        root.mainloop()
        return

    # ── 6. 实例化主界面，传入数据与 AI 模块 ────────────────────
    try:
        app = FoodWheelApp(root, data_manager=data_manager, ai=ai)
    except Exception as e:
        messagebox.showerror("界面初始化失败", f"gui_ui.py 出错：\n{e}")
        root.destroy()
        return

    # ── 7. 绑定转盘旋转完成回调 → 触发 AI 建议 ────────────────
    def on_spin_done(food_name: str):
        """旋转结束后自动调用：获取 AI 建议并推送到界面。"""
        if ai and ai.is_ready():
            try:
                print(f"正在获取「{food_name}」的 AI 健康建议...")
                suggestion = ai.get_suggestion(food_name)
                # 将建议推送到界面文本框
                if hasattr(app, "show_ai_suggestion"):
                    app.show_ai_suggestion(suggestion)
                else:
                    print(f"AI建议：{suggestion}")
            except Exception as e:
                print(f"⚠️  AI建议获取失败：{e}")
                if hasattr(app, "show_ai_suggestion"):
                    app.show_ai_suggestion("AI建议暂时不可用，请检查网络或密钥配置。")
        else:
            # AI 未配置时，显示默认提示
            if hasattr(app, "show_ai_suggestion"):
                app.show_ai_suggestion(
                    f"您抽中了【{food_name}】\n"
                    "（AI建议功能未启用，请在 .env 文件中配置 API Key）"
                )

    app.on_spin_done = on_spin_done

    # ── 8. 启动主循环 ───────────────────────────────────────────
    print("🎉 美食转盘 AI 助手已启动！")
    root.mainloop()


def _show_placeholder(root: tk.Tk):
    """界面模块未完成时，显示一个占位提示窗口。"""
    root.geometry("500x300")
    frame = tk.Frame(root, bg="#FFF8F0", padx=40, pady=40)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="🍜 美食转盘 AI 助手",
        font=("微软雅黑", 18, "bold"),
        bg="#FFF8F0",
        fg="#FF6B35"
    ).pack(pady=(0, 10))

    tk.Label(
        frame,
        text="界面模块（gui_ui.py）尚未完成\n\n请等待组员 1 完成开发后再运行。",
        font=("微软雅黑", 12),
        bg="#FFF8F0",
        fg="#666666",
        justify="center"
    ).pack(pady=10)

    tk.Label(
        frame,
        text="✅ 数据模块  ✅ AI模块  ⏳ 界面模块",
        font=("微软雅黑", 10),
        bg="#FFF8F0",
        fg="#999999"
    ).pack(pady=5)


if __name__ == "__main__":
    main()
