# 👥 分人开发任务说明
# ================================================================
# 每位组员对照自己的角色认领任务，互不干扰
# 组长请将对应部分转发给每位组员
# ================================================================

---

## 组员 1 ｜ GUI 界面开发

**开发分支**：`member1-gui`  
**负责文件**：`src/gui_ui.py`  
**切换分支命令**：`git checkout member1-gui`

### 开发任务清单

#### ✅ 必须完成（基础功能）

1. **界面布局搭建**
   - 使用 `tk.Frame` 将窗口分为左侧转盘区 + 右侧控制区
   - 左侧：Canvas 画布（480×480px），用于绘制转盘
   - 右侧：菜品 Listbox、功能按钮区、AI 建议文本框

2. **转盘绘制**
   - 根据 `self.foods` 列表数量，均分圆心角（360° / 菜品数量）
   - 使用 `canvas.create_arc()` 绘制彩色扇形，颜色循环使用 `SECTOR_COLORS`
   - 使用 `canvas.create_text()` 在每个扇区中央绘制菜品名称（自动计算坐标）
   - 在转盘顶部绘制固定指针（向下三角形）

3. **旋转动画**
   - 点击"开始转动"后，随机生成目标旋转角度（720°~1440° + 随机偏移）
   - 使用 ease-out 缓动公式实现减速停止效果
   - 动画期间禁用旋转按钮，动画结束后恢复

4. **结果弹窗**
   - 旋转结束后，根据最终角度计算指针指向哪个扇区
   - 使用 `messagebox.showinfo()` 弹出"🎉 今天吃：XXX"的结果窗口

5. **手动添加菜品**
   - 点击"➕ 手动添加"弹出输入框（`simpledialog.askstring()`）
   - 非空校验 + 去重后添加，刷新 Listbox 和转盘

#### 🌟 拓展任务（加分项）

6. **外部菜单导入**（与组员 2 协作）
   - 点击"📂 导入菜单"调用 `filedialog.askopenfilename()`
   - 支持 .txt 和 .csv 格式，调用 `data_manager.import_from_file(path)`

7. **AI 建议展示**
   - 旋转结束后，将抽中菜品名传给 `self.on_spin_done(food_name)`
   - 在右侧文本框中展示 AI 返回的健康建议

---

## 组员 2 ｜ 数据管理开发

**开发分支**：`member2-data`  
**负责文件**：`src/data_file.py`、`data/food_list.txt`  
**切换分支命令**：`git checkout member2-data`

### 开发任务清单

#### ✅ 必须完成（基础功能）

1. **本地 txt 菜品读写**
   - 实现 `load_from_file(path)`：逐行读取 txt，过滤空行和注释行，去重后存入 `self.foods`
   - 实现 `save_to_file()`：将 `self.foods` 持久化保存到 txt 文件
   - 程序启动时自动加载 `data/food_list.txt`

2. **增删查改接口**
   - `add_food(name)`：添加单条菜品（非空 + 去重校验）
   - `remove_food(name)`：删除指定菜品
   - `clear_all()`：清空全部菜品
   - `get_foods()`：返回菜品列表浅拷贝

3. **随机抽取算法**
   - `random_pick()`：均匀随机抽取一道菜品（使用 `random.choice()`）
   - 边界处理：菜品库为空时返回 `None` 并提示

#### 🌟 拓展任务（加分项）

4. **外部菜单批量导入**（拓展功能 1）
   - 实现 `import_from_file(path)`：支持 .txt（每行一菜）和 .csv（第一列为菜名）
   - 自动去重，返回新增菜品数量
   - 导入后自动调用 `save_to_file()` 持久化

5. **导出功能**
   - 实现 `export_to_csv(path)`：将当前菜品库导出为标准 CSV 文件

6. **加权随机抽取**
   - 实现 `weighted_pick(weights)`：按权重随机抽取（如近期未吃的菜品权重更高）

---

## 组员 3 ｜ AI 建议开发

**开发分支**：`member3-ai`  
**负责文件**：`src/ai_suggest.py`、`.env.example`  
**切换分支命令**：`git checkout member3-ai`

### 开发任务清单

#### ✅ 必须完成（基础功能）

1. **密钥加载**
   - 实现 `init_api_key(env_path)`：使用 `python-dotenv` 读取 `.env` 文件
   - 从环境变量获取 `OPENAI_API_KEY`，实例化 OpenAI 客户端
   - 支持可选环境变量 `OPENAI_BASE_URL` 和 `AI_MODEL`

2. **AI 建议生成**（拓展功能 2）
   - 实现 `get_suggestion(food_name)`：调用 OpenAI Chat Completion API
   - 构造 system prompt（营养师角色）和 user prompt（菜品名称）
   - 返回健康建议文本（口味特点、营养价值、搭配方案三个维度）

3. **错误处理**
   - 捕获网络异常、超时、API 错误，返回友好降级文字
   - `is_ready()` 方法：判断 AI 模块是否已正确初始化

#### 🌟 拓展任务（加分项）

4. **流式输出**
   - 实现 `get_suggestion_stream(food_name, callback)`：逐字输出，实现打字机效果

5. **多模型支持**
   - 实现 `set_model(model_name)`：动态切换 AI 模型（如 gpt-3.5-turbo → gpt-4o）

6. **建议缓存**
   - 对相同菜品名称的建议结果进行本地缓存，避免重复调用 API

---

## 模块协作接口说明

为了确保三个模块能正确整合，以下是模块间的协作接口：

### main.py 调用方式（组长负责整合）

```python
# 初始化各模块
data_manager = FoodDataManager()
ai = AISuggest()
ai.init_api_key()  # 加载 .env 中的密钥

# 创建界面，传入数据和 AI 模块
app = FoodWheelApp(root, data_manager=data_manager, ai=ai)

# 绑定旋转完成回调
def on_spin_done(food_name):
    suggestion = ai.get_suggestion(food_name)
    app.show_ai_suggestion(suggestion)

app.on_spin_done = on_spin_done
```

### gui_ui.py 调用 data_file.py

```python
# 在 gui_ui.py 中通过 self.data_manager 调用：
self.data_manager.load_from_file("data/food_list.txt")
self.data_manager.add_food("新菜品")
foods = self.data_manager.get_foods()
```

### gui_ui.py 调用 ai_suggest.py

```python
# 在 gui_ui.py 中通过 self.ai 调用：
if self.ai.is_ready():
    suggestion = self.ai.get_suggestion(food_name)
    self.show_ai_suggestion(suggestion)
```
