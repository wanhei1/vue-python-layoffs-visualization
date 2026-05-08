import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_beautiful_nightingale_rose():
    """创建美观的南丁格尔玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("成功加载真实数据")
    except:
        print("使用示例数据")
        # 创建示例数据
        np.random.seed(42)
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail', 
                     'Manufacturing', 'Education', 'Transportation', 'Media', 'Food']
        
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 200),
            'Num': np.random.randint(50, 2000, 200)
        })
    
    # 按行业汇总数据
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建图表
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('南丁格尔玫瑰图 - 不同风格实现', fontsize=16, fontweight='bold')
    
    # 1. 基础玫瑰图
    ax1 = axes[0]
    ax1 = plt.subplot(1, 3, 1, projection='polar')
    
    # 计算角度和半径
    theta = np.linspace(0, 2*np.pi, len(industry_data), endpoint=False)
    radii = industry_data.values
    width = 2*np.pi / len(industry_data)
    
    # 基础颜色
    colors = cm.Set3(np.linspace(0, 1, len(industry_data)))
    
    # 绘制基础玫瑰图
    bars = ax1.bar(theta, radii, width=width, alpha=0.8, color=colors, 
                   edgecolor='white', linewidth=1.5)
    
    ax1.set_title('基础玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    
    # 2. 渐变色玫瑰图
    ax2 = plt.subplot(1, 3, 2, projection='polar')
    
    # 创建渐变色
    gradient_colors = []
    for i in range(len(industry_data)):
        # 从蓝色到红色的渐变
        ratio = i / (len(industry_data) - 1)
        color = mcolors.to_rgba(plt.cm.coolwarm(ratio))
        gradient_colors.append(color)
    
    # 绘制渐变玫瑰图
    bars2 = ax2.bar(theta, radii, width=width, alpha=0.8, 
                    color=gradient_colors, edgecolor='white', linewidth=2)
    
    ax2.set_title('渐变色玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    
    # 添加数值标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        label_radius = radii[i] + max(radii) * 0.1
        ax2.text(angle, label_radius, f'{int(value)}', 
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # 3. 高级美化玫瑰图
    ax3 = plt.subplot(1, 3, 3, projection='polar')
    
    # 创建彩虹色谱
    rainbow_colors = cm.rainbow(np.linspace(0, 1, len(industry_data)))
    
    # 绘制高级玫瑰图
    bars3 = ax3.bar(theta, radii, width=width, alpha=0.85, 
                    color=rainbow_colors, edgecolor='black', linewidth=1)
    
    # 设置样式
    ax3.set_title('高级美化玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax3.set_theta_zero_location('N')
    ax3.set_theta_direction(-1)
    
    # 添加行业标签和数值
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        
        # 行业标签
        label_radius = radii[i] + max(radii) * 0.15
        ax3.text(angle, label_radius, industry, 
                ha='center', va='center', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=rainbow_colors[i], alpha=0.7))
        
        # 数值标签
        value_radius = radii[i] / 2
        ax3.text(angle, value_radius, str(int(value)), 
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='white', 
                bbox=dict(boxstyle="circle,pad=0.1", facecolor='black', alpha=0.7))
    
    # 设置网格样式
    ax3.grid(True, alpha=0.3)
    ax3.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    plt.show()

def create_interactive_rose_chart():
    """创建交互式风格的玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except:
        np.random.seed(42)
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail', 
                     'Manufacturing', 'Education', 'Transportation']
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 150),
            'Num': np.random.randint(100, 1500, 150)
        })
    
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建大图
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # 计算参数
    theta = np.linspace(0, 2*np.pi, len(industry_data), endpoint=False)
    radii = industry_data.values
    width = 2*np.pi / len(industry_data)
    
    # 创建渐变色彩
    colors = []
    for i in range(len(industry_data)):
        hue = i / len(industry_data)
        color = mcolors.hsv_to_rgb([hue, 0.8, 0.9])
        colors.append(color)
    
    # 绘制玫瑰图
    bars = ax.bar(theta, radii, width=width, alpha=0.8, color=colors, 
                  edgecolor='white', linewidth=3)
    
    # 设置样式
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('南丁格尔玫瑰图 - 行业与裁员关系', 
                pad=30, fontsize=18, fontweight='bold')
    
    # 添加标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        
        # 外部标签
        label_radius = radii[i] + max(radii) * 0.2
        ax.text(angle, label_radius, industry, 
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=colors[i], alpha=0.8,
                         edgecolor='white', linewidth=2))
        
        # 内部数值
        value_radius = radii[i] / 2.5
        ax.text(angle, value_radius, f'{int(value)}', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                color='white',
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='black', alpha=0.8))
    
    # 美化网格
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f0f0f0')
    
    # 添加说明
    ax.text(0, max(radii) * 1.4, '数据：裁员人数统计', 
            ha='center', va='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.show()

def create_multi_layer_rose():
    """创建多层玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except:
        np.random.seed(42)
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail']
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 100),
            'Num': np.random.randint(50, 1000, 100),
            'Year': np.random.choice([2022, 2023, 2024], 100)
        })
    
    # 按年份和行业汇总
    pivot_data = df.pivot_table(values='Num', index='Industry', columns='Year', 
                               aggfunc='sum', fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # 计算角度
    theta = np.linspace(0, 2*np.pi, len(pivot_data.index), endpoint=False)
    width = 2*np.pi / len(pivot_data.index)
    
    # 绘制多层玫瑰图
    years = pivot_data.columns
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, year in enumerate(years):
        radii = pivot_data[year].values
        bars = ax.bar(theta, radii, width=width, alpha=0.7, 
                     color=colors[i], label=f'{year}年',
                     bottom=sum(pivot_data[y].values for y in years[:i]))
    
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('多层玫瑰图 - 年度行业对比', pad=30, fontsize=16, fontweight='bold')
    
    # 添加标签
    for i, industry in enumerate(pivot_data.index):
        angle = theta[i]
        total_height = sum(pivot_data.loc[industry, y] for y in years)
        label_radius = total_height + max(pivot_data.values.flatten()) * 0.1
        ax.text(angle, label_radius, industry, 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("="*60)
    print("南丁格尔玫瑰图 - 美化版本")
    print("="*60)
    
    print("\n1. 基础、渐变、高级三种风格对比")
    create_beautiful_nightingale_rose()
    
    print("\n2. 交互式风格大图")
    create_interactive_rose_chart()
    
    print("\n3. 多层玫瑰图")
    create_multi_layer_rose()
    
    print("\n南丁格尔玫瑰图特点:")
    print("- 扇形面积代表数值大小")
    print("- 颜色区分不同类别")
    print("- 视觉冲击力强")
    print("- 适合展示分类数据的对比")
