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
    os.path.dirname(__file__), "..", "data", "food_list.txt"
)


class FoodDataManager:
    """菜品数据管理器，提供增删查改、文件读写与随机抽取功能。"""

    def __init__(self, filepath: str = DEFAULT_FOOD_FILE):
        self.filepath = filepath
        self.foods: list[str] = []    # 内存中的菜品列表
        self._load_on_init()

    # ──────────────────────────────────────────────────────────
    # 初始化加载
    # ──────────────────────────────────────────────────────────
    def _load_on_init(self):
        """程序启动时自动加载本地菜品库（若文件存在）。"""
        # TODO: 判断 self.filepath 是否存在
        # TODO: 若存在则调用 self.load_from_file(self.filepath)
        # TODO: 若不存在则写入一组默认菜品并保存
        pass

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
        # TODO: 用 open(path, encoding='utf-8') 读取文件
        # TODO: 过滤空行与以 '#' 开头的注释行
        # TODO: 去重后赋值给 self.foods
        # TODO: 返回 self.foods
        pass

    def save_to_file(self, path: Optional[str] = None) -> bool:
        """将当前菜品列表持久化保存到 txt 文件。

        Args:
            path: 保存路径，默认使用 self.filepath。

        Returns:
            保存成功返回 True，失败返回 False。
        """
        # TODO: 创建目标目录（若不存在）
        # TODO: 写入每行一个菜品名，末尾加换行符
        # TODO: 捕获 IOError 并返回 False
        pass

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
        # TODO: 根据文件扩展名选择解析方式
        # TODO: txt  → 逐行读取，与 load_from_file 相同逻辑
        # TODO: csv  → 用 csv.reader() 读取，取第一列作为菜品名
        # TODO: 计算新增数量 = 导入前后 self.foods 长度之差
        # TODO: 调用 save_to_file() 自动持久化
        # TODO: 返回新增数量
        pass

    def export_to_csv(self, path: str) -> bool:
        """将当前菜品库导出为标准 CSV 文件（供备份或分享）。

        Args:
            path: 导出目标 csv 文件路径。

        Returns:
            导出成功返回 True，失败返回 False。
        """
        # TODO: 写入 header 行 ["food_name"]
        # TODO: 逐行写入 self.foods
        pass

    # ──────────────────────────────────────────────────────────
    # 增删查
    # ──────────────────────────────────────────────────────────
    def add_food(self, name: str) -> bool:
        """添加单条菜品（自动去重）。返回是否实际添加成功。"""
        # TODO: 校验 name 非空且不重复
        # TODO: 追加到 self.foods 并调用 save_to_file()
        pass

    def remove_food(self, name: str) -> bool:
        """删除指定菜品。返回是否删除成功。"""
        # TODO: 从 self.foods 移除，调用 save_to_file()
        pass

    def clear_all(self) -> None:
        """清空全部菜品并保存。"""
        # TODO: self.foods = [] 并调用 save_to_file()
        pass

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
        # TODO: 校验列表非空
        # TODO: 使用 random.choice(self.foods) 实现均匀随机
        pass

    def weighted_pick(self, weights: Optional[list[float]] = None) -> Optional[str]:
        """按权重随机抽取菜品（权重越高被抽中概率越大）。

        Args:
            weights: 与 self.foods 等长的权重列表，默认为均匀权重。

        Returns:
            抽中的菜品名称，若菜品库为空则返回 None。
        """
        # TODO: 校验 weights 长度与 self.foods 一致
        # TODO: 使用 random.choices(self.foods, weights=weights, k=1)[0]
        pass
