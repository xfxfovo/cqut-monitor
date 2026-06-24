# CQUT Notification Monitor

重庆理工大学通知公告自动监控系统

## 功能

- 自动爬取教务处、机械工程学院、学校主页的通知公告
- 根据用户画像（专业、兴趣、班级）智能评估关联度（满分100分）
- 通过 PushPlus 推送到微信
- 使用 GitHub Actions 每小时自动运行

## 快速开始

### 1. 获取 PushPlus Token

1. 微信搜索并关注「PushPlus推送加」公众号
2. 点击「我的」→「个人中心」
3. 复制 Token

### 2. 创建 GitHub 仓库

1. 登录 GitHub
2. 点击 "+" → "New repository"
3. Repository name: `cqut-monitor`
4. 选择 "Public"
5. 点击 "Create repository"

### 3. 上传代码

```bash
cd cqut-monitor
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/cqut-monitor.git
git push -u origin main
```

### 4. 配置 Secrets

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. Name: `PUSHPLUS_TOKEN`
4. Value: 你的 PushPlus Token
5. 点击 "Add secret"

### 5. 启用 Actions

1. 点击 "Actions" 标签
2. 点击 "I understand my workflows, go ahead and enable them"

## 本地测试

```bash
pip install -r requirements.txt
export PUSHPLUS_TOKEN=your_token
python -m src.main
```

## 配置说明

编辑 `config.json` 修改用户信息和关注领域：

```json
{
  "user": {
    "name": "肖仁康",
    "major": "机械电子工程"
  },
  "interests": ["学科竞赛", "个人成长", ...]
}
```
