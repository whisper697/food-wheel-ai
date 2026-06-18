# 美食转盘 AI 助手 🍜

> 一个基于 Python + Tkinter + OpenAI 的可视化美食随机转盘，抽到菜品后自动给出 AI 营养健康建议。

---

## 项目介绍

本项目为课程期末作业，由 4 人小组共同开发。  
核心功能：
- **基础功能**：Tkinter 可视化转盘，随机抽取菜品/门店
- **拓展功能 1**：支持外部 txt/csv 菜单文件批量导入菜品库
- **拓展功能 2**：接入 AI 接口，抽中菜品后自动输出健康建议（重油重盐 / 清淡 / 搭配方案）

---

## 目录结构

```
food-wheel-ai/
├─ src/
│  ├─ main.py          # 程序总入口（组长负责）
│  ├─ gui_ui.py        # Tkinter 转盘界面（组员 1）
│  ├─ data_file.py     # 菜品数据管理（组员 2）
│  └─ ai_suggest.py    # AI 健康建议（组员 3）
├─ data/
│  └─ food_list.txt    # 本地菜品库（每行一个菜品名称）
├─ screenshots/        # 功能演示截图
├─ report/             # 期末实验报告
├─ .env                # 本地密钥文件（禁止上传 GitHub！）
├─ .env.example        # 密钥脱敏模板（可上传）
└─ README.md
```

---

## 运行步骤

### 1. 克隆项目

```bash
git clone https://github.com/<你的GitHub用户名>/food-wheel-ai.git
cd food-wheel-ai
```

### 2. 安装依赖

```bash
pip install python-dotenv openai
```

> Tkinter 为 Python 标准库，通常无需额外安装。  
> 若提示缺失（Linux），可执行：`sudo apt-get install python3-tk`

### 3. 配置 AI 密钥

```bash
# 复制脱敏模板为本地配置
cp .env.example .env
```

打开 `.env` 文件，填入真实密钥：

```
OPENAI_API_KEY=sk-你的真实密钥
```

### 4. 启动程序

```bash
python src/main.py
```

---

## 四人分工说明

| 角色 | 姓名 | 开发分支 | 负责文件 | 主要任务 |
|------|------|----------|----------|----------|
| 组长 | （姓名） | `leader-main` | `main.py` | 项目整合、模块联调、合并分支、最终部署 |
| 组员 1 | （姓名） | `member1-gui` | `gui_ui.py` | Tkinter 转盘界面、旋转动画、所有交互按钮 |
| 组员 2 | （姓名） | `member2-data` | `data_file.py` | 菜品读写、外部文件导入、随机抽取算法 |
| 组员 3 | （姓名） | `member3-ai` | `ai_suggest.py` | .env 密钥读取、OpenAI 接口调用、健康建议生成 |

---

## 开发分支说明

本项目采用 **Fork + 独立分支** 协作模式，共设 4 条开发分支：

| 分支名 | 用途 |
|--------|------|
| `leader-main` | 组长主分支，用于模块整合与最终发布 |
| `member1-gui` | 组员 1 独立开发 Tkinter 界面模块 |
| `member2-data` | 组员 2 独立开发数据管理模块 |
| `member3-ai` | 组员 3 独立开发 AI 建议模块 |

**合并流程**：各组员完成开发后，在 GitHub 上向 `leader-main` 分支提交 Pull Request，由组长审核合并。

---

## 密钥脱敏规范（⚠️ 硬性要求）

> 违反此规范可能导致 AI 密钥泄露，造成账号被盗和不必要的费用损失。

1. **`.env` 文件绝对禁止提交到 GitHub**，该文件已加入 `.gitignore`
2. 仅提交 `.env.example` 脱敏模板（内容为空占位符，不含真实密钥）
3. 提交前必须执行 `git status` 确认 `.env` 不在暂存区
4. 若已误提交密钥，立即到 AI 服务商控制台撤销该密钥并重新生成

---

## 技术栈

- Python 3.10+
- Tkinter（GUI 界面）
- python-dotenv（环境变量管理）
- OpenAI Python SDK（AI 接口调用）
