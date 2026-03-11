# 减脂追踪助手 (Fat Loss Tracker)

一个智能的减脂追踪技能，帮助你记录每日饮食、运动、体重、睡眠等信息，并对照减脂计划提供个性化建议。

## 功能特性

- **本地目录存储** - 所有配置和记录都自动保存在当前工作目录的 `fat-loss-tracker/` 文件夹下，方便管理和备份
- **固定目录结构** - 无需配置路径，所有数据都使用统一的目录结构，避免混乱
- **初始化引导** - 首次使用自动引导用户完成配置，支持设置个性化昵称（例如：长沙彭于晏）
- **日期智能识别** - 自动识别"今天"、"昨天"、"前天"或具体日期
- **信息记录** - 支持饮食、运动、体重、睡眠、步数等多维度记录
- **营养估算** - 自动预估热量和营养摄入（蛋白质、脂肪、碳水）
- **运动消耗** - 根据用户体重预估运动消耗量
- **营养计算** - 根据个人信息自动计算每日推荐热量和营养摄入
- **个性化建议** - 基于体重、运动基础、年龄、性别等提供定制化减脂建议
- **计划对照** - 每次记录后对照减脂计划生成个性化建议
- **昨日总结** - 创建今日文件时自动总结昨天的记录
- **补录支持** - 支持补录之前日期的记录

## 安装使用

### 1. 安装

**直接下载使用（推荐）**

1. 下载本项目中的 `fat-loss-tracker` 技能文件夹（包含skill.md、config.example.yaml等）
2. 将技能文件夹安装到对应工具的 skills 目录下：
   - **Claude Code**: `C:\Users\<用户名>\.claude\skills`
   - **Trae 国际版**: `C:\Users\<用户名>\.trae\skills`
   - **Trae 中文版**: `C:\Users\<用户名>\.trae-cn\skills`
   - **OpenClaw**: `C:\Users\<用户名>\.openclaw\skills`

### 2. 使用

当你在任意工作目录提到减脂相关内容时，技能会自动触发，并在**当前工作目录**下创建专门的记录文件夹：

```
你的工作目录/
└── fat-loss-tracker/           # <-- 自动创建的记录文件夹
    ├── config.yaml             # 自动生成的配置文件
    ├── 减脂计划.md              # 减脂计划文件
    ├── 体重记录.md              # 体重记录文件
    └── daily/                   # 每日记录目录
        └── YYYY-MM-DD.md
```

**注意：技能本身的文件（skill.md、evals等）和用户记录文件夹是分开的，记录文件夹只会包含你的个人数据，不会包含技能代码。**

### 2. 配置

首次使用时，技能会自动引导你完成配置（设置记录存放路径和可选的用户信息）。

首次使用时，技能会自动引导你完成配置（设置昵称和可选的用户信息），并自动创建目录结构。

也可以手动配置：在记录文件夹下编辑 `config.yaml`：

```yaml
# 用户信息（可选，用于个性化建议）
user_info:
  nickname: ""                   # 昵称（例如：长沙彭于晏）
  current_weight: null           # 当前体重(kg)
  target_weight: null            # 目标体重(kg)
  height: null                   # 身高(cm)
  age: null                      # 年龄
  gender: null                   # 性别（male/female/other）
  past_activity: "none"          # 运动基础：none(从未锻炼), slight(略有基础), good(基础不错), strong(基础很好), professional(专业运动员)
  current_activity: "moderate"   # 当前/计划运动频率：sedentary(几乎不运动), light(每周1-2次), moderate(每周3-4次), active(每周5-6次), very_active(每天)

# 减脂目标设置
weight_loss_goal:
  weekly_rate: 0.5              # 每周目标减重速度(kg)，推荐0.25-1kg/周
  calorie_deficit: null         # 热量缺口(kcal)，如果不设置将自动计算

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

### 目录结构（固定）
所有用户数据都统一存储在当前工作目录的 `fat-loss-tracker/` 文件夹下，无需手动配置路径：

```
./fat-loss-tracker/
├── config.yaml      # 配置文件
├── 减脂计划.md      # 减脂计划文件
├── 体重记录.md      # 体重记录文件
└── daily/           # 每日记录目录
    └── YYYY-MM-DD.md
```

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| user_info.nickname | 用户昵称（例如：长沙彭于晏） |
| user_info.current_weight | 当前体重(kg) |
| user_info.target_weight | 目标体重(kg) |
| user_info.height | 身高(cm) |
| user_info.age | 年龄 |
| user_info.gender | 性别（male/female/other） |
| user_info.past_activity | 运动基础：<br>none(从未锻炼), slight(略有基础), good(基础不错), strong(基础很好), professional(专业运动员) |
| user_info.current_activity | 当前/计划运动频率：<br>sedentary(几乎不运动), light(每周1-2次), moderate(每周3-4次), active(每周5-6次), very_active(每天) |
| weight_loss_goal.weekly_rate | 每周目标减重速度(kg) |
| weight_loss_goal.calorie_deficit | 热量缺口(kcal)，自动计算 |
| initialized | 是否已完成初始化（系统自动管理） |

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

**注意：安装时只需将技能文件夹放置到 Claude Code 的 skills 目录下即可。使用时技能会自动在你的当前工作目录创建 fat-loss-tracker 记录文件夹，所有个人数据都保存在此目录下，方便管理和备份。**

## 营养计算器与动态推荐

我们提供了完整的Python工具链支持个性化减脂计划：

### 1. 营养计算器
用于计算每日推荐热量和营养摄入

使用方法：
```bash
cd fat-loss-tracker
python ./scripts/nutrition_calculator.py --config config.yaml
```

### 2. 模板处理器
用于将每日记录模板中的变量替换为实际计算的个性化推荐值

使用方法：
```bash
cd fat-loss-tracker
python ./scripts/template_processor.py --config config.yaml --output daily_template.md
```

### 3. 动态推荐值
每日记录文件中的所有推荐值（每餐热量、营养素范围）均由上述脚本根据用户的个人信息自动计算，包括：
- 基础代谢率(BMR)
- 每日总能量消耗(TDEE)
- 个性化热量缺口
- 三餐和加餐的热量与营养分配
- 每日总营养素推荐范围

**示例输出：**
```
🎯 营养摄入推荐
==================================================
用户信息: 长沙彭于晏
当前体重: 70kg
目标体重: 65kg
身高: 175cm
年龄: 30
性别: male
运动基础: good
当前/计划运动频率: moderate
每周目标减重: 0.5kg
==================================================

基础代谢率(BMR): 1649千卡/天
基础活动系数: 1.55
运动基础调整系数: +0.1
最终活动系数: 1.65
每日总消耗(TDEE): 2720千卡/天
每日热量缺口: 550千卡/天
每日目标热量: 2170千卡/天

营养分配建议:
蛋白质: 140.0g (560千卡, 26.0%)
脂肪: 63.0g (567千卡, 26.0%)
碳水化合物: 260.9g (1043千卡, 48.0%)

三餐热量和营养分配:
早餐: 543-651千卡
  蛋白质: 28.0-46.2g
  碳水化合物: 35.0-63.0g
  脂肪: 14.0-21.0g

午餐: 760-868千卡
  蛋白质: 39.2-61.6g
  碳水化合物: 49.0-84.0g
  脂肪: 19.6-28.0g

晚餐: 651-760千卡
  蛋白质: 33.6-53.9g
  碳水化合物: 42.0-73.5g
  脂肪: 16.8-24.5g

加餐: 109-217千卡
  蛋白质: 5.6-15.4g
  碳水化合物: 7.0-21.0g
  脂肪: 2.8-7.0g

💡 建议
- 确保每日热量缺口不超过1000千卡
- 优先保证蛋白质摄入，防止肌肉流失
- 碳水化合物提供运动能量，避免过度限制
- 脂肪摄入要适度，保证激素正常分泌
- 结合饮食记录和运动，定期调整
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
