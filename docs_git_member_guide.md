# 📢 组员通用 Git 操作话术与终端命令
# ================================================================
# 适用对象：组员 1（gui）/ 组员 2（data）/ 组员 3（ai）
# 发送方式：直接复制粘贴给组员，或贴到群聊
# ================================================================

---

## 🔔 发给组员的通用话术（直接复制发群里）

---

> 大家好！
> 以下是我们项目 `food-wheel-ai` 的统一 Git 操作规范，**每人按自己的分支操作**，不要随意合并到别人的分支！
>
> **⚠️ 密钥保护硬性规定（违反会出大问题）：**
> 1. `.env` 文件**绝对不要** `git add`，也不要提交到 GitHub！
> 2. 每次提交前必须 `git status` 检查，确认没有 `.env` 在里面
> 3. 只能提交 `.env.example`（空模板，没有真实密钥）
>
> 下面是每人的完整操作步骤 ↓

---

## 第一步：克隆仓库（只做一次）

```bash
# 把下面的 <组长GitHub用户名> 替换为真实用户名
git clone https://github.com/<组长GitHub用户名>/food-wheel-ai.git

# 进入项目目录
cd food-wheel-ai
```

---

## 第二步：切换到自己的开发分支

> 根据你的角色，执行对应那一行命令（只执行自己的那行！）

```bash
# 组员 1（负责界面）—— 切换到 member1-gui 分支
git checkout member1-gui

# 组员 2（负责数据）—— 切换到 member2-data 分支
git checkout member2-data

# 组员 3（负责 AI）—— 切换到 member3-ai 分支
git checkout member3-ai
```

> 💡 若提示分支不存在，先从远程拉取：
> ```bash
> git fetch origin
> git checkout -b member1-gui origin/member1-gui
> ```

---

## 第三步：日常开发标准提交推送（三步命令）

> 每次写完代码都执行这三步，养成习惯！

```bash
# ① 查看改动状态（务必确认没有 .env 文件！）
git status

# ② 暂存改动（只 add 自己负责的文件，避免误 add）
#    示例：组员1 只 add gui_ui.py
git add src/gui_ui.py

# ③ 提交，填写有意义的中文描述
git commit -m "feat: 完成转盘基础绘制功能"

# ④ 推送到远程分支
#    注意：<你的分支名> 要和第二步切换的分支一致
git push origin member1-gui    # 组员 1
# git push origin member2-data # 组员 2
# git push origin member3-ai   # 组员 3
```

---

## 提交消息规范（让提交历史更整洁）

| 前缀 | 含义 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: 完成菜品 txt 读取功能` |
| `fix:` | 修复 bug | `fix: 修复转盘角度计算错误` |
| `refactor:` | 代码重构 | `refactor: 提取公共绘图函数` |
| `docs:` | 文档更新 | `docs: 更新 README 运行步骤` |
| `chore:` | 杂项（配置等） | `chore: 更新 .env.example` |

---

## ⚠️ 密钥脱敏硬性规定（请认真阅读）

```
【强制要求，必须遵守】

1. 复制 .env.example 为 .env，在 .env 里填真实密钥
   命令：cp .env.example .env（Windows 用：copy .env.example .env）

2. .env 已加入 .gitignore，理论上不会被 add
   但每次提交前请手动执行 git status 确认！

3. 绝对禁止执行：
   ❌ git add .env
   ❌ git add -A（会把 .env 一起 add 进去！）
   ✅ 只 add 具体文件名，如：git add src/gui_ui.py

4. 若已经误提交了密钥：
   → 立即到 OpenAI 控制台（platform.openai.com）撤销该密钥
   → 重新生成新密钥
   → 告知组长处理 git 历史
```

---

## 常用查看命令

```bash
git status          # 查看当前改动状态
git log --oneline   # 查看提交历史（简洁版）
git branch -a       # 查看所有本地和远程分支
git diff            # 查看未暂存的改动内容
```
