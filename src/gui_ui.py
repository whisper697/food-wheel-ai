# =============================================================
# gui_ui.py  —  Tkinter 转盘界面模块
# 职责：绘制可视化转盘、旋转动画、所有交互按钮与弹窗
# 负责人：组员 1（member1-gui 分支）
# =============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import random


# ──────────────────────────────────────────────────────────────
# 常量配置
# ──────────────────────────────────────────────────────────────
CANVAS_SIZE = 480          # 画布尺寸（正方形边长，单位 px）
WHEEL_RADIUS = 210         # 转盘半径
CENTER = CANVAS_SIZE // 2  # 圆心坐标
SPIN_STEPS = 60            # 每次旋转的总帧数
SPIN_DURATION_MS = 20      # 每帧刷新间隔（毫秒）

# 扇区背景颜色循环（可自行扩展）
SECTOR_COLORS = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF",
    "#C77DFF", "#FF9F43", "#48DBFB", "#FF6CAE",
]


class FoodWheelApp:
    """美食转盘主界面类，整合转盘绘制、动画、按钮与结果展示。"""

    def __init__(self, root: tk.Tk, data_manager=None, ai=None):
        self.root = root
        self.data_manager = data_manager  # 数据模块（由 main.py 注入）
        self.ai = ai                      # AI 模块（由 main.py 注入）

        self.foods: list[str] = []        # 当前菜品列表
        self.angle_offset: float = 0.0   # 当前旋转角度偏移（度）
        self.is_spinning: bool = False    # 转盘是否正在旋转

        # 旋转完成后的回调（由 main.py 绑定）
        self.on_spin_done = None

        self._build_ui()
        self._refresh_wheel()

    # ──────────────────────────────────────────────────────────
    # UI 构建
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        """构建完整界面布局：左侧转盘区 + 右侧控制区。"""
        # TODO: 实现界面布局
        # 建议布局：
        #   左列 → Canvas（转盘）+ 指针三角形
        #   右列 → 菜品列表显示框 / 导入按钮 / 旋转按钮 / AI建议展示框
        pass

    def _build_wheel_canvas(self, parent):
        """创建并返回转盘画布控件。"""
        # TODO: 使用 tk.Canvas 绘制圆形转盘区域
        # canvas = tk.Canvas(parent, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#F8F8F8")
        # return canvas
        pass

    def _build_control_panel(self, parent):
        """构建右侧控制面板（按钮、列表、AI建议文本框）。"""
        # TODO: 添加以下控件：
        #   - Listbox：显示当前菜品列表
        #   - Button "🎯 开始转动"  → self._on_spin_click()
        #   - Button "📂 导入菜单"  → self._on_import_click()
        #   - Button "➕ 手动添加"  → self._on_add_food_click()
        #   - Button "🗑 清空菜品"  → self._on_clear_click()
        #   - Text：AI 健康建议展示区（只读）
        pass

    # ──────────────────────────────────────────────────────────
    # 转盘绘制
    # ──────────────────────────────────────────────────────────
    def _refresh_wheel(self):
        """根据 self.foods 和 self.angle_offset 重新绘制转盘。"""
        # TODO: 清空 Canvas，按扇区数量等分圆心角，循环调用 _draw_sector()
        pass

    def _draw_sector(self, idx: int, start_deg: float, sweep_deg: float, label: str):
        """绘制单个扇区（含扇形背景色、菜品文字）。"""
        # TODO: 使用 canvas.create_arc() 绘制扇形
        # TODO: 使用 canvas.create_text() 在扇区中心绘制文字（需旋转坐标）
        pass

    def _draw_pointer(self):
        """在转盘顶部绘制固定指针三角形。"""
        # TODO: 使用 canvas.create_polygon() 在 CENTER_X, 0 附近绘制向下三角
        pass

    # ──────────────────────────────────────────────────────────
    # 旋转动画
    # ──────────────────────────────────────────────────────────
    def _on_spin_click(self):
        """'开始转动' 按钮点击处理：校验菜品数量，触发旋转动画。"""
        if self.is_spinning:
            return
        if len(self.foods) < 2:
            messagebox.showwarning("提示", "请至少添加 2 道菜品！")
            return
        # TODO: 计算随机目标角度（建议 720°~1440° + 随机偏移）
        # TODO: 调用 self._animate_spin(target_angle, step=0)
        pass

    def _animate_spin(self, target_angle: float, current_angle: float, step: int):
        """递归帧动画：缓动旋转转盘至目标角度。"""
        # TODO: 使用 ease-out 缓动公式逐帧更新 self.angle_offset
        # TODO: 每帧调用 self._refresh_wheel()
        # TODO: 动画结束后调用 self._on_spin_finish()
        pass

    def _on_spin_finish(self):
        """旋转结束：计算指针指向的菜品，显示结果弹窗，触发 AI 建议。"""
        # TODO: 根据最终 angle_offset 计算指针所在扇区索引
        # TODO: 使用 messagebox.showinfo() 弹窗展示抽中的菜品名称
        # TODO: 调用 self.on_spin_done(food_name) 触发外部 AI 回调
        pass

    # ──────────────────────────────────────────────────────────
    # 按钮事件处理
    # ──────────────────────────────────────────────────────────
    def _on_import_click(self):
        """导入外部 txt/csv 菜单文件到菜品库。"""
        # TODO: 调用 filedialog.askopenfilename() 选择文件
        # TODO: 调用 self.data_manager.import_from_file(path) 读取菜品
        # TODO: 刷新 Listbox 和转盘
        pass

    def _on_add_food_click(self):
        """弹出输入对话框，手动添加单条菜品。"""
        # TODO: 使用 tk.simpledialog.askstring() 获取用户输入
        # TODO: 校验非空后追加到 self.foods 并更新 data_manager
        pass

    def _on_clear_click(self):
        """清空当前全部菜品。"""
        # TODO: 二次确认弹窗 → 清空 self.foods → 刷新转盘
        pass

    def show_ai_suggestion(self, text: str):
        """将 AI 返回的健康建议显示到界面文本框中。（由外部调用）"""
        # TODO: 更新右侧 AI 建议 Text 控件内容
        pass
