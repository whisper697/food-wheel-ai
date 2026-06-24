# =============================================================
# data_file.py  —  菜品数据管理模块
# 职责：本地 txt 菜品读写、外部 txt/csv 批量导入、随机抽取算法
# 负责人：组员 2（member2-data 分支）
# =============================================================

import os
import csv
import random
from typing import Optional

# 默认菜品库文件路径（相对于项目根目录）
DEFAULT_FOOD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "food_list.txt"
)

# 默认菜品库（首次初始化时写入文件）
DEFAULT_FOODS = [
    "宫保鸡丁", "麻婆豆腐", "红烧肉", "糖醋里脊",
    "鱼香肉丝", "番茄炒蛋", "蒜蓉炒青菜", "土豆丝",
    "地三鲜", "夫妻肺片",
    "西红柿鸡蛋汤", "紫菜蛋花汤", "冬瓜排骨汤", "酸辣汤",
    "扬州炒饭", "蛋炒饭", "葱油拌面", "牛肉面",
]


class FoodDataManager:
    """菜品数据管理器，提供增删查改、文件读写与随机抽取功能。"""

    def __init__(self, filepath: str = DEFAULT_FOOD_FILE):
        self.filepath = os.path.abspath(filepath)
        self.foods: list[str] = []    # 内存中的菜品列表
        self._load_on_init()

    # ──────────────────────────────────────────────────────────
    # 初始化加载
    # ──────────────────────────────────────────────────────────
    def _load_on_init(self):
        """程序启动时自动加载本地菜品库（若文件存在）。"""
        if os.path.exists(self.filepath):
            self.load_from_file(self.filepath)
        else:
            # 文件不存在：写入默认菜品库并保存
            self.foods = DEFAULT_FOODS.copy()
            self.save_to_file()

    # ──────────────────────────────────────────────────────────
    # 本地 txt 读写
    # ──────────────────────────────────────────────────────────
    def load_from_file(self, path: str) -> list[str]:
        """从指定 txt 文件逐行读取菜品名称，返回菜品列表。

        Args:
            path: txt 文件路径，每行一个菜品名称，空行自动跳过。

        Returns:
            成功加载的菜品名称列表。
        """
        path = os.path.abspath(path)

        if not os.path.exists(path):
            # 文件不存在 → 返回空列表，不报错
            self.foods = []
            return self.foods

        seen: set[str] = set()
        loaded: list[str] = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                # 跳过空行和 '#' 注释行
                if not name or name.startswith("#"):
                    continue
                if name not in seen:
                    seen.add(name)
                    loaded.append(name)

        self.foods = loaded
        return self.foods

    def save_to_file(self, path: Optional[str] = None) -> bool:
        """将当前菜品列表持久化保存到 txt 文件。

        Args:
            path: 保存路径，默认使用 self.filepath。

        Returns:
            保存成功返回 True，失败返回 False。
        """
        target = os.path.abspath(path) if path else self.filepath

        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                for name in self.foods:
                    f.write(name + "\n")
            return True
        except (OSError, IOError):
            return False

    # ──────────────────────────────────────────────────────────
    # 外部菜单批量导入（拓展功能 1）
    # ──────────────────────────────────────────────────────────
    def import_from_file(self, path: str) -> int:
        """批量导入外部 txt 或 csv 菜单文件，自动去重后追加到库中。

        Args:
            path: 外部文件路径，支持 .txt（每行一菜）和 .csv（第一列为菜名）。

        Returns:
            新增菜品数量（去重后实际增加的条数）。
        """
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return 0

        ext = os.path.splitext(path)[1].lower()
        new_names: list[str] = []

        if ext == ".txt":
            # 逐行读取，与 load_from_file 相同逻辑（不含文件存在判断）
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    name = line.strip()
                    if not name or name.startswith("#"):
                        continue
                    new_names.append(name)

        elif ext == ".csv":
            # 用 csv.reader() 读取，取第一列作为菜品名
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if not row:
                        continue
                    name = row[0].strip()
                    if not name:
                        continue
                    # 跳过表头行（含 菜 / food / name / 菜品 等关键词）
                    if i == 0 and any(
                        kw in name.lower()
                        for kw in ("菜", "food", "name", "菜品", "dish")
                    ):
                        continue
                    new_names.append(name)
        else:
            # 不支持的文件格式
            return 0

        # 去重合并
        before_count = len(self.foods)
        existing = set(self.foods)
        for name in new_names:
            if name not in existing:
                self.foods.append(name)
                existing.add(name)

        # 自动持久化
        self.save_to_file()

        return len(self.foods) - before_count

    def export_to_csv(self, path: str) -> bool:
        """将当前菜品库导出为标准 CSV 文件（供备份或分享）。

        Args:
            path: 导出目标 csv 文件路径。

        Returns:
            导出成功返回 True，失败返回 False。
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                # utf-8-sig 带 BOM，Excel 打开中文无乱码
                writer = csv.writer(f)
                writer.writerow(["food_name"])    # header
                for name in self.foods:
                    writer.writerow([name])
            return True
        except (OSError, IOError):
            return False

    # ──────────────────────────────────────────────────────────
    # 增删查
    # ──────────────────────────────────────────────────────────
    def add_food(self, name: str) -> bool:
        """添加单条菜品（自动去重）。返回是否实际添加成功。"""
        name = name.strip()
        if not name:
            return False
        if name in self.foods:
            return False    # 不重复添加
        self.foods.append(name)
        self.save_to_file()
        return True

    def remove_food(self, name: str) -> bool:
        """删除指定菜品。返回是否删除成功。"""
        name = name.strip()
        if name in self.foods:
            self.foods.remove(name)
            self.save_to_file()
            return True
        return False

    def clear_all(self) -> None:
        """清空全部菜品并保存。"""
        self.foods.clear()
        self.save_to_file()

    def get_foods(self) -> list[str]:
        """返回当前菜品列表的浅拷贝（防止外部直接修改）。"""
        return self.foods.copy()

    # ──────────────────────────────────────────────────────────
    # 随机抽取算法
    # ──────────────────────────────────────────────────────────
    def random_pick(self) -> Optional[str]:
        """从菜品库中随机均匀抽取一道菜品。

        Returns:
            抽中的菜品名称，若菜品库为空则返回 None。
        """
        if not self.foods:
            return None
        return random.choice(self.foods)

    def weighted_pick(self, weights: Optional[list[float]] = None) -> Optional[str]:
        """按权重随机抽取菜品（权重越高被抽中概率越大）。

        Args:
            weights: 与 self.foods 等长的权重列表，默认为均匀权重。

        Returns:
            抽中的菜品名称，若菜品库为空则返回 None。
        """
        if not self.foods:
            return None

        if weights is None:
            return random.choice(self.foods)

        if len(weights) != len(self.foods):
            raise ValueError(
                f"[weighted_pick] weights 长度 ({len(weights)}) "
                f"与菜品数量 ({len(self.foods)}) 不匹配。"
            )

        if any(w < 0 for w in weights):
            raise ValueError("[weighted_pick] 权重不能为负数。")

        total = sum(weights)
        if total == 0:
            raise ValueError("[weighted_pick] 权重之和不能为 0。")

        result = random.choices(self.foods, weights=weights, k=1)
        return result[0]
