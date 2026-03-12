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
- **精准营养计算** - 基于Katch-McArdle公式计算BMR，分项计算TDEE（BMR+EAT+NEAT）
- **训练日调整** - 根据训练类型（力量/有氧/休息）自动调整碳水摄入
- **个性化建议** - 基于体重、体脂率、训练计划等提供定制化减脂建议
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

### 3. 配置

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
  body_fat_rate: null            # 体脂率(%)，用于Katch-McArdle公式计算BMR
  past_activity: "none"          # 运动基础
  current_activity: "moderate"   # 当前/计划运动频率

# 训练计划（用于计算运动消耗EAT）
training_plan:
  low_intensity_days: 0          # 每周低强度训练天数（散步、瑜伽、拉伸等）
  medium_intensity_days: 0       # 每周中强度训练天数（慢跑、游泳、骑行等）
  high_intensity_days: 0         # 每周高强度训练天数（HIIT、力量训练、冲刺跑等）

# 每日追踪
daily_tracking:
  daily_steps: 10000             # 每日步数目标
  today_type: "rest"             # 今日类型：strength(力量训练日)/cardio(有氧日)/rest(休息日)

# 减脂目标设置
weight_loss_goal:
  weekly_rate: 0.5              # 每周目标减重速度(kg)，推荐0.25-1kg/周
  calorie_deficit: null         # 热量缺口(kcal)，如果不设置将自动计算

initialized: true
```

### 4. 触发关键词

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
| user_info.body_fat_rate | 体脂率(%)，用于精准计算BMR |
| user_info.past_activity | 运动基础 |
| user_info.current_activity | 当前/计划运动频率 |
| training_plan.low_intensity_days | 每周低强度训练天数 |
| training_plan.medium_intensity_days | 每周中强度训练天数 |
| training_plan.high_intensity_days | 每周高强度训练天数 |
| daily_tracking.daily_steps | 每日步数目标 |
| daily_tracking.today_type | 今日类型（strength/cardio/rest） |
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
用户：今天去健身房撸铁了，练了1小时
助手：好的，已记录！今天是力量训练日，碳水会自动增加30%支持训练💪 身体感觉如何？
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

## 营养计算与动态推荐

### 基础代谢率(BMR)计算（Katch-McArdle公式）

**计算步骤：**
1. 计算去脂体重(FFM)：
   `FFM(kg) = 体重(kg) × (1 - 体脂率%)`
   
2. 计算基础代谢率：
   `BMR(大卡) = 370 + (21.6 × FFM)`

**示例：** 70kg男性，体脂率20%
- FFM = 70 × (1 - 0.2) = 56kg
- BMR = 370 + (21.6 × 56) ≈ 1580大卡

**体脂率未提供时：**
- 男性默认体脂率：18%
- 女性默认体脂率：25%

### 每日总能量消耗(TDEE)计算

TDEE由三部分组成：`TDEE = BMR + EAT + NEAT`

#### NEAT（非运动性热量消耗）

`NEAT(大卡) = (体重 × 2) + (步数/1000 × 体重 × 0.5)`

**示例：** 70kg用户，每日10000步
- NEAT = (70 × 2) + (10 × 70 × 0.5) = 490大卡

#### EAT（运动性热量消耗）

`EAT = BMR × 运动系数`

**运动系数计算：**
`运动系数 = (低强度天数 × 0.1 + 中强度天数 × 0.2 + 高强度天数 × 0.3) / 7`

| 训练强度 | 系数 | 示例运动类型 |
|---------|------|-------------|
| 低强度 | 0.1 | 散步、瑜伽、拉伸 |
| 中强度 | 0.2 | 慢跑、游泳、骑行 |
| 高强度 | 0.3 | HIIT、力量训练、冲刺跑 |

### 每日摄入量计算

`摄入量 = TDEE - 热量缺口`
`热量缺口 = 每周计划减脂重量(kg) × 7700 / 7`

### 营养素分配

**计算公式：**
- 蛋白质(g) = 体重(kg) × 1.8
- 脂肪(g) = 摄入热量 × 30% / 9
- 碳水(g) = (摄入热量 - 蛋白质×4 - 脂肪×9) / 4

**示例：** 70kg用户，摄入量1746大卡
- 蛋白质 = 70 × 1.8 = 126g → 504大卡
- 脂肪 = 1746 × 0.3 / 9 = 58g → 522大卡
- 碳水 = (1746 - 504 - 522) / 4 = 180g → 720大卡
- 验证：504 + 522 + 720 = 1746大卡 ✓

### 训练日营养调整

根据当日训练类型调整碳水摄入：

| 日类型 | 碳水调整 | 说明 |
|--------|----------|------|
| 力量训练日(strength) | 碳水 × 1.3 | 增加能量储备，支持高强度训练 |
| 有氧日(cardio) | 碳水 × 1.0 | 维持标准摄入 |
| 休息日(rest) | 碳水 × 0.7 | 减少能量需求 |

### 三餐热量分配原则

推荐三餐热量分配比例：
- **早餐：** 30%（提供上午能量）
- **午餐：** 40%（提供下午和运动能量）
- **晚餐：** 30%（避免晚餐过饱影响睡眠）

### 边界情况警告

**碳水过低警告：** 如果计算出的碳水 < 100g/天，会提示降低减重目标或增加运动量。

**热量摄入过低警告：** 如果摄入量 < BMR × 1.2，会提示每周减重目标不超过体重的1%。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
