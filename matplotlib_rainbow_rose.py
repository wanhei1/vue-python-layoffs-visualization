import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_matplotlib_rainbow_rose():
    """用matplotlib重现final_rose.py的彩虹风格玫瑰图"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("✅ 成功加载Vue项目数据")
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return
    
    # 数据处理 - 与final_rose.py保持一致
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(8)
    
    # 创建彩虹风格图表 - 与final_rose.py布局一致
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Matplotlib版本：彩虹风格南丁格尔玫瑰图与柱状图对比', fontsize=16, fontweight='bold')
    
    # 数据准备
    industries = list(industry_data.index)
    values = np.array(list(industry_data.values))
    n_sectors = len(industries)
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    
    # 左侧：彩虹风格南丁格尔玫瑰图
    ax1_polar = plt.subplot(1, 2, 1, projection='polar')
    
    # 使用与final_rose.py相同的彩虹色彩
    from matplotlib import cm
    colors = cm.get_cmap('rainbow')(np.linspace(0, 1, n_sectors))
    
    # 绘制玫瑰图
    bars = ax1_polar.bar(theta, values, width=width, alpha=0.8, color=colors,
                        edgecolor='black', linewidth=1)
    ax1_polar.set_title('Matplotlib彩虹风格玫瑰图', pad=20, fontweight='bold')
    
    # 添加行业标签 - 与final_rose.py一致（不显示人数）
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        label_radius = value + max(values) * 0.1
        ax1_polar.text(angle, label_radius, str(industry)[:6], 
                      ha='center', va='center', fontsize=9, fontweight='bold',
                      bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # 右侧：对比柱状图 - 与final_rose.py保持一致
    ax2.barh(industries, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('对比：Matplotlib彩虹风格柱状图', fontsize=14, fontweight='bold')
    ax2.set_xlabel('裁员人数', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.set_facecolor('#f8f9fa')
    
    # 添加数值标签到柱状图
    for i, (industry, value) in enumerate(industry_data.items()):
        ax2.text(value + max(values) * 0.01, i, f'{int(value)}', 
                va='center', ha='left', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return industry_data

def create_enhanced_rainbow_charts():
    """创建增强版的彩虹风格图表集合"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception:
        return
    
    # 创建2x2子图布局
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('增强版彩虹风格可视化集合', fontsize=16, fontweight='bold')
    
    # 数据处理
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(10)
    
    # 1. 彩虹玫瑰图 (左上)
    ax1_polar = plt.subplot(2, 2, 1, projection='polar')
    n_sectors = len(industry_data)
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
    width = 2*np.pi / n_sectors
    colors = plt.cm.rainbow(np.linspace(0, 1, n_sectors))
    
    ax1_polar.bar(theta, industry_data.values, width=width, alpha=0.8, 
                  color=colors, edgecolor='black', linewidth=1)
    ax1_polar.set_title('彩虹南丁格尔玫瑰图', pad=20, fontweight='bold')
    
    # 2. 3D柱状图效果 (右上) 
    x_pos = np.arange(len(industry_data))
    bars2 = ax2.bar(x_pos, industry_data.values, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=2)
    
    # 添加3D视觉效果
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        # 添加顶部高亮
        ax2.add_patch(plt.Rectangle((bar.get_x(), height), bar.get_width(), height*0.05, 
                                   facecolor='white', alpha=0.7))
        # 添加侧面阴影
        ax2.add_patch(plt.Rectangle((bar.get_x()+bar.get_width()*0.05, 0), 
                                   bar.get_width()*0.05, height, 
                                   facecolor='gray', alpha=0.3))
    
    ax2.set_title('3D效果彩虹柱状图', fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(industry_data.index, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. 彩虹环形图 (左下)
    wedges, texts, autotexts = ax3.pie(industry_data.values, 
                                      labels=industry_data.index,
                                      colors=colors, startangle=90,
                                      wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                      autopct='%1.1f%%',
                                      pctdistance=0.85)
    ax3.set_title('彩虹环形图', fontweight='bold')
    
    # 美化文字
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    # 4. 彩虹雷达图 (右下)
    ax4_polar = plt.subplot(2, 2, 4, projection='polar')
    
    # 标准化数据到0-1范围
    normalized_values = industry_data.values / industry_data.values.max()
    
    # 绘制雷达图
    ax4_polar.plot(theta, normalized_values, 'o-', linewidth=3, markersize=8, 
                   color='darkblue', alpha=0.7)
    ax4_polar.fill(theta, normalized_values, alpha=0.3, 
                   color=plt.cm.rainbow(np.linspace(0, 1, 1))[0])
    
    # 设置标签
    ax4_polar.set_xticks(theta)
    ax4_polar.set_xticklabels([name[:6] for name in industry_data.index])
    ax4_polar.set_title('彩虹雷达图', pad=20, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def create_interactive_style_simulation():
    """模拟交互式样式的静态版本"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception:
        return
    
    # 创建多个颜色主题的对比
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('多主题彩虹风格对比 (模拟Vue主题切换)', fontsize=16, fontweight='bold')
    
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(6)
    
    # 不同的颜色主题
    color_themes = [
        ('rainbow', '彩虹主题'),
        ('viridis', '翠绿主题'), 
        ('plasma', '等离子主题'),
        ('cool', '冷色主题'),
        ('hot', '热色主题'),
        ('tab10', '经典主题')
    ]
    
    for idx, (cmap_name, theme_name) in enumerate(color_themes):
        ax = axes[idx//3, idx%3]
        ax_polar = plt.subplot(2, 3, idx+1, projection='polar')
        
        # 数据准备
        n_sectors = len(industry_data)
        theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)
        width = 2*np.pi / n_sectors
        
        # 根据主题生成颜色
        if cmap_name == 'tab10':
            colors = plt.cm.tab10(np.linspace(0, 1, n_sectors))
        else:
            colors = plt.cm.get_cmap(cmap_name)(np.linspace(0, 1, n_sectors))
        
        # 绘制玫瑰图
        ax_polar.bar(theta, industry_data.values, width=width, alpha=0.8, 
                    color=colors, edgecolor='white', linewidth=1)
        ax_polar.set_title(theme_name, pad=20, fontweight='bold')
        
        # 简化标签
        for i, industry in enumerate(industry_data.index):
            angle = theta[i]
            ax_polar.text(angle, industry_data.values[i] * 1.1, industry[:4], 
                         ha='center', va='center', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("🎨 Matplotlib重现final_rose.py效果")
    print("="*60)
    
    # 加载数据并进行基础分析
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        # 与final_rose.py相同的数据分析
        industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(10)
        total = sum(industry_data.values)
        
        print("\n" + "="*60)
        print("📊 TOP 10 行业裁员数据分析 (与final_rose.py一致)")
        print("="*60)
        
        for i, (industry, value) in enumerate(industry_data.items()):
            percentage = (value / total) * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"{i+1:2d}. {industry:15s} | {value:6d} | {percentage:5.1f}% | {bar}")
        
        print(f"\n📈 总计: {int(total):,} 人")
        print(f"📊 平均每行业: {int(total/len(industry_data)):,} 人")
        
        print("\n1️⃣ 创建与final_rose.py一致的彩虹玫瑰图")
        create_matplotlib_rainbow_rose()
        
        print("\n2️⃣ 创建增强版彩虹图表集合")
        create_enhanced_rainbow_charts()
        
        print("\n3️⃣ 创建多主题对比图表")
        create_interactive_style_simulation()
        
        print("\n🎨 Matplotlib版本特色:")
        print("="*40)
        print("✨ 完全重现了final_rose.py的视觉效果")
        print("✨ 提供了更多样的图表类型组合") 
        print("✨ 支持多种颜色主题切换")
        print("✨ 添加了3D效果和雷达图等扩展")
        print("✨ 保持了与Vue版本相同的数据分析输出")
        
        print("\n🎯 对比总结:")
        print("- Vue版本: 交互性强，适合Web展示")
        print("- Matplotlib版本: 静态精美，适合报告和分析")
        print("- 数据处理: 两者完全一致")
        print("- 视觉效果: 各有特色，都很专业")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
