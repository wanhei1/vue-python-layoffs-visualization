import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
                     'Manufacturing', 'Education', 'Transportation']
        
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 200),
            'Num': np.random.randint(100, 2000, 200)
        })
    
    # 按行业汇总数据
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建3个不同风格的玫瑰图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('南丁格尔玫瑰图 - 不同风格展示', fontsize=16, fontweight='bold')
    
    # 准备数据
    industries = list(industry_data.index)
    values = list(industry_data.values)
    n_sectors = len(industries)
    
    # 计算角度
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 1. 基础玫瑰图
    ax1 = plt.subplot(1, 3, 1, projection='polar')
    
    # 创建基础颜色
    colors1 = plt.cm.Set3(np.linspace(0, 1, n_sectors))
    
    # 绘制基础玫瑰图
    ax1.bar(theta, values, width=width, alpha=0.8, color=colors1, 
            edgecolor='white', linewidth=2)
    
    ax1.set_title('基础玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    
    # 2. 渐变色玫瑰图
    ax2 = plt.subplot(1, 3, 2, projection='polar')
    
    # 创建渐变色
    colors2 = plt.cm.viridis(np.linspace(0, 1, n_sectors))
    
    # 绘制渐变玫瑰图
    ax2.bar(theta, values, width=width, alpha=0.8, color=colors2, 
            edgecolor='white', linewidth=2)
    
    ax2.set_title('渐变色玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    
    # 添加数值标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        label_radius = value + max(values) * 0.1
        ax2.text(angle, label_radius, f'{int(value)}', 
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # 3. 高级美化玫瑰图
    ax3 = plt.subplot(1, 3, 3, projection='polar')
    
    # 创建彩虹色
    colors3 = plt.cm.rainbow(np.linspace(0, 1, n_sectors))
    
    # 绘制高级玫瑰图
    ax3.bar(theta, values, width=width, alpha=0.85, color=colors3, 
            edgecolor='black', linewidth=1)
    
    ax3.set_title('高级美化玫瑰图', pad=20, fontsize=12, fontweight='bold')
    ax3.set_theta_zero_location('N')
    ax3.set_theta_direction(-1)
    
    # 添加行业标签和数值
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        
        # 行业标签
        label_radius = value + max(values) * 0.15
        ax3.text(angle, label_radius, str(industry), 
                ha='center', va='center', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors3[i], alpha=0.7))
        
        # 数值标签
        value_radius = value / 2
        ax3.text(angle, value_radius, str(int(value)), 
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='white', 
                bbox=dict(boxstyle="circle,pad=0.1", facecolor='black', alpha=0.7))
    
    # 美化网格
    ax3.grid(True, alpha=0.3)
    ax3.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    plt.show()

def create_large_rose_chart():
    """创建大型精美玫瑰图"""
    
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
            'Num': np.random.randint(200, 1800, 150)
        })
    
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建大图
    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(projection='polar'))
    
    # 准备数据
    industries = list(industry_data.index)
    values = list(industry_data.values)
    n_sectors = len(industries)
    
    # 计算角度
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 创建HSV颜色空间的色彩
    colors = []
    for i in range(n_sectors):
        hue = i / n_sectors
        # 使用HSV色彩空间创建鲜艳的色彩
        rgb = mcolors.hsv_to_rgb([hue, 0.8, 0.9])
        colors.append(rgb)
    
    # 绘制玫瑰图
    bars = ax.bar(theta, values, width=width, alpha=0.8, color=colors, 
                  edgecolor='white', linewidth=3)
    
    # 设置样式
    ax.set_theta_zero_location('N')  # 0度在顶部
    ax.set_theta_direction(-1)  # 顺时针
    ax.set_title('南丁格尔玫瑰图 - 行业与裁员关系', 
                pad=40, fontsize=20, fontweight='bold')
    
    # 添加详细标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        
        # 外部行业标签
        label_radius = value + max(values) * 0.25
        ax.text(angle, label_radius, str(industry), 
                ha='center', va='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=colors[i], alpha=0.8,
                         edgecolor='white', linewidth=2))
        
        # 内部数值标签
        value_radius = value / 2.5
        ax.text(angle, value_radius, f'{int(value)}', 
                ha='center', va='center', fontsize=16, fontweight='bold',
                color='white',
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='black', alpha=0.8))
    
    # 美化网格和背景
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f8f8')
    
    # 添加说明文字
    ax.text(0, max(values) * 1.5, '扇形面积 = 裁员人数', 
            ha='center', va='center', fontsize=14, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.show()

def create_comparison_charts():
    """创建玫瑰图与其他图表的对比"""
    
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
            'Num': np.random.randint(100, 1000, 100)
        })
    
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建对比图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('玫瑰图 vs 其他图表类型对比', fontsize=16, fontweight='bold')
    
    # 1. 南丁格尔玫瑰图
    ax1 = plt.subplot(2, 2, 1, projection='polar')
    
    industries = list(industry_data.index)
    values = list(industry_data.values)
    n_sectors = len(industries)
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_sectors))
    ax1.bar(theta, values, width=width, alpha=0.8, color=colors, 
            edgecolor='white', linewidth=2)
    ax1.set_title('南丁格尔玫瑰图', pad=20, fontweight='bold')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    
    # 2. 传统饼图
    ax2 = axes[0, 1]
    ax2.pie(values, labels=industries, autopct='%1.1f%%', startangle=90,
            colors=colors)
    ax2.set_title('传统饼图', fontweight='bold')
    
    # 3. 柱状图
    ax3 = axes[1, 0]
    bars = ax3.bar(industries, values, color=colors, alpha=0.8)
    ax3.set_title('柱状图', fontweight='bold')
    ax3.set_ylabel('数值')
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. 环形图
    ax4 = axes[1, 1]
    wedges, texts, autotexts = ax4.pie(values, labels=industries, autopct='%1.1f%%',
                                      startangle=90, colors=colors,
                                      wedgeprops=dict(width=0.5))
    ax4.set_title('环形图', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("="*60)
    print("南丁格尔玫瑰图 - 美化版本展示")
    print("="*60)
    
    print("\n1. 三种风格的玫瑰图对比")
    create_beautiful_nightingale_rose()
    
    print("\n2. 大型精美玫瑰图")
    create_large_rose_chart()
    
    print("\n3. 玫瑰图与其他图表类型对比")
    create_comparison_charts()
    
    print("\n" + "="*60)
    print("南丁格尔玫瑰图的优势：")
    print("="*60)
    print("✨ 视觉冲击力强，美观度高")
    print("✨ 扇形面积直观表示数值大小")
    print("✨ 适合展示分类数据的占比关系")
    print("✨ 色彩丰富，易于区分类别")
    print("✨ 比传统饼图更有设计感")
    print("✨ 非常适合数据可视化展示")
