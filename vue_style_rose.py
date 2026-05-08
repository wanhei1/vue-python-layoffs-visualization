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

def create_vue_style_rose():
    """创建类似Vue项目风格的玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("✅ 成功加载项目数据")
    except Exception as e:
        print(f"⚠️ 数据加载失败: {e}")
        print("使用模拟数据")
        # 模拟Vue项目中的行业数据
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail', 
                     'Transportation', 'Manufacturing', 'Education', 'Media', 'Food']
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 300),
            'Num': np.random.randint(50, 1500, 300)
        })
    
    # 按行业统计数据
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建大型美观玫瑰图
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='polar')
    
    # 数据准备
    industries = list(industry_data.index)
    values = np.array(list(industry_data.values))
    n_sectors = len(industries)
    
    # 角度计算
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 创建渐变色彩方案
    colors = []
    for i in range(n_sectors):
        # 使用HSV色彩空间创建丰富的颜色
        hue = i / n_sectors
        saturation = 0.8 + 0.2 * np.sin(i * np.pi / 4)  # 添加一些变化
        value = 0.9
        rgb = mcolors.hsv_to_rgb([hue, saturation, value])
        colors.append(rgb)
    
    # 绘制玫瑰图主体
    bars = ax.bar(theta, values, width=width, alpha=0.85, color=colors,
                  edgecolor='white', linewidth=3)
    
    # 添加渐变效果
    for bar, color in zip(bars, colors):
        # 为每个扇形添加渐变效果
        bar.set_facecolor(color)
        bar.set_alpha(0.85)
    
    # 设置极坐标样式
    ax.set_theta_zero_location('N')  # 0度在顶部
    ax.set_theta_direction(-1)  # 顺时针方向
    
    # 美化标题
    ax.set_title('南丁格尔玫瑰图\\n行业与裁员关系可视化', 
                pad=40, fontsize=24, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))
    
    # 添加行业标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        
        # 外部标签位置
        label_radius = value + max(values) * 0.3
        
        # 行业名称标签
        ax.text(angle, label_radius, str(industry), 
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", facecolor=colors[i], alpha=0.9,
                         edgecolor='white', linewidth=2))
        
        # 数值标签 - 放在扇形中心
        value_radius = value / 2.5
        ax.text(angle, value_radius, f'{int(value)}', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                color='white',
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='black', alpha=0.8))
        
        # 添加百分比标签
        percentage = (value / sum(values)) * 100
        percent_radius = value * 0.8
        ax.text(angle, percent_radius, f'{percentage:.1f}%', 
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='white', alpha=0.9)
    
    # 美化网格
    ax.grid(True, alpha=0.3, linestyle='--', color='gray')
    ax.set_facecolor('#f8f9fa')
    
    # 添加说明文字
    ax.text(0, max(values) * 1.6, '扇形面积代表裁员人数', 
            ha='center', va='center', fontsize=14, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.7))
    
    # 添加数据统计信息
    total_layoffs = sum(values)
    ax.text(np.pi, max(values) * 1.6, f'总裁员人数: {int(total_layoffs)}', 
            ha='center', va='center', fontsize=14, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.7))
    
    plt.tight_layout()
    plt.show()
    
    # 打印统计信息
    print("\\n" + "="*60)
    print("📊 数据统计结果")
    print("="*60)
    for i, (industry, value) in enumerate(industry_data.items()):
        percentage = (value / total_layoffs) * 100
        print(f"{i+1:2d}. {industry:15s} | 裁员: {value:6d} | 占比: {percentage:5.1f}%")
    
    return industry_data

def create_animated_style_rose():
    """创建动画风格的玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception:
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail']
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 200),
            'Num': np.random.randint(100, 1200, 200)
        })
    
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    
    # 创建多个子图展示不同效果
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('南丁格尔玫瑰图 - 多种美化效果', fontsize=18, fontweight='bold')
    
    industries = list(industry_data.index)
    values = np.array(list(industry_data.values))
    n_sectors = len(industries)
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 1. 经典风格
    ax1 = plt.subplot(2, 2, 1, projection='polar')
    colors1 = plt.cm.Set3(np.linspace(0, 1, n_sectors))
    ax1.bar(theta, values, width=width, alpha=0.8, color=colors1,
            edgecolor='white', linewidth=2)
    ax1.set_title('经典风格', pad=20, fontweight='bold')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    
    # 2. 现代风格
    ax2 = plt.subplot(2, 2, 2, projection='polar')
    colors2 = plt.cm.viridis(np.linspace(0, 1, n_sectors))
    ax2.bar(theta, values, width=width, alpha=0.9, color=colors2,
            edgecolor='black', linewidth=1)
    ax2.set_title('现代风格', pad=20, fontweight='bold')
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    ax2.set_facecolor('#2f2f2f')
    
    # 3. 彩虹风格
    ax3 = plt.subplot(2, 2, 3, projection='polar')
    colors3 = plt.cm.rainbow(np.linspace(0, 1, n_sectors))
    ax3.bar(theta, values, width=width, alpha=0.8, color=colors3,
            edgecolor='white', linewidth=3)
    ax3.set_title('彩虹风格', pad=20, fontweight='bold')
    ax3.set_theta_zero_location('N')
    ax3.set_theta_direction(-1)
    
    # 4. 渐变风格
    ax4 = plt.subplot(2, 2, 4, projection='polar')
    colors4 = plt.cm.plasma(np.linspace(0, 1, n_sectors))
    bars4 = ax4.bar(theta, values, width=width, alpha=0.85, color=colors4,
                    edgecolor='white', linewidth=2)
    ax4.set_title('渐变风格', pad=20, fontweight='bold')
    ax4.set_theta_zero_location('N')
    ax4.set_theta_direction(-1)
    
    # 为渐变风格添加标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        label_radius = value + max(values) * 0.1
        ax4.text(angle, label_radius, str(industry)[:3], 
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='white',
                bbox=dict(boxstyle="round,pad=0.2", facecolor=colors4[i], alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("🌹 南丁格尔玫瑰图美化版本")
    print("="*60)
    
    print("\\n1. 创建Vue项目风格的玫瑰图")
    industry_data = create_vue_style_rose()
    
    print("\\n2. 创建多种美化效果对比")
    create_animated_style_rose()
    
    print("\\n🎨 玫瑰图美化技巧:")
    print("="*60)
    print("✨ 使用HSV色彩空间创建丰富颜色")
    print("✨ 添加白色边框增强视觉效果")
    print("✨ 合理使用透明度和渐变")
    print("✨ 添加数值和百分比标签")
    print("✨ 美化背景和网格线")
    print("✨ 使用合适的字体和布局")
    print("\\n🎯 南丁格尔玫瑰图最适合:")
    print("- 展示分类数据的占比关系")
    print("- 突出最重要的几个类别")
    print("- 创建视觉冲击力强的图表")
    print("- 数据可视化报告和展示")
