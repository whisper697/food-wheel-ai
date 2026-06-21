# =============================================================
# gui_ui.py  —  Tkinter 转盘界面模块
# 职责：绘制可视化转盘、旋转动画、所有交互按钮与弹窗
# 负责人：组员 1（member1-gui 分支）
# =============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import math
import random
import csv as _csv


# ──────────────────────────────────────────────────────────────
# 常量配置
# ──────────────────────────────────────────────────────────────
CANVAS_SIZE = 480          # 画布尺寸（正方形边长，单位 px）
WHEEL_RADIUS = 210         # 转盘半径
CENTER = CANVAS_SIZE // 2  # 圆心坐标
SPIN_STEPS = 80            # 每次旋转的总帧数（越大越平滑）
SPIN_DURATION_MS = 16      # 每帧刷新间隔（毫秒），约 60fps

# 扇区背景颜色循环（可自行扩展）
SECTOR_COLORS = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF",
    "#C77DFF", "#FF9F43", "#48DBFB", "#FF6CAE",
    "#A8E063", "#FFA07A", "#87CEEB", "#DDA0DD",
]

# 默认内置菜品（当数据管理器未提供时使用）
DEFAULT_FOODS = [
    "红烧肉", "清炒西兰花", "番茄炒蛋", "宫保鸡丁",
    "麻婆豆腐", "水煮鱼", "糖醋里脊", "蒜蓉炒菜心",
]


class FoodWheelApp:
    """美食转盘主界面类，整合转盘绘制、动画、按钮与结果展示。"""

    def __init__(self, root: tk.Tk, data_manager=None, ai=None):
        self.root = root
        self.data_manager = data_manager  # 数据模块（由 main.py 注入）
        self.ai = ai                      # AI 模块（由 main.py 注入）

        self.foods: list = []             # 当前菜品列表
        self.angle_offset: float = 0.0   # 当前旋转角度偏移（度，顺时针累计）
        self.is_spinning: bool = False    # 转盘是否正在旋转

        # 旋转完成后的回调（由 main.py 绑定）
        self.on_spin_done = None

        # 控件引用（在 _build_ui 中赋值）
        self.canvas = None
        self.listbox = None
        self.btn_spin = None
        self.ai_text = None

        # 从数据管理器加载菜品，若为空则使用默认列表
        if data_manager is not None:
            loaded = data_manager.get_foods()
            self.foods = loaded if loaded else []
        if not self.foods:
            self.foods = DEFAULT_FOODS.copy()

        self._build_ui()
        self._refresh_wheel()
        self._refresh_listbox()

    # ──────────────────────────────────────────────────────────
    # UI 构建
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        """构建完整界面布局：标题栏 + 左侧转盘区 + 右侧控制区。"""
        self.root.configure(bg="#F5F5F5")

        # ── 顶部标题栏 ──
        title_bar = tk.Frame(self.root, bg="#FF6B6B", pady=10)
        title_bar.pack(fill=tk.X)
        tk.Label(
            title_bar, text="🍜  美食转盘 AI 助手",
            font=("微软雅黑", 20, "bold"),
            bg="#FF6B6B", fg="white"
        ).pack()
        tk.Label(
            title_bar, text="转一转，决定今天吃什么！",
            font=("微软雅黑", 10),
            bg="#FF6B6B", fg="#FFE0E0"
        ).pack()

        # ── 主内容区 ──
        main_frame = tk.Frame(self.root, bg="#F5F5F5", padx=12, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧：转盘区
        left_frame = tk.Frame(main_frame, bg="#F5F5F5")
        left_frame.pack(side=tk.LEFT, padx=(0, 12))

        self.canvas = self._build_wheel_canvas(left_frame)
        self.canvas.pack()

        # 右侧：控制面板
        right_frame = tk.Frame(main_frame, bg="#F5F5F5", width=230)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        self._build_control_panel(right_frame)

    def _build_wheel_canvas(self, parent):
        """创建并返回转盘画布控件。"""
        canvas = tk.Canvas(
            parent,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg="#ECECEC",
            highlightthickness=3,
            highlightbackground="#CCCCCC",
            cursor="crosshair"
        )
        return canvas

    def _build_control_panel(self, parent):
        """构建右侧控制面板（菜品列表、按钮、AI 建议文本框）。"""
        # ── 菜品列表 ──
        tk.Label(
            parent, text="🍽  当前菜品列表",
            font=("微软雅黑", 12, "bold"),
            bg="#F5F5F5", fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 4))

        list_container = tk.Frame(parent, bg="#F5F5F5")
        list_container.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        sb = tk.Scrollbar(list_container, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_container,
            yscrollcommand=sb.set,
            font=("微软雅黑", 11),
            height=9,
            selectbackground="#FF6B6B",
            selectforeground="white",
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#DDDDDD",
            bg="white",
            fg="#444444"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.config(command=self.listbox.yview)

        # ── 功能按钮 ──
        btn_base = {
            "font": ("微软雅黑", 11, "bold"),
            "relief": tk.FLAT,
            "bd": 0,
            "padx": 8,
            "pady": 7,
            "cursor": "hand2",
        }

        self.btn_spin = tk.Button(
            parent, text="🎯  开始转动",
            bg="#FF6B6B", fg="white",
            activebackground="#E85555", activeforeground="white",
            command=self._on_spin_click,
            **btn_base
        )
        self.btn_spin.pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            parent, text="➕  手动添加",
            bg="#6BCB77", fg="white",
            activebackground="#56B464", activeforeground="white",
            command=self._on_add_food_click,
            **btn_base
        ).pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            parent, text="📂  导入菜单",
            bg="#4D96FF", fg="white",
            activebackground="#3A80E8", activeforeground="white",
            command=self._on_import_click,
            **btn_base
        ).pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            parent, text="🗑  清空菜品",
            bg="#BBBBBB", fg="white",
            activebackground="#999999", activeforeground="white",
            command=self._on_clear_click,
            **btn_base
        ).pack(fill=tk.X, pady=(0, 14))

        # ── AI 建议区 ──
        tk.Label(
            parent, text="🤖  AI 健康建议",
            font=("微软雅黑", 11, "bold"),
            bg="#F5F5F5", fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 4))

        self.ai_text = tk.Text(
            parent,
            height=9,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("微软雅黑", 10),
            bg="#FFFDF5",
            fg="#555555",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#DDDDDD",
            spacing1=3,
            spacing2=2
        )
        self.ai_text.pack(fill=tk.BOTH, expand=True)
        # 初始提示文字
        self._set_ai_text("🌟 点击「开始转动」抽取今日菜品\n转盘停下后将为您显示 AI 健康建议～")

    # ──────────────────────────────────────────────────────────
    # 转盘绘制
    # ──────────────────────────────────────────────────────────
    def _refresh_wheel(self):
        """根据 self.foods 和 self.angle_offset 重新绘制转盘。"""
        self.canvas.delete("all")
        n = len(self.foods)

        if n == 0:
            # 空转盘占位绘制
            self.canvas.create_oval(
                CENTER - WHEEL_RADIUS, CENTER - WHEEL_RADIUS,
                CENTER + WHEEL_RADIUS, CENTER + WHEEL_RADIUS,
                fill="#E8E8E8", outline="#CCCCCC", width=3
            )
            self.canvas.create_text(
                CENTER, CENTER,
                text="请添加菜品\n再开始转动 🍴",
                font=("微软雅黑", 14),
                fill="#AAAAAA",
                justify=tk.CENTER
            )
            self._draw_pointer()
            return

        sweep_deg = 360.0 / n

        # 绘制各扇区（从外到内覆盖）
        for i in range(n):
            # 扇区起始角度（tkinter 逆时针为正，90° = 12 点钟方向）
            start_deg = 90.0 - self.angle_offset - i * sweep_deg
            self._draw_sector(i, start_deg, sweep_deg, self.foods[i])

        # 绘制转盘外圈装饰环
        self.canvas.create_oval(
            CENTER - WHEEL_RADIUS - 6, CENTER - WHEEL_RADIUS - 6,
            CENTER + WHEEL_RADIUS + 6, CENTER + WHEEL_RADIUS + 6,
            outline="#DDDDDD", width=5, fill=""
        )

        # 绘制中心圆
        cr = 28
        self.canvas.create_oval(
            CENTER - cr, CENTER - cr,
            CENTER + cr, CENTER + cr,
            fill="white", outline="#DDDDDD", width=2
        )
        self.canvas.create_text(
            CENTER, CENTER,
            text="转！",
            font=("微软雅黑", 11, "bold"),
            fill="#FF6B6B"
        )

        self._draw_pointer()

    def _draw_sector(self, idx: int, start_deg: float, sweep_deg: float, label: str):
        """绘制单个扇区（含扇形背景色、菜品文字）。"""
        color = SECTOR_COLORS[idx % len(SECTOR_COLORS)]

        x0 = CENTER - WHEEL_RADIUS
        y0 = CENTER - WHEEL_RADIUS
        x1 = CENTER + WHEEL_RADIUS
        y1 = CENTER + WHEEL_RADIUS

        # 绘制扇形（clockwise：extent 为负）
        self.canvas.create_arc(
            x0, y0, x1, y1,
            start=start_deg,
            extent=-sweep_deg,
            fill=color,
            outline="white",
            width=2,
            style=tk.PIE
        )

        # 计算扇区中心角度（tkinter 角度体系）
        mid_deg = start_deg - sweep_deg / 2.0
        mid_rad = math.radians(mid_deg)

        # 文字位置（在 65% 半径处）
        r_text = WHEEL_RADIUS * 0.65
        tx = CENTER + r_text * math.cos(mid_rad)
        ty = CENTER - r_text * math.sin(mid_rad)  # 注意 canvas y 轴向下，sin 取反

        # 超长菜品名截断
        display = label if len(label) <= 5 else label[:4] + "…"

        # 文字旋转角：让文字沿径向方向排列，确保可读（-90° ~ 90°）
        text_angle = -(mid_deg - 90.0)
        # 归一化到 [-90, 90] 区间，避免文字倒置
        while text_angle > 90:
            text_angle -= 180.0
        while text_angle < -90:
            text_angle += 180.0

        self.canvas.create_text(
            tx, ty,
            text=display,
            font=("微软雅黑", 10, "bold"),
            fill="white",
            angle=text_angle
        )

    def _draw_pointer(self):
        """在转盘顶部绘制固定指针三角形（向下，指向转盘）。"""
        px = CENTER
        # 指针尖端位置（紧贴转盘外圆上方）
        py_tip = CENTER - WHEEL_RADIUS - 8
        py_base = py_tip - 22
        half_w = 13

        # 外圈阴影
        self.canvas.create_polygon(
            px, py_tip + 2,
            px - half_w - 1, py_base - 1,
            px + half_w + 1, py_base - 1,
            fill="#CC0000", outline=""
        )
        # 主体红色三角
        self.canvas.create_polygon(
            px, py_tip,
            px - half_w, py_base,
            px + half_w, py_base,
            fill="#FF3333",
            outline="#FFFFFF",
            width=1.5
        )

    # ──────────────────────────────────────────────────────────
    # Listbox 刷新
    # ──────────────────────────────────────────────────────────
    def _refresh_listbox(self):
        """重新渲染菜品列表框内容。"""
        if self.listbox is None:
            return
        self.listbox.delete(0, tk.END)
        for i, food in enumerate(self.foods):
            self.listbox.insert(tk.END, f"  {i + 1}.  {food}")

    # ──────────────────────────────────────────────────────────
    # 旋转动画
    # ──────────────────────────────────────────────────────────
    def _on_spin_click(self):
        """'开始转动' 按钮点击处理：校验菜品数量，触发旋转动画。"""
        if self.is_spinning:
            return
        if len(self.foods) < 2:
            messagebox.showwarning("提示", "请至少添加 2 道菜品再开始转动！")
            return

        self.is_spinning = True
        self.btn_spin.config(state=tk.DISABLED, text="⏳  转动中…")
        self._set_ai_text("🔄 转盘旋转中，稍候揭晓结果……")

        # 随机旋转总量：720°~1440° + 随机角度偏移，确保落点不可预测
        total_rotation = random.randint(720, 1440) + random.uniform(0.0, 360.0)
        start_angle = self.angle_offset
        end_angle = start_angle + total_rotation

        self._animate_spin(start_angle, end_angle, 0)

    def _animate_spin(self, start_angle: float, end_angle: float, step: int):
        """递归帧动画：使用 ease-out cubic 缓动公式旋转转盘至目标角度。"""
        if step >= SPIN_STEPS:
            # 动画结束，精确定位到最终角度
            self.angle_offset = end_angle
            self._refresh_wheel()
            self.is_spinning = False
            self.btn_spin.config(state=tk.NORMAL, text="🎯  开始转动")
            self._on_spin_finish()
            return

        # ease-out cubic：t 从 0 → 1，速度由快到慢
        t = step / SPIN_STEPS
        eased = 1.0 - (1.0 - t) ** 3

        self.angle_offset = start_angle + (end_angle - start_angle) * eased
        self._refresh_wheel()

        self.root.after(
            SPIN_DURATION_MS,
            lambda: self._animate_spin(start_angle, end_angle, step + 1)
        )

    def _on_spin_finish(self):
        """旋转结束：计算指针指向的菜品，显示结果弹窗，触发 AI 建议。"""
        n = len(self.foods)
        if n == 0:
            return

        sweep_deg = 360.0 / n

        # 根据旋转角度计算指针（12 点钟位置）对应的扇区
        # 转盘顺时针旋转 angle_offset 后，原始 sector i 现在位于
        # 顺时针方向 (i * sweep_deg + angle_offset) 处
        # 指针在 12 点钟（顺时针 0°），对应原始扇区：
        #   sector_idx = floor((360 - angle_offset % 360) % 360 / sweep_deg) % n
        remaining = self.angle_offset % 360.0
        sector_idx = int((360.0 - remaining) % 360.0 / sweep_deg) % n

        chosen = self.foods[sector_idx]

        # 弹出结果提示框
        messagebox.showinfo("🎉 今天吃这个！", f"今天吃：{chosen}")

        # 优先使用外部 AI 回调（main.py 绑定），其次直接调用 AI 模块
        if self.on_spin_done is not None:
            self.on_spin_done(chosen)
        elif self.ai is not None and self.ai.is_ready():
            self._set_ai_text("🤖 正在生成 AI 健康建议，请稍候…")
            suggestion = self.ai.get_suggestion(chosen)
            self.show_ai_suggestion(suggestion)
        else:
            self.show_ai_suggestion(
                f"🍽  今天抽中了【{chosen}】！\n\n"
                "💡 提示：在 .env 文件中填入 OPENAI_API_KEY\n"
                "即可开启 AI 健康建议功能，获取营养搭配方案～"
            )

    # ──────────────────────────────────────────────────────────
    # 按钮事件处理
    # ──────────────────────────────────────────────────────────
    def _on_import_click(self):
        """导入外部 txt/csv 菜单文件到菜品库。"""
        path = filedialog.askopenfilename(
            title="选择菜单文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("CSV 文件", "*.csv"),
                ("所有文件", "*.*"),
            ]
        )
        if not path:
            return

        try:
            if self.data_manager is not None:
                # 优先使用数据管理模块（组员 2 实现）
                count = self.data_manager.import_from_file(path)
                self.foods = self.data_manager.get_foods()
                messagebox.showinfo(
                    "导入成功",
                    f"✅ 成功新增 {count} 道菜品！\n当前共 {len(self.foods)} 道菜品。"
                )
            else:
                # 兜底：自行解析文件
                new_items = self._parse_food_file(path)
                existing = set(self.foods)
                added = 0
                for item in new_items:
                    if item not in existing:
                        self.foods.append(item)
                        existing.add(item)
                        added += 1
                messagebox.showinfo(
                    "导入成功",
                    f"✅ 成功新增 {added} 道菜品！\n当前共 {len(self.foods)} 道菜品。"
                )
        except Exception as e:
            messagebox.showerror("导入失败", f"读取文件时发生错误：\n{e}")
            return

        self._refresh_listbox()
        self._refresh_wheel()

    def _parse_food_file(self, path: str) -> list:
        """从 txt 或 csv 文件中解析菜品列表（兜底方法）。"""
        items = []
        if path.lower().endswith(".csv"):
            with open(path, encoding="utf-8-sig") as f:
                for row in _csv.reader(f):
                    if row:
                        name = row[0].strip()
                        if name and not name.startswith("#"):
                            items.append(name)
        else:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    name = line.strip()
                    if name and not name.startswith("#"):
                        items.append(name)
        return items

    def _on_add_food_click(self):
        """弹出输入对话框，手动添加单条菜品。"""
        name = simpledialog.askstring(
            "➕ 手动添加菜品",
            "请输入菜品名称：",
            parent=self.root
        )
        if name is None:
            return  # 用户点了取消
        name = name.strip()
        if not name:
            messagebox.showwarning("提示", "菜品名称不能为空！")
            return
        if name in self.foods:
            messagebox.showwarning("提示", f"「{name}」已在列表中，无需重复添加。")
            return

        self.foods.append(name)
        if self.data_manager is not None:
            self.data_manager.add_food(name)

        self._refresh_listbox()
        self._refresh_wheel()
        messagebox.showinfo("添加成功", f"✅ 已将「{name}」加入菜品列表！")

    def _on_clear_click(self):
        """二次确认后清空全部菜品。"""
        if not self.foods:
            messagebox.showinfo("提示", "菜品列表已经是空的！")
            return
        confirmed = messagebox.askyesno(
            "确认清空",
            f"⚠️ 将清空全部 {len(self.foods)} 道菜品，确定吗？"
        )
        if not confirmed:
            return

        self.foods.clear()
        if self.data_manager is not None:
            self.data_manager.clear_all()

        self._refresh_listbox()
        self._refresh_wheel()
        self._set_ai_text("🌟 菜品列表已清空，请重新添加菜品～")

    # ──────────────────────────────────────────────────────────
    # AI 建议文本框
    # ──────────────────────────────────────────────────────────
    def _set_ai_text(self, text: str):
        """内部方法：更新 AI 文本框内容（含写保护切换）。"""
        if self.ai_text is None:
            return
        self.ai_text.config(state=tk.NORMAL)
        self.ai_text.delete("1.0", tk.END)
        self.ai_text.insert(tk.END, text)
        self.ai_text.config(state=tk.DISABLED)

    def show_ai_suggestion(self, text: str):
        """将 AI 返回的健康建议显示到界面文本框中。（由外部 main.py 调用）"""
        self._set_ai_text(text)
