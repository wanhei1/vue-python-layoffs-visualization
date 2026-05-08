import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
def load_data():
    """加载数据文件"""
    with open('e:/BIT_file/大三下学期/大数据可视化/vue-vis(1)/public/static/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# 数据分析和可视化
def analyze_and_visualize():
    """分析数据并生成可视化图表"""
    df = load_data()
    print("数据概览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"数据列名: {df.columns.tolist()}")
    
    # 设置图表样式
    plt.style.use('seaborn-v0_8')
    
    # 创建子图
    fig = plt.figure(figsize=(20, 15))
    
    # 1. 柱状图 - 融资阶段与裁员关系 (对应ChartBar.vue)
    ax1 = plt.subplot(2, 3, 1)
    state_data = df.groupby('State')['Num'].sum().sort_values(ascending=False)
    # 合并Series A-Z
    series_data = state_data[state_data.index.str.startswith('Series')].sum()
    state_data = state_data[~state_data.index.str.startswith('Series')]
    state_data['Series A-Z'] = series_data
    
    bars = ax1.bar(range(len(state_data)), state_data.values, color='skyblue', alpha=0.7)
    ax1.set_title('融资阶段与裁员关系', fontsize=14, fontweight='bold')
    ax1.set_xlabel('融资阶段')
    ax1.set_ylabel('裁员人数')
    ax1.set_xticks(range(len(state_data)))
    ax1.set_xticklabels(state_data.index, rotation=45, ha='right')
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    # 2. 饼图 - 行业与裁员关系 (对应ChartCircle.vue)
    ax2 = plt.subplot(2, 3, 2)
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False)
    colors = plt.cm.Set3(np.linspace(0, 1, len(industry_data)))
    
    wedges, texts, autotexts = ax2.pie(industry_data.values, labels=industry_data.index, 
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('行业与裁员关系', fontsize=14, fontweight='bold')
    
    # 3. 条形图 - 公司规模与裁员关系 (对应ChartLine.vue)
    ax3 = plt.subplot(2, 3, 3)
    scale_data = df.groupby('Scale')['Num'].sum().sort_values(ascending=True)
    bars = ax3.barh(range(len(scale_data)), scale_data.values, color='lightcoral', alpha=0.7)
    ax3.set_title('公司规模与裁员关系', fontsize=14, fontweight='bold')
    ax3.set_xlabel('裁员人数')
    ax3.set_ylabel('公司规模')
    ax3.set_yticks(range(len(scale_data)))
    ax3.set_yticklabels(scale_data.index)
    
    # 4. 散点图 - 地理位置散点图 (对应ChartMap.vue的散点部分)
    ax4 = plt.subplot(2, 3, 4)
    scatter = ax4.scatter(df['lng'], df['lat'], s=df['Num']/10, 
                         c=df['Num'], cmap='viridis', alpha=0.6)
    ax4.set_title('地理位置散点图', fontsize=14, fontweight='bold')
    ax4.set_xlabel('经度')
    ax4.set_ylabel('纬度')
    plt.colorbar(scatter, ax=ax4, label='裁员人数')
    
    # 5. 热力图 - 年份与地区的关系
    ax5 = plt.subplot(2, 3, 5)
    pivot_data = df.groupby(['Year', 'Location'])['Num'].sum().unstack(fill_value=0)
    sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax5)
    ax5.set_title('年份-地区热力图', fontsize=14, fontweight='bold')
    ax5.set_xlabel('地区')
    ax5.set_ylabel('年份')
    
    # 6. 时间序列图 - 年份趋势
    ax6 = plt.subplot(2, 3, 6)
    yearly_data = df.groupby('Year')['Num'].sum()
    ax6.plot(yearly_data.index, yearly_data.values, marker='o', linewidth=2, markersize=8)
    ax6.set_title('年度裁员趋势', fontsize=14, fontweight='bold')
    ax6.set_xlabel('年份')
    ax6.set_ylabel('裁员人数')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def create_seaborn_visualizations():
    """使用Seaborn创建更高级的可视化"""
    df = load_data()
    
    # 设置Seaborn样式
    sns.set_style("whitegrid")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 箱线图 - 不同行业的裁员分布
    sns.boxplot(data=df, x='Industry', y='Num', ax=axes[0,0])
    axes[0,0].set_title('不同行业裁员分布', fontsize=14, fontweight='bold')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. 小提琴图 - 不同规模公司的裁员分布
    sns.violinplot(data=df, x='Scale', y='Num', ax=axes[0,1])
    axes[0,1].set_title('不同规模公司裁员分布', fontsize=14, fontweight='bold')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # 3. 散点图矩阵 - 数值变量关系
    numeric_cols = ['Num', 'Before', 'After', 'Money', 'Year']
    df_numeric = df[numeric_cols].dropna()
    
    # 相关性热力图
    correlation_matrix = df_numeric.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                center=0, ax=axes[1,0])
    axes[1,0].set_title('变量相关性热力图', fontsize=14, fontweight='bold')
    
    # 4. 分面图 - 按年份分组的行业裁员情况
    yearly_industry = df.groupby(['Year', 'Industry'])['Num'].sum().reset_index()
    pivot_yearly = yearly_industry.pivot(index='Year', columns='Industry', values='Num').fillna(0)
    
    # 选择前5个行业
    top_industries = df.groupby('Industry')['Num'].sum().nlargest(5).index
    pivot_top = pivot_yearly[top_industries]
    
    for i, industry in enumerate(top_industries):
        if i < 5:
            axes[1,1].plot(pivot_top.index, pivot_top[industry], marker='o', label=industry)
    
    axes[1,1].set_title('主要行业年度裁员趋势', fontsize=14, fontweight='bold')
    axes[1,1].set_xlabel('年份')
    axes[1,1].set_ylabel('裁员人数')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def simulate_3d_visualization():
    """模拟3D可视化效果（类似Mayavi但使用matplotlib）"""
    df = load_data()
    
    # 创建3D散点图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 使用年份、经度、纬度作为三个维度
    x = df['lng']
    y = df['lat'] 
    z = df['Year']
    colors = df['Num']
    
    scatter = ax.scatter(x, y, z, c=colors, cmap='viridis', s=df['Num']/10, alpha=0.6)
    
    ax.set_xlabel('经度')
    ax.set_ylabel('纬度')
    ax.set_zlabel('年份')
    ax.set_title('三维时空分布图', fontsize=14, fontweight='bold')
    
    # 添加颜色条
    plt.colorbar(scatter, ax=ax, label='裁员人数', shrink=0.5)
    
    plt.show()

def create_interactive_style_plots():
    """创建交互式风格的图表"""
    df = load_data()
    
    # 1. 创建类似Vue项目中散点图的效果
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 模拟气泡图效果
    industry_sizes = df.groupby('Industry')['Num'].sum()
    colors = plt.cm.Set3(np.linspace(0, 1, len(industry_sizes)))
    
    # 随机生成位置（模拟Vue项目中的散点布局）
    np.random.seed(42)
    n_industries = len(industry_sizes)
    x_pos = np.random.uniform(0, 10, n_industries)
    y_pos = np.random.uniform(0, 10, n_industries)
    
    for i, (industry, size) in enumerate(industry_sizes.items()):
        circle = Circle((x_pos[i], y_pos[i]), radius=size/5000, 
                       color=colors[i], alpha=0.7)
        ax1.add_patch(circle)
        ax1.text(x_pos[i], y_pos[i], industry, ha='center', va='center', 
                fontsize=8, fontweight='bold')
    
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('行业分布气泡图', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # 2. 创建地区分布图
    location_data = df.groupby('Location')['Num'].sum().sort_values(ascending=False)
    
    # 创建条形图，模拟地图的效果
    bars = ax2.bar(range(len(location_data)), location_data.values, 
                   color=plt.cm.viridis(np.linspace(0, 1, len(location_data))))
    
    ax2.set_title('地区裁员分布', fontsize=14, fontweight='bold')
    ax2.set_xlabel('地区')
    ax2.set_ylabel('裁员人数')
    ax2.set_xticks(range(len(location_data)))
    ax2.set_xticklabels(location_data.index, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("="*50)
    print("Vue项目图表分析 - Python可视化实现")
    print("="*50)
    
    # 基础可视化
    print("\n1. 基础可视化图表（对应Vue项目中的图表）")
    analyze_and_visualize()
    
    # Seaborn高级可视化
    print("\n2. Seaborn高级可视化")
    create_seaborn_visualizations()
    
    # 3D可视化
    print("\n3. 3D可视化效果")
    simulate_3d_visualization()
    
    # 交互式风格图表
    print("\n4. 交互式风格图表")
    create_interactive_style_plots()
