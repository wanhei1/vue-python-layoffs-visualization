import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载数据文件"""
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        print("数据文件未找到，生成示例数据")
        # 生成示例数据
        np.random.seed(42)
        n_samples = 100
        
        locations = ['California', 'New York', 'Texas', 'Washington', 'Florida']
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail']
        states = ['Seed', 'Series A', 'Series B', 'Series C', 'Post-IPO']
        scales = ['0-100', '100-500', '500-1000', '1000-5000', '5000+']
        
        data = {
            'Location': np.random.choice(locations, n_samples),
            'Industry': np.random.choice(industries, n_samples),
            'State': np.random.choice(states, n_samples),
            'Scale': np.random.choice(scales, n_samples),
            'Num': np.random.randint(10, 1000, n_samples),
            'Before': np.random.randint(100, 5000, n_samples),
            'Year': np.random.choice([2020, 2021, 2022, 2023, 2024], n_samples),
            'Money': np.random.uniform(1, 500, n_samples),
            'lng': np.random.uniform(-125, -70, n_samples),
            'lat': np.random.uniform(25, 50, n_samples)
        }
        
        df = pd.DataFrame(data)
        df['After'] = df['Before'] - df['Num']
        return df

def demo_chart_implementations():
    """演示每种图表类型的实现"""
    df = load_data()
    
    print("="*60)
    print("Vue项目图表 vs Python实现对比")
    print("="*60)
    
    # 1. ChartBar.vue - 柱状图实现
    print("\n1. ChartBar.vue - 融资阶段与裁员关系")
    print("✅ Matplotlib: 完全可以实现")
    print("✅ Seaborn: 可以实现，样式更美观")
    print("❌ Mayavi: 不适合2D图表")
    
    plt.figure(figsize=(12, 4))
    
    # Matplotlib实现
    plt.subplot(1, 2, 1)
    state_data = df.groupby('State')['Num'].sum()
    bars = plt.bar(state_data.index, state_data.values, color='skyblue', alpha=0.7)
    plt.title('Matplotlib - 融资阶段裁员情况')
    plt.xticks(rotation=45)
    plt.ylabel('裁员人数')
    
    # Seaborn实现
    plt.subplot(1, 2, 2)
    sns.barplot(data=df, x='State', y='Num', estimator=sum, ci=None)
    plt.title('Seaborn - 融资阶段裁员情况')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # 2. ChartCircle.vue - 饼图实现
    print("\n2. ChartCircle.vue - 行业与裁员关系")
    print("✅ Matplotlib: 可以实现饼图")
    print("⚠️ Seaborn: 不直接支持饼图")
    print("❌ Mayavi: 不适合2D图表")
    
    plt.figure(figsize=(12, 4))
    
    industry_data = df.groupby('Industry')['Num'].sum()
    
    # Matplotlib饼图
    plt.subplot(1, 2, 1)
    plt.pie(industry_data.values, labels=industry_data.index, autopct='%1.1f%%', startangle=90)
    plt.title('Matplotlib - 行业分布饼图')
    
    # Matplotlib南丁格尔玫瑰图（优化版）
    ax = plt.subplot(1, 2, 2, projection='polar')
    
    # 计算角度和半径
    theta = np.linspace(0, 2*np.pi, len(industry_data), endpoint=False)
    radii = industry_data.values
    width = 2*np.pi / len(industry_data)
    
    # 创建渐变颜色
    colors = plt.cm.Set3(np.linspace(0, 1, len(industry_data)))
    
    # 绘制玫瑰图
    bars = ax.bar(theta, radii, width=width, alpha=0.8, 
                  color=colors, edgecolor='white', linewidth=2)
    
    # 设置标签
    ax.set_theta_zero_location('N')  # 设置0度位置在顶部
    ax.set_theta_direction(-1)  # 设置顺时针方向
    
    # 添加行业标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        # 标签位置稍微向外偏移
        label_radius = radii[i] + max(radii) * 0.1
        ax.text(angle, label_radius, industry, 
                ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # 在扇形中心添加数值
        value_radius = radii[i] / 2
        ax.text(angle, value_radius, str(int(value)), 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='white')
    
    ax.set_title('南丁格尔玫瑰图 - 行业分布', pad=20, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # 3. ChartLine.vue - 条形图实现
    print("\n3. ChartLine.vue - 公司规模与裁员关系")
    print("✅ Matplotlib: 完全可以实现")
    print("✅ Seaborn: 可以实现，样式更丰富")
    print("❌ Mayavi: 不适合")
    
    plt.figure(figsize=(12, 4))
    
    scale_data = df.groupby('Scale')['Num'].sum().sort_values()
    
    # Matplotlib实现
    plt.subplot(1, 2, 1)
    plt.barh(scale_data.index, scale_data.values, color='lightcoral', alpha=0.7)
    plt.title('Matplotlib - 公司规模裁员情况')
    plt.xlabel('裁员人数')
    
    # Seaborn实现
    plt.subplot(1, 2, 2)
    sns.barplot(data=df, y='Scale', x='Num', estimator=sum, ci=None, orient='h')
    plt.title('Seaborn - 公司规模裁员情况')
    
    plt.tight_layout()
    plt.show()
    
    # 4. ChartMap.vue - 地图/散点图实现
    print("\n4. ChartMap.vue - 地理位置可视化")
    print("⚠️ Matplotlib: 散点图可以，地图需要额外库")
    print("⚠️ Seaborn: 不直接支持地图")
    print("✅ Mayavi: 可以做3D地理可视化")
    
    plt.figure(figsize=(12, 4))
    
    # Matplotlib散点图
    plt.subplot(1, 2, 1)
    scatter = plt.scatter(df['lng'], df['lat'], s=df['Num']/10, c=df['Num'], 
                         cmap='viridis', alpha=0.6)
    plt.title('Matplotlib - 地理散点图')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.colorbar(scatter, label='裁员人数')
    
    # 地区汇总条形图（替代地图）
    plt.subplot(1, 2, 2)
    location_data = df.groupby('Location')['Num'].sum().sort_values(ascending=False)
    plt.bar(location_data.index, location_data.values, 
            color=plt.cm.viridis(np.linspace(0, 1, len(location_data))))
    plt.title('地区裁员汇总')
    plt.xticks(rotation=45)
    plt.ylabel('裁员人数')
    
    plt.tight_layout()
    plt.show()
    
    # 5. scatter.vue - 气泡图实现
    print("\n5. scatter.vue - 气泡散点图")
    print("✅ Matplotlib: 可以实现气泡图")
    print("✅ Seaborn: 可以实现")
    print("✅ Mayavi: 可以创建3D气泡效果")
    
    plt.figure(figsize=(12, 4))
    
    # Matplotlib气泡图
    plt.subplot(1, 2, 1)
    industry_sizes = df.groupby('Industry')['Num'].sum()
    
    # 生成随机位置
    np.random.seed(42)
    x_pos = np.random.uniform(0, 10, len(industry_sizes))
    y_pos = np.random.uniform(0, 10, len(industry_sizes))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(industry_sizes)))
    
    for i, (industry, size) in enumerate(industry_sizes.items()):
        plt.scatter(x_pos[i], y_pos[i], s=size, c=[colors[i]], alpha=0.7, 
                   label=industry)
    
    plt.title('Matplotlib - 行业气泡图')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 3D效果模拟
    ax = plt.subplot(1, 2, 2, projection='3d')
    x = df['lng']
    y = df['lat']
    z = df['Year']
    colors = df['Num']
    
    scatter = ax.scatter(x, y, z, c=colors, cmap='viridis', s=df['Num']/10, alpha=0.6)
    ax.set_title('3D时空分布')
    ax.set_xlabel('经度')
    ax.set_ylabel('纬度')
    ax.set_zlabel('年份')
    
    plt.tight_layout()
    plt.show()

def create_comparison_table():
    """创建对比表格"""
    print("\n" + "="*80)
    print("各Python库对Vue项目图表的支持情况对比")
    print("="*80)
    
    comparison_data = {
        'Vue组件': ['ChartBar.vue', 'ChartCircle.vue', 'ChartLine.vue', 'ChartMap.vue', 'scatter.vue'],
        '图表类型': ['双Y轴柱状图', '玫瑰图/饼图', '水平条形图', '地图+散点图', '气泡散点图'],
        'Matplotlib': ['✅ 完全支持', '✅ 支持饼图, ⚠️ 玫瑰图需自定义', '✅ 完全支持', '⚠️ 散点图支持, 地图需额外库', '✅ 完全支持'],
        'Seaborn': ['✅ 支持', '❌ 不直接支持饼图', '✅ 支持', '❌ 不支持地图', '✅ 支持'],
        'Mayavi': ['❌ 不适合', '❌ 不适合', '❌ 不适合', '✅ 3D地理可视化', '✅ 3D气泡图']
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    print(df_comparison.to_string(index=False))
    
    print("\n" + "="*80)
    print("推荐方案:")
    print("="*80)
    print("1. 优先使用: Matplotlib (最全面，可实现80%的图表)")
    print("2. 配合使用: Seaborn (统计图表，样式美观)")
    print("3. 特殊需求: Mayavi (3D可视化)")
    print("4. 地图可视化: 考虑使用 Folium 或 Plotly")

if __name__ == "__main__":
    demo_chart_implementations()
    create_comparison_table()
