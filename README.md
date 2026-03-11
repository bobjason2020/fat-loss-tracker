# 减脂追踪助手 (Fat Loss Tracker)

一个智能的减脂追踪技能，帮助你记录每日饮食、运动、体重、睡眠等信息，并对照减脂计划提供个性化建议。

## 功能特性

- **配置化管理** - 支持自定义记录存放路径，配置与代码分离
- **初始化引导** - 首次使用自动引导用户完成配置
- **日期智能识别** - 自动识别"今天"、"昨天"、"前天"或具体日期
- **信息记录** - 支持饮食、运动、体重、睡眠、步数等多维度记录
- **营养估算** - 自动预估热量和营养摄入（蛋白质、脂肪、碳水）
- **运动消耗** - 根据用户体重预估运动消耗量
- **计划对照** - 每次记录后对照减脂计划生成个性化建议
- **昨日总结** - 创建今日文件时自动总结昨天的记录
- **补录支持** - 支持补录之前日期的记录

## 安装使用

### 1. 安装

**直接下载使用（推荐）**

1. 下载本项目整个 `fat-loss-tracker` 文件夹
2. 将文件夹内的 `fat-loss-tracker` 子文件夹复制到 Claude Code 的 skill 目录下：
   - Windows: `%APPDATA%\Claude\claude_code_settings\skills\`
   - macOS: `~/Library/Application Support/Claude/claude_code_settings/skills/`
   - Linux: `~/.config/Claude/claude_code_settings/skills/`

复制后的目录结构示例：
```
skills/
└── fat-loss-tracker/           # <-- 将此文件夹复制到 skills 目录
    ├── skill.md
    ├── config.example.yaml
    └── evals/
        └── evals.json
```

### 2. 配置

首次使用时，技能会自动引导你完成配置（设置记录存放路径和可选的用户信息）。

也可以手动配置：复制 `config.example.yaml` 为 `config.yaml`，然后编辑填写配置：

```yaml
records_root_path: "./records"   # 记录存放根路径
plan_filename: "减脂计划.md"     # 减脂计划文件名
weight_filename: "体重记录.md"   # 体重记录文件名
daily_dirname: "daily"           # 每日记录目录名
user_info:
  name: ""                       # 姓名
  target_weight: null            # 目标体重(kg)
  height: null                   # 身高(cm)
  age: null                      # 年龄
initialized: true
```

### 3. 使用

当用户提到以下内容时自动触发：
- 饮食相关：早餐、午餐、晚餐、吃了什么...
- 运动相关：跑步、健身、爬坡、力量训练...
- 体重相关：体重多少、称重...
- 睡眠相关：昨晚几点睡、今早几点起、睡眠质量...
- 减脂相关：减脂、减肥、健身计划...

## 配置说明

### 路径配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| records_root_path | 记录存放根路径 | `"./records"` 或 `"D:/MyRecords/fat-loss"` |
| plan_filename | 减脂计划文件名 | `"减脂计划.md"` |
| weight_filename | 体重记录文件名 | `"体重记录.md"` |
| daily_dirname | 每日记录目录名 | `"daily"` |

## 使用示例

### 记录睡眠
```
用户：昨晚11点睡，今早7点起
助手：好的，已记录昨晚的睡眠到今天！睡眠8小时，很符合要求👍
```

### 记录饮食
```
用户：今天早餐吃了2个水煮蛋和一杯黑咖啡
助手：好的，已记录到今天！今天的早餐很符合减脂计划👍 继续保持！午餐打算吃什么？
```

### 记录运动
```
用户：刚才去跑步了，跑了30分钟
助手：好的，已记录！跑步30分钟预估消耗约300-400千卡，很棒！身体感觉如何？
```

### 补录记录
```
用户：昨天早餐吃了包子
助手：好的，已确认是昨天！请问包子大概吃了几个？是什么馅的呢？
```

## 目录结构

```
fat-loss-tracker/                    # 项目根目录
├── fat-loss-tracker/                # Skill 主文件夹（将此文件夹放入 skills 目录）
│   ├── skill.md                     # 技能主文件
│   ├── config.example.yaml          # 配置示例
│   └── evals/
│       └── evals.json               # 评估测试用例
├── README.md                        # 项目说明
├── CHANGELOG.md                     # 更新日志
├── LICENSE                          # 开源许可证
└── .gitignore                      # Git 忽略规则
```

**注意：安装时只需将 `fat-loss-tracker` 子文件夹（包含 skill.md）放置到 Claude Code 的 skills 目录下。首次运行时会自动创建 config.yaml 文件。**

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
