#!/usr/bin/env python3
"""
营养计算器 - 根据用户信息计算每日推荐热量和营养摄入

使用方法:
    python nutrition_calculator.py --config config.yaml
"""

import argparse
import yaml
import math

def calculate_bmr(weight, height, age, gender):
    """
    计算基础代谢率(BMR) - Mifflin-St Jeor公式
    """
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return 10 * weight + 6.25 * height - 5 * age


def get_base_activity_factor(current_activity):
    """
    根据当前运动频率获取基础活动系数
    """
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.3,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return activity_factors.get(current_activity.lower(), 1.55)


def get_activity_adjustment(past_activity):
    """
    根据运动基础获取调整系数
    """
    adjustment_factors = {
        'none': 0.0,        # 无基础，按当前活动
        'slight': 0.05,     # 略有基础，稍微提高
        'good': 0.1,       # 基础不错，提高10%
        'strong': 0.15,     # 基础很好，提高15%
        'professional': 0.25 # 专业运动员，提高25%
    }
    return adjustment_factors.get(past_activity.lower(), 0.0)


def calculate_daily_calories(weight, height, age, gender, past_activity, current_activity, weekly_weight_loss):
    """
    计算每日目标热量
    """
    # 基础代谢率
    bmr = calculate_bmr(weight, height, age, gender)

    # 获取基础活动系数
    base_factor = get_base_activity_factor(current_activity)

    # 根据运动基础调整活动系数
    adjustment = get_activity_adjustment(past_activity)
    activity_factor = base_factor + adjustment

    # 限制活动系数在合理范围内
    activity_factor = max(1.2, min(activity_factor, 2.0))

    # 每日总消耗(TDEE)
    tdee = bmr * activity_factor

    # 每日热量缺口
    daily_deficit = weekly_weight_loss * 7700 / 7

    # 目标热量
    target_calories = tdee - daily_deficit

    return bmr, base_factor, adjustment, activity_factor, tdee, target_calories


def calculate_nutrition(target_calories, weight):
    """
    计算营养摄入目标
    """
    # 蛋白质: 1.6-2.2g/kg
    protein_g = 2.0 * weight
    protein_calories = protein_g * 4

    # 脂肪: 0.8-1.0g/kg
    fat_g = 0.9 * weight
    fat_calories = fat_g * 9

    # 碳水化合物: 剩余热量
    carb_calories = target_calories - protein_calories - fat_calories
    carb_g = carb_calories / 4

    return {
        'protein': {
            'grams': round(protein_g, 1),
            'calories': round(protein_calories, 0),
            'percentage': round(protein_calories / target_calories * 100, 0),
            'range': {
                'min': round(1.6 * weight, 1),
                'max': round(2.2 * weight, 1)
            }
        },
        'fat': {
            'grams': round(fat_g, 1),
            'calories': round(fat_calories, 0),
            'percentage': round(fat_calories / target_calories * 100, 0),
            'range': {
                'min': round(0.8 * weight, 1),
                'max': round(1.0 * weight, 1)
            }
        },
        'carbs': {
            'grams': round(carb_g, 1),
            'calories': round(carb_calories, 0),
            'percentage': round(carb_calories / target_calories * 100, 0),
            'range': {
                'min': round(2.0 * weight, 1),
                'max': round(3.0 * weight, 1)
            }
        }
    }


def calculate_meal_distribution(target_calories):
    """
    计算三餐热量分配
    """
    return {
        'breakfast': {
            'min': round(target_calories * 0.25, 0),
            'max': round(target_calories * 0.30, 0)
        },
        'lunch': {
            'min': round(target_calories * 0.35, 0),
            'max': round(target_calories * 0.40, 0)
        },
        'dinner': {
            'min': round(target_calories * 0.30, 0),
            'max': round(target_calories * 0.35, 0)
        },
        'snack': {
            'min': round(target_calories * 0.05, 0),
            'max': round(target_calories * 0.10, 0)
        }
    }


def calculate_meal_nutrition(target_calories, weight):
    """
    计算每个餐次的推荐热量和营养素范围
    """
    meal_distribution = calculate_meal_distribution(target_calories)
    nutrition = calculate_nutrition(target_calories, weight)

    meals = {}
    for meal, calories in meal_distribution.items():
        # 计算每个餐次的营养素范围（根据总营养素范围的比例分配）
        meals[meal] = {
            'calories': calories,
            'protein': {
                'min': round(nutrition['protein']['range']['min'] * calories['min'] / target_calories, 1),
                'max': round(nutrition['protein']['range']['max'] * calories['max'] / target_calories, 1)
            },
            'carbs': {
                'min': round(nutrition['carbs']['range']['min'] * calories['min'] / target_calories, 1),
                'max': round(nutrition['carbs']['range']['max'] * calories['max'] / target_calories, 1)
            },
            'fat': {
                'min': round(nutrition['fat']['range']['min'] * calories['min'] / target_calories, 1),
                'max': round(nutrition['fat']['range']['max'] * calories['max'] / target_calories, 1)
            }
        }

    return meals


def get_recommendation_data(config):
    """
    获取推荐结果数据
    """
    user_info = config['user_info']
    weight_loss_goal = config['weight_loss_goal']

    bmr, base_factor, adjustment, activity_factor, tdee, target_calories = calculate_daily_calories(
        user_info['current_weight'],
        user_info['height'],
        user_info['age'],
        user_info['gender'],
        user_info['past_activity'],
        user_info['current_activity'],
        weight_loss_goal['weekly_rate']
    )

    nutrition = calculate_nutrition(target_calories, user_info['current_weight'])
    meal_nutrition = calculate_meal_nutrition(target_calories, user_info['current_weight'])

    return {
        'user_info': user_info,
        'weight_loss_goal': weight_loss_goal,
        'bmr': round(bmr, 0),
        'base_factor': base_factor,
        'adjustment': adjustment,
        'activity_factor': round(activity_factor, 2),
        'tdee': round(tdee, 0),
        'calorie_deficit': round(tdee - target_calories, 0),
        'target_calories': round(target_calories, 0),
        'nutrition': nutrition,
        'meal_nutrition': meal_nutrition,
        'total_recommended': {
            'calories': {
                'min': round(target_calories * 0.95, 0),
                'max': round(target_calories * 1.05, 0)
            },
            'protein': {
                'min': nutrition['protein']['range']['min'],
                'max': nutrition['protein']['range']['max']
            },
            'carbs': {
                'min': nutrition['carbs']['range']['min'],
                'max': nutrition['carbs']['range']['max']
            },
            'fat': {
                'min': nutrition['fat']['range']['min'],
                'max': nutrition['fat']['range']['max']
            }
        }
    }


def print_recommendation(config):
    """
    打印推荐结果
    """
    data = get_recommendation_data(config)

    print("🎯 营养摄入推荐")
    print("=" * 50)
    print(f"用户信息: {data['user_info']['nickname']}")
    print(f"当前体重: {data['user_info']['current_weight']}kg")
    print(f"目标体重: {data['user_info']['target_weight']}kg")
    print(f"身高: {data['user_info']['height']}cm")
    print(f"年龄: {data['user_info']['age']}")
    print(f"性别: {data['user_info']['gender']}")
    print(f"运动基础: {data['user_info']['past_activity']}")
    print(f"当前/计划运动频率: {data['user_info']['current_activity']}")
    print(f"每周目标减重: {data['weight_loss_goal']['weekly_rate']}kg")
    print("=" * 50)

    print(f"\n基础代谢率(BMR): {data['bmr']}千卡/天")
    print(f"基础活动系数: {data['base_factor']}")
    print(f"运动基础调整系数: +{data['adjustment']}")
    print(f"最终活动系数: {data['activity_factor']}")
    print(f"每日总消耗(TDEE): {data['tdee']}千卡/天")
    print(f"每日热量缺口: {data['calorie_deficit']}千卡/天")
    print(f"每日目标热量: {data['target_calories']}千卡/天")

    print("\n营养分配建议:")
    print(f"蛋白质: {data['nutrition']['protein']['grams']}g ({data['nutrition']['protein']['calories']}千卡, {data['nutrition']['protein']['percentage']}%)")
    print(f"脂肪: {data['nutrition']['fat']['grams']}g ({data['nutrition']['fat']['calories']}千卡, {data['nutrition']['fat']['percentage']}%)")
    print(f"碳水化合物: {data['nutrition']['carbs']['grams']}g ({data['nutrition']['carbs']['calories']}千卡, {data['nutrition']['carbs']['percentage']}%)")

    print("\n三餐热量和营养分配:")
    print(f"早餐: {data['meal_nutrition']['breakfast']['calories']['min']}-{data['meal_nutrition']['breakfast']['calories']['max']}千卡")
    print(f"  蛋白质: {data['meal_nutrition']['breakfast']['protein']['min']}-{data['meal_nutrition']['breakfast']['protein']['max']}g")
    print(f"  碳水化合物: {data['meal_nutrition']['breakfast']['carbs']['min']}-{data['meal_nutrition']['breakfast']['carbs']['max']}g")
    print(f"  脂肪: {data['meal_nutrition']['breakfast']['fat']['min']}-{data['meal_nutrition']['breakfast']['fat']['max']}g")

    print(f"\n午餐: {data['meal_nutrition']['lunch']['calories']['min']}-{data['meal_nutrition']['lunch']['calories']['max']}千卡")
    print(f"  蛋白质: {data['meal_nutrition']['lunch']['protein']['min']}-{data['meal_nutrition']['lunch']['protein']['max']}g")
    print(f"  碳水化合物: {data['meal_nutrition']['lunch']['carbs']['min']}-{data['meal_nutrition']['lunch']['carbs']['max']}g")
    print(f"  脂肪: {data['meal_nutrition']['lunch']['fat']['min']}-{data['meal_nutrition']['lunch']['fat']['max']}g")

    print(f"\n晚餐: {data['meal_nutrition']['dinner']['calories']['min']}-{data['meal_nutrition']['dinner']['calories']['max']}千卡")
    print(f"  蛋白质: {data['meal_nutrition']['dinner']['protein']['min']}-{data['meal_nutrition']['dinner']['protein']['max']}g")
    print(f"  碳水化合物: {data['meal_nutrition']['dinner']['carbs']['min']}-{data['meal_nutrition']['dinner']['carbs']['max']}g")
    print(f"  脂肪: {data['meal_nutrition']['dinner']['fat']['min']}-{data['meal_nutrition']['dinner']['fat']['max']}g")

    print(f"\n加餐: {data['meal_nutrition']['snack']['calories']['min']}-{data['meal_nutrition']['snack']['calories']['max']}千卡")
    print(f"  蛋白质: {data['meal_nutrition']['snack']['protein']['min']}-{data['meal_nutrition']['snack']['protein']['max']}g")
    print(f"  碳水化合物: {data['meal_nutrition']['snack']['carbs']['min']}-{data['meal_nutrition']['snack']['carbs']['max']}g")
    print(f"  脂肪: {data['meal_nutrition']['snack']['fat']['min']}-{data['meal_nutrition']['snack']['fat']['max']}g")

    print("\n💡 建议")
    print("- 确保每日热量缺口不超过1000千卡")
    print("- 优先保证蛋白质摄入，防止肌肉流失")
    print("- 碳水化合物提供运动能量，避免过度限制")
    print("- 脂肪摄入要适度，保证激素正常分泌")
    print("- 结合饮食记录和运动，定期调整")

    return data


def main():
    parser = argparse.ArgumentParser(
        description='营养计算器 - 根据用户信息计算每日推荐热量和营养摄入')
    parser.add_argument('--config', default='config.yaml',
                     help='配置文件路径 (default: config.yaml)')

    args = parser.parse_args()

    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print_recommendation(config)

    except FileNotFoundError:
        print(f"错误: 配置文件 '{args.config}' 未找到")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
