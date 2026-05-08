import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def create_perfect_nightingale_rose():
    """创建完美的南丁格尔玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("🎯 成功加载Vue项目数据")
    except Exception as e:
        print(f"⚠️ 加载失败: {e}")
        return
    
    # 数据处理
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 只取前12个行业，让图表更清晰
    top_industries = industry_data.head(12)
    
    # 设置图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # 左侧：标准玫瑰图
    ax1_polar = plt.subplot(1, 2, 1, projection='polar')
    
    # 数据准备
    industries = list(top_industries.index)
    values = np.array(list(top_industries.values))
    n_sectors = len(industries)
    
    # 角度计算
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 创建美丽的颜色方案
    colors = []
    base_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                   '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
                   '#F8C471', '#82E0AA']
    
    for i in range(n_sectors):
        if i < len(base_colors):
            colors.append(base_colors[i])
        else:
            # 如果行业数量超过预设颜色，自动生成
            hue = i / n_sectors
            rgb = mcolors.hsv_to_rgb([hue, 0.7, 0.9])
            colors.append(mcolors.to_hex(rgb))
    
    # 绘制玫瑰图
    bars = ax1_polar.bar(theta, values, width=width, alpha=0.8, color=colors,
                        edgecolor='white', linewidth=3)
    
    # 设置极坐标样式
    ax1_polar.set_theta_zero_location('N')
    ax1_polar.set_theta_direction(-1)
    ax1_polar.set_title('南丁格尔玫瑰图\\n行业裁员分布', 
                       pad=30, fontsize=16, fontweight='bold')
    
    # 添加行业标签
    for i, (industry, value) in enumerate(top_industries.items()):
        angle = theta[i]
        
        # 行业标签
        label_radius = value + max(values) * 0.2
        ax1_polar.text(angle, label_radius, str(industry), 
                      ha='center', va='center', fontsize=10, fontweight='bold',
                      bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], 
                               alpha=0.8, edgecolor='white', linewidth=1))
        
        # 数值标签
        value_radius = value / 2
        ax1_polar.text(angle, value_radius, f'{int(value)}', 
                      ha='center', va='center', fontsize=11, fontweight='bold',
                      color='white',
                      bbox=dict(boxstyle="circle,pad=0.2", facecolor='black', alpha=0.7))
    
    # 美化网格
    ax1_polar.grid(True, alpha=0.3, linestyle='--')
    ax1_polar.set_facecolor('#f8f9fa')
    
    # 右侧：对比柱状图
    ax2.barh(industries, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('对比：水平柱状图\n同样数据的传统展示', fontsize=16, fontweight='bold')
    ax2.set_xlabel('裁员人数', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.set_facecolor('#f8f9fa')
    
    # 添加数值标签到柱状图
    for i, (industry, value) in enumerate(top_industries.items()):
        ax2.text(value + max(values) * 0.01, i, f'{int(value)}', 
                va='center', ha='left', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # 数据分析
    total = sum(values)
    print("\n" + "="*70)
    print("📊 TOP 12 行业裁员数据分析")
    print("="*70)
    for i, (industry, value) in enumerate(top_industries.items()):
        percentage = (value / total) * 100
        bar = "█" * int(percentage / 2)  # 简单的文字图表
        print(f"{i+1:2d}. {industry:15s} | {value:6d} | {percentage:5.1f}% | {bar}")
    
    print(f"\n📈 总计: {int(total):,} 人")
    print(f"📊 平均每行业: {int(total/len(top_industries)):,} 人")
    
    return top_industries

def create_comparison_visualization():
    \"\"\"创建玫瑰图与其他图表的对比\"\"\"
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception:
        return
    
    # 数据处理
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(8)
    
    # 创建对比图
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('南丁格尔玫瑰图 vs 其他图表类型', fontsize=18, fontweight='bold')
    
    industries = list(industry_data.index)
    values = np.array(list(industry_data.values))
    n_sectors = len(industries)
    
    # 颜色方案
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#F7DC6F']
    
    # 1. 南丁格尔玫瑰图
    ax1 = plt.subplot(2, 2, 1, projection='polar')
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    ax1.bar(theta, values, width=width, alpha=0.8, color=colors[:n_sectors],
            edgecolor='white', linewidth=2)
    ax1.set_title('南丁格尔玫瑰图', pad=20, fontweight='bold')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    
    # 2. 传统饼图
    ax2 = axes[0, 1]
    wedges, texts, autotexts = ax2.pie(values, labels=industries, autopct='%1.1f%%',
                                      colors=colors[:n_sectors], startangle=90)
    ax2.set_title('传统饼图', fontweight='bold')
    
    # 3. 垂直柱状图
    ax3 = axes[1, 0]
    bars = ax3.bar(industries, values, color=colors[:n_sectors], alpha=0.8,
                   edgecolor='white', linewidth=2)
    ax3.set_title('垂直柱状图', fontweight='bold')
    ax3.set_ylabel('裁员人数')
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. 水平柱状图
    ax4 = axes[1, 1]
    ax4.barh(industries, values, color=colors[:n_sectors], alpha=0.8,
             edgecolor='white', linewidth=2)
    ax4.set_title('水平柱状图', fontweight='bold')
    ax4.set_xlabel('裁员人数')
    
    plt.tight_layout()
    plt.show()
    
    print(\"\\n🎨 各图表类型特点对比:\")
    print(\"=\"*50)
    print(\"🌹 南丁格尔玫瑰图: 视觉冲击力强，美观度最高\")
    print(\"🥧 传统饼图: 占比清晰，但视觉效果一般\")
    print(\"📊 柱状图: 数值对比清晰，但缺乏设计感\")
    print(\"\\n💡 建议: 展示报告用玫瑰图，数据分析用柱状图\")

if __name__ == \"__main__\":
    print(\"🌹 南丁格尔玫瑰图 - 完美版本\")
    print(\"=\"*70)
    
    # 创建完美玫瑰图
    print(\"\\n1. 创建完美的南丁格尔玫瑰图\")
    top_industries = create_perfect_nightingale_rose()
    
    if top_industries is not None:
        print(\"\\n2. 创建图表类型对比\")
        create_comparison_visualization()
        
        print(\"\\n🎯 南丁格尔玫瑰图制作要点:\")
        print(\"=\"*50)
        print(\"✨ 选择合适的数据量 (建议8-12个分类)\")
        print(\"✨ 使用协调的色彩搭配\")
        print(\"✨ 添加清晰的标签和数值\")
        print(\"✨ 保持适当的透明度和边框\")
        print(\"✨ 美化背景和网格线\")
        print(\"✨ 添加标题和说明文字\")
        
        print(\"\\n🚀 玫瑰图 vs Vue项目中的ChartCircle.vue:\")
        print(\"- Vue项目: 使用ECharts实现，支持交互\")
        print(\"- Python版: 使用Matplotlib实现，静态但美观\")
        print(\"- 都能很好地展示分类数据的占比关系\")
        print(\"- 玫瑰图比普通饼图更有视觉冲击力\")
