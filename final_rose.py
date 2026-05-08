import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_rainbow_style():
    """创建彩虹风格的玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception:
        return
    
    # 数据处理
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(8)
    
    # 创建单个彩虹风格图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('彩虹风格南丁格尔玫瑰图与柱状图对比', fontsize=16, fontweight='bold')
    
    # 数据准备
    industries = list(industry_data.index)
    values = np.array(list(industry_data.values))
    n_sectors = len(industries)
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 彩虹风格玫瑰图
    ax1_polar = plt.subplot(1, 2, 1, projection='polar')
    from matplotlib import cm
    colors = cm.get_cmap('rainbow')(np.linspace(0, 1, n_sectors))
    ax1_polar.bar(theta, values, width=width, alpha=0.8, color=colors,
                  edgecolor='black', linewidth=1)
    ax1_polar.set_title('彩虹风格玫瑰图', pad=20, fontweight='bold')
    
    # 为彩虹风格添加标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        label_radius = value + max(values) * 0.1
        ax1_polar.text(angle, label_radius, str(industry)[:6], 
                      ha='center', va='center', fontsize=9, fontweight='bold',
                      bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # 右侧：对比柱状图
    ax2.barh(industries, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('对比：彩虹风格柱状图', fontsize=14, fontweight='bold')
    ax2.set_xlabel('裁员人数', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.set_facecolor('#f8f9fa')
    
    # 添加数值标签到柱状图
    for i, (industry, value) in enumerate(industry_data.items()):
        ax2.text(value + max(values) * 0.01, i, f'{int(value)}', 
                va='center', ha='left', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("🌹 南丁格尔玫瑰图 - 彩虹风格版本")
    print("="*50)
    
    # 加载数据并创建彩虹风格图表
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("✅ 成功加载Vue项目数据")
        
        # 数据分析
        industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(10)
        total = sum(industry_data.values)
        print("\n" + "="*60)
        print("📊 TOP 10 行业裁员数据分析")
        print("="*60)
        
        for i, (industry, value) in enumerate(industry_data.items()):
            percentage = (value / total) * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"{i+1:2d}. {industry:15s} | {value:6d} | {percentage:5.1f}% | {bar}")
        
        print(f"\n📈 总计: {int(total):,} 人")
        print(f"📊 平均每行业: {int(total/len(industry_data)):,} 人")
        
        print("\n创建彩虹风格的玫瑰图")
        create_rainbow_style()
        
        print("\n🎨 南丁格尔玫瑰图的优势:")
        print("="*40)
        print("✨ 视觉冲击力强，比普通饼图更美观")
        print("✨ 扇形面积直观表示数值大小")
        print("✨ 色彩丰富，容易区分不同类别")
        print("✨ 适合展示分类数据的占比关系")
        print("✨ 非常适合数据可视化报告")
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")
