# 🔧 组长合并分支操作指令
# ================================================================
# 适用对象：组长（leader-main 分支负责人）
# 场景：各组员开发完成后，将其分支合并到主分支
# ================================================================

---

## 前置准备：确保本地分支是最新的

```bash
# 进入项目目录
cd "c:/Users/Administrator/WorkBuddy/20260618200135/food-wheel-ai"

# 切换到 leader-main 分支
git checkout leader-main

# 从远程拉取最新代码
git pull origin leader-main
```

---

## 方式一：通过 GitHub Pull Request 合并（✅ 推荐）

> 这是最安全的方式，可以在合并前进行代码审查（Code Review）。

### 步骤 1：组员提交 PR

告诉组员，开发完成后执行：

```bash
# 组员在自己分支上提交并推送
git add src/gui_ui.py    # 替换为自己的文件
git commit -m "feat: 完成转盘界面开发"
git push origin member1-gui
```

然后让组员去 GitHub 仓库页面，点击 **"Compare & pull request"** 按钮。

### 步骤 2：组长审查并合并 PR

1. 打开 GitHub 仓库的 **Pull requests** 标签页
2. 点击对应 PR（如 `member1-gui → leader-main`）
3. 点击 **"Files changed"** 查看代码改动
4. 确认无误后，点击 **"Merge pull request"**
5. 选择合并方式：
   - **Merge commit**（推荐）：保留完整提交历史
   - **Squash and merge**：将多次提交合并为一个
   - **Rebase and merge**：线性历史，无合并节点

### 步骤 3：删除已合并的远程分支（可选）

```bash
# 合并后删除远程分支（保持仓库整洁）
git push origin --delete member1-gui

# 删除本地分支
git branch -d member1-gui
```

---

## 方式二：本地命令行合并（⚠️ 需谨慎）

> 适用于快速合并或解决复杂冲突的场景。

### 基本合并流程

```bash
# 1. 确保在目标分支（leader-main）
git checkout leader-main

# 2. 拉取最新代码
git pull origin leader-main

# 3. 合并组员分支
git merge member1-gui

# 4. 若无冲突，直接推送到远程
git push origin leader-main
```

---

## 冲突解决全流程

> 当多个组员修改了同一文件的同一区域时，会产生冲突。

### 步骤 1：识别冲突

```bash
# 尝试合并，若有冲突会提示
git merge member1-gui

# 输出示例：
# CONFLICT (content): Merge conflict in src/main.py
# Automatic merge failed; fix conflicts and then commit the result.
```

### 步骤 2：查看冲突文件

```bash
# 查看哪些文件有冲突
git status

# 输出示例：
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#         both modified:   src/main.py
```

### 步骤 3：手动解决冲突

打开冲突文件（如 `src/main.py`），会看到类似这样的标记：

```python
<<<<<<< HEAD
# 这是 leader-main 分支的代码
data_manager = FoodDataManager()
=======
# 这是 member1-gui 分支的代码
self.data_manager = FoodDataManager()
>>>>>>> member1-gui
```

**解决方法**：
1. 决定保留哪一段代码，或手动合并两段代码
2. 删除 `<<<<<<<`、`=======`、`>>>>>>>` 这三行标记
3. 保存文件

### 步骤 4：标记冲突已解决并完成合并

```bash
# 标记冲突已解决
git add src/main.py

# 完成合并提交
git commit -m "merge: 解决 member1-gui 合并冲突"

# 推送到远程
git push origin leader-main
```

---

## 常见合并场景与命令速查

| 场景 | 命令 | 说明 |
|------|------|------|
| 合并某分支到当前分支 | `git merge <分支名>` | 基本合并操作 |
| 中止正在进行的合并 | `git merge --abort` | 冲突无法解决时回退 |
| 查看所有分支合并情况 | `git branch --merged` | 查看已合并到当前分支的分支 |
| 查看未合并的分支 | `git branch --no-merged` | 查看还未合并的分支 |
| 强制删除未合并分支 | `git branch -D <分支名>` | 谨慎使用！会丢失改动 |
| 查看合并历史 | `git log --graph --oneline` | 图形化展示分支合并历史 |

---

## 合并后验证

```bash
# 1. 确保程序能正常运行
python src/main.py

# 2. 确认所有模块正确整合
git log --oneline --graph   # 查看合并历史是否整洁

# 3. 打标签标记重要版本（可选）
git tag -a v1.0 -m "完成基础功能，第一次整合"
git push origin v1.0
```

---

## ⚠️ 合并注意事项

1. **合并前先沟通**：确保组员已完成开发，并且代码能正常运行
2. **一次合并一个分支**：不要同时合并多个分支，容易产生复杂冲突
3. **合并后立即测试**：合并后运行程序，确保各模块整合正常
4. **保留分支记录**：合并后不要立即删除分支，便于回溯问题
5. **.env 文件检查**：合并后执行 `git status`，确认 `.env` 没有被意外加入版本控制
