#!/usr/bin/env python3
"""
模板处理器 - 将每日记录模板中的变量替换为实际计算的推荐值
"""

import yaml
import re
from nutrition_calculator import get_recommendation_data


def load_template(template_path):
    """
    加载模板文件
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def replace_template_variables(template_content, recommendation_data):
    """
    将模板中的变量替换为实际值
    """
    data = recommendation_data

    # 替换总热量和营养素
    replacements = {
        '{{total_calories_min}}': str(data['total_recommended']['calories']['min']),
        '{{total_calories_max}}': str(data['total_recommended']['calories']['max']),
        '{{total_protein_min}}': str(data['total_recommended']['protein']['min']),
        '{{total_protein_max}}': str(data['total_recommended']['protein']['max']),
        '{{total_carbs_min}}': str(data['total_recommended']['carbs']['min']),
        '{{total_carbs_max}}': str(data['total_recommended']['carbs']['max']),
        '{{total_fat_min}}': str(data['total_recommended']['fat']['min']),
        '{{total_fat_max}}': str(data['total_recommended']['fat']['max']),

        # 早餐
        '{{breakfast_calories_min}}': str(data['meal_nutrition']['breakfast']['calories']['min']),
        '{{breakfast_calories_max}}': str(data['meal_nutrition']['breakfast']['calories']['max']),
        '{{breakfast_protein_min}}': str(data['meal_nutrition']['breakfast']['protein']['min']),
        '{{breakfast_protein_max}}': str(data['meal_nutrition']['breakfast']['protein']['max']),
        '{{breakfast_carbs_min}}': str(data['meal_nutrition']['breakfast']['carbs']['min']),
        '{{breakfast_carbs_max}}': str(data['meal_nutrition']['breakfast']['carbs']['max']),
        '{{breakfast_fat_min}}': str(data['meal_nutrition']['breakfast']['fat']['min']),
        '{{breakfast_fat_max}}': str(data['meal_nutrition']['breakfast']['fat']['max']),

        # 午餐
        '{{lunch_calories_min}}': str(data['meal_nutrition']['lunch']['calories']['min']),
        '{{lunch_calories_max}}': str(data['meal_nutrition']['lunch']['calories']['max']),
        '{{lunch_protein_min}}': str(data['meal_nutrition']['lunch']['protein']['min']),
        '{{lunch_protein_max}}': str(data['meal_nutrition']['lunch']['protein']['max']),
        '{{lunch_carbs_min}}': str(data['meal_nutrition']['lunch']['carbs']['min']),
        '{{lunch_carbs_max}}': str(data['meal_nutrition']['lunch']['carbs']['max']),
        '{{lunch_fat_min}}': str(data['meal_nutrition']['lunch']['fat']['min']),
        '{{lunch_fat_max}}': str(data['meal_nutrition']['lunch']['fat']['max']),

        # 晚餐
        '{{dinner_calories_min}}': str(data['meal_nutrition']['dinner']['calories']['min']),
        '{{dinner_calories_max}}': str(data['meal_nutrition']['dinner']['calories']['max']),
        '{{dinner_protein_min}}': str(data['meal_nutrition']['dinner']['protein']['min']),
        '{{dinner_protein_max}}': str(data['meal_nutrition']['dinner']['protein']['max']),
        '{{dinner_carbs_min}}': str(data['meal_nutrition']['dinner']['carbs']['min']),
        '{{dinner_carbs_max}}': str(data['meal_nutrition']['dinner']['carbs']['max']),
        '{{dinner_fat_min}}': str(data['meal_nutrition']['dinner']['fat']['min']),
        '{{dinner_fat_max}}': str(data['meal_nutrition']['dinner']['fat']['max']),

        # 加餐
        '{{snack_calories_min}}': str(data['meal_nutrition']['snack']['calories']['min']),
        '{{snack_calories_max}}': str(data['meal_nutrition']['snack']['calories']['max']),
        '{{snack_protein_min}}': str(data['meal_nutrition']['snack']['protein']['min']),
        '{{snack_protein_max}}': str(data['meal_nutrition']['snack']['protein']['max']),
        '{{snack_carbs_min}}': str(data['meal_nutrition']['snack']['carbs']['min']),
        '{{snack_carbs_max}}': str(data['meal_nutrition']['snack']['carbs']['max']),
        '{{snack_fat_min}}': str(data['meal_nutrition']['snack']['fat']['min']),
        '{{snack_fat_max}}': str(data['meal_nutrition']['snack']['fat']['max']),
    }

    # 进行替换
    processed_content = template_content
    for variable, value in replacements.items():
        processed_content = processed_content.replace(variable, value)

    # 清理未替换的变量（如果有的话）
    processed_content = re.sub(r'\{\{.*?\}\}', '___', processed_content)

    return processed_content


def generate_daily_record_template(config_path, output_template_path=None):
    """
    生成包含实际推荐值的每日记录模板
    """
    # 加载配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 获取推荐数据
    recommendation_data = get_recommendation_data(config)

    # 加载原始模板
    # 注意：这里需要根据实际路径调整
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skill_md_path = os.path.join(current_dir, '..', 'skill.md')
    template_content = None

    if os.path.exists(skill_md_path):
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            # 提取模板部分
            content = f.read()
            # 找到每日记录模板的起始和结束位置
            start_marker = '### 早餐'
            end_marker = '```'

            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker, start_idx)

            if start_idx != -1 and end_idx != -1:
                template_content = content[start_idx:end_idx + len(end_marker)]

    if not template_content:
        # 如果找不到完整模板，使用基本结构
        template_content = """## 🍽️ 饮食记录

### 早餐
| 食物名称 | 用量 | 预估热量(kcal) | 蛋白质(g) | 碳水(g) | 脂肪(g) |
|---------|------|---------------|----------|---------|--------|
| | | | | | |
| **小计** | - | ___ | ___ | ___ | ___ |
| **推荐** | - | {{breakfast_calories_min}}-{{breakfast_calories_max}} | {{breakfast_protein_min}}-{{breakfast_protein_max}} | {{breakfast_carbs_min}}-{{breakfast_carbs_max}} | {{breakfast_fat_min}}-{{breakfast_fat_max}} |

### 午餐
| 食物名称 | 用量 | 预估热量(kcal) | 蛋白质(g) | 碳水(g) | 脂肪(g) |
|---------|------|---------------|----------|---------|--------|
| | | | | | |
| **小计** | - | ___ | ___ | ___ | ___ |
| **推荐** | - | {{lunch_calories_min}}-{{lunch_calories_max}} | {{lunch_protein_min}}-{{lunch_protein_max}} | {{lunch_carbs_min}}-{{lunch_carbs_max}} | {{lunch_fat_min}}-{{lunch_fat_max}} |

### 晚餐
| 食物名称 | 用量 | 预估热量(kcal) | 蛋白质(g) | 碳水(g) | 脂肪(g) |
|---------|------|---------------|----------|---------|--------|
| | | | | | |
| **小计** | - | ___ | ___ | ___ | ___ |
| **推荐** | - | {{dinner_calories_min}}-{{dinner_calories_max}} | {{dinner_protein_min}}-{{dinner_protein_max}} | {{dinner_carbs_min}}-{{dinner_carbs_max}} | {{dinner_fat_min}}-{{dinner_fat_max}} |

### 加餐
| 食物名称 | 用量 | 预估热量(kcal) | 蛋白质(g) | 碳水(g) | 脂肪(g) |
|---------|------|---------------|----------|---------|--------|
| | | | | | |
| **小计** | - | ___ | ___ | ___ | ___ |
| **推荐** | - | {{snack_calories_min}}-{{snack_calories_max}} | {{snack_protein_min}}-{{snack_protein_max}} | {{snack_carbs_min}}-{{snack_carbs_max}} | {{snack_fat_min}}-{{snack_fat_max}} |

---

**今日营养汇总：**
- 总热量：___ kcal（推荐：{{total_calories_min}}-{{total_calories_max}} kcal）
- 蛋白质：___ g（推荐：{{total_protein_min}}-{{total_protein_max}} g）
- 碳水：___ g（推荐：{{total_carbs_min}}-{{total_carbs_max}} g）
- 脂肪：___ g（推荐：{{total_fat_min}}-{{total_fat_max}} g）
"""

    # 替换变量
    processed_template = replace_template_variables(template_content, recommendation_data)

    # 保存输出文件
    if output_template_path:
        with open(output_template_path, 'w', encoding='utf-8') as f:
            f.write(processed_template)
        print(f"处理后的模板已保存到: {output_template_path}")

    return processed_template


def main():
    import argparse
    parser = argparse.ArgumentParser(description='处理每日记录模板，替换为实际推荐值')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--output', help='输出文件路径')

    args = parser.parse_args()

    try:
        result = generate_daily_record_template(args.config, args.output)
        if not args.output:
            print(result)
    except Exception as e:
        print(f"错误: {e}")


if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()