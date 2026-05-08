import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8')

def load_data():
    """加载数据"""
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return None

def create_bar_chart(df):
    """创建柱状图 - 融资阶段与裁员关系 (对应ChartBar.vue)"""
    
    # 数据处理
    stage_data = df.groupby('State').agg({
        'Num': ['sum', 'count'],
        'Before': 'sum'
    }).round(2)
    
    stage_data.columns = ['total_layoffs', 'companies', 'total_before']
    stage_data['percentage'] = (stage_data['total_layoffs'] / stage_data['total_before'] * 100).round(2)
    stage_data = stage_data.sort_values('total_layoffs', ascending=False).head(7)
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('融资阶段与裁员关系分析', fontsize=16, fontweight='bold')
    
    # 左侧：裁员人数柱状图
    bars1 = ax1.bar(range(len(stage_data)), stage_data['total_layoffs'], 
                    color='#5470C6', alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_title('各融资阶段裁员总数', fontsize=14, fontweight='bold')
    ax1.set_xlabel('融资阶段', fontsize=12)
    ax1.set_ylabel('裁员人数', fontsize=12)
    ax1.set_xticks(range(len(stage_data)))
    ax1.set_xticklabels(stage_data.index, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    # 右侧：裁员百分比折线图
    ax2_twin = ax2.twinx()
    
    # 柱状图：公司数量
    bars2 = ax2.bar(range(len(stage_data)), stage_data['companies'], 
                    color='#91CC75', alpha=0.7, label='公司数量')
    
    # 折线图：裁员百分比
    line = ax2_twin.plot(range(len(stage_data)), stage_data['percentage'], 
                        color='#EE6666', marker='o', linewidth=3, 
                        markersize=8, label='裁员百分比')
    
    ax2.set_title('公司数量 vs 裁员百分比', fontsize=14, fontweight='bold')
    ax2.set_xlabel('融资阶段', fontsize=12)
    ax2.set_ylabel('公司数量', fontsize=12, color='#91CC75')
    ax2_twin.set_ylabel('裁员百分比 (%)', fontsize=12, color='#EE6666')
    
    ax2.set_xticks(range(len(stage_data)))
    ax2.set_xticklabels(stage_data.index, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 图例
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    plt.show()
    
    return stage_data

def create_industry_pie_chart(df):
    """创建饼图/玫瑰图 - 行业与裁员关系 (对应ChartCircle.vue)"""
    
    # 数据处理
    industry_data = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(10)
    
    # 创建子图
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('行业裁员数据可视化', fontsize=16, fontweight='bold')
    
    # 1. 传统饼图
    colors1 = plt.cm.Set3(np.linspace(0, 1, len(industry_data)))
    wedges, texts, autotexts = ax1.pie(industry_data.values, labels=industry_data.index, 
                                      autopct='%1.1f%%', colors=colors1, startangle=90)
    ax1.set_title('传统饼图 - 行业裁员占比', fontweight='bold')
    
    # 2. 南丁格尔玫瑰图 (极坐标柱状图)
    ax2 = plt.subplot(2, 2, 2, projection='polar')
    theta = np.linspace(0, 2*np.pi, len(industry_data), endpoint=False)
    width = 2*np.pi / len(industry_data)
    colors2 = plt.cm.rainbow(np.linspace(0, 1, len(industry_data)))
    
    bars = ax2.bar(theta, industry_data.values, width=width, alpha=0.8, 
                  color=colors2, edgecolor='black', linewidth=1)
    ax2.set_title('南丁格尔玫瑰图 - 行业分布', pad=20, fontweight='bold')
    
    # 添加标签
    for i, (industry, value) in enumerate(industry_data.items()):
        angle = theta[i]
        ax2.text(angle, value * 1.1, industry[:6], ha='center', va='center', 
                fontsize=9, fontweight='bold', 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # 3. 环形图
    wedges2, texts2, autotexts2 = ax3.pie(industry_data.values, labels=industry_data.index,
                                         autopct='%1.1f%%', colors=colors1, startangle=90,
                                         wedgeprops=dict(width=0.5))
    ax3.set_title('环形图 - 行业分布', fontweight='bold')
    
    # 4. 水平柱状图
    bars4 = ax4.barh(range(len(industry_data)), industry_data.values, 
                    color=colors2, alpha=0.8, edgecolor='white', linewidth=2)
    ax4.set_title('水平柱状图 - 行业裁员数', fontweight='bold')
    ax4.set_xlabel('裁员人数')
    ax4.set_yticks(range(len(industry_data)))
    ax4.set_yticklabels(industry_data.index)
    ax4.grid(True, alpha=0.3, axis='x')
    
    # 添加数值标签
    for i, bar in enumerate(bars4):
        width = bar.get_width()
        ax4.text(width + max(industry_data.values)*0.01, bar.get_y() + bar.get_height()/2,
                f'{int(width):,}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return industry_data

def create_scatter_chart(df):
    """创建散点图 - 公司规模与裁员关系 (对应ChartLine.vue)"""
    
    # 数据处理
    scale_data = df.groupby('Scale').agg({
        'Num': ['sum', 'mean', 'count'],
        'Before': 'mean',
        'After': 'mean',
        'Money': 'mean'
    }).round(2)
    
    scale_data.columns = ['total_layoffs', 'mean_layoffs', 'companies', 'mean_before', 'mean_after', 'mean_money']
    scale_data['layoff_percentage'] = ((scale_data['mean_before'] - scale_data['mean_after']) / scale_data['mean_before'] * 100).round(2)
    scale_data = scale_data.sort_values('mean_before')
    
    # 创建图表
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('公司规模与裁员关系分析', fontsize=16, fontweight='bold')
    
    # 1. 散点图 - 公司规模 vs 平均裁员人数
    scatter1 = ax1.scatter(scale_data['mean_before'], scale_data['mean_layoffs'], 
                          s=scale_data['companies']*10, 
                          c=scale_data['mean_money'], cmap='viridis', 
                          alpha=0.7, edgecolors='black', linewidth=1)
    ax1.set_xlabel('平均公司规模 (裁员前)')
    ax1.set_ylabel('平均裁员人数')
    ax1.set_title('公司规模 vs 平均裁员人数\n(气泡大小=公司数量, 颜色=平均融资额)')
    ax1.grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('平均融资额 (百万美元)')
    
    # 2. 柱状图 - 各规模区间公司数量
    bars2 = ax2.bar(range(len(scale_data)), scale_data['companies'], 
                    color=plt.cm.plasma(np.linspace(0, 1, len(scale_data))), 
                    alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('各规模区间公司数量分布')
    ax2.set_xlabel('公司规模区间')
    ax2.set_ylabel('公司数量')
    ax2.set_xticks(range(len(scale_data)))
    ax2.set_xticklabels(scale_data.index, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. 散点图 - 裁员百分比 vs 融资额
    scatter3 = ax3.scatter(scale_data['layoff_percentage'], scale_data['mean_money'],
                          s=scale_data['companies']*15,
                          c=scale_data['mean_before'], cmap='coolwarm',
                          alpha=0.7, edgecolors='black', linewidth=1)
    ax3.set_xlabel('裁员百分比 (%)')
    ax3.set_ylabel('平均融资额 (百万美元)')
    ax3.set_title('裁员百分比 vs 融资额\n(气泡大小=公司数量, 颜色=公司规模)')
    ax3.grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar3 = plt.colorbar(scatter3, ax=ax3)
    cbar3.set_label('平均公司规模')
    
    # 4. 箱线图 - 各规模区间裁员分布
    layoff_by_scale = [df[df['Scale'] == scale]['Num'].values for scale in scale_data.index]
    bp = ax4.boxplot(layoff_by_scale, labels=scale_data.index, patch_artist=True)
    
    # 设置箱线图颜色
    colors = plt.cm.Set2(np.linspace(0, 1, len(bp['boxes'])))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax4.set_title('各规模区间裁员人数分布 (箱线图)')
    ax4.set_xlabel('公司规模区间')
    ax4.set_ylabel('裁员人数')
    ax4.set_xticklabels(scale_data.index, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    return scale_data

def create_map_visualization(df):
    """创建地理分布可视化 (对应ChartMap.vue)"""
    
    # 数据处理
    location_data = df.groupby('Location').agg({
        'Num': ['sum', 'count'],
        'lat': 'first',
        'lng': 'first'
    }).round(2)
    
    location_data.columns = ['total_layoffs', 'companies', 'lat', 'lng']
    location_data = location_data.sort_values('total_layoffs', ascending=False).head(15)
    
    # 创建图表
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('地理分布分析', fontsize=16, fontweight='bold')
    
    # 1. 地理散点图 (模拟地图)
    scatter1 = ax1.scatter(location_data['lng'], location_data['lat'], 
                          s=location_data['total_layoffs']/100, 
                          c=location_data['total_layoffs'], 
                          cmap='Reds', alpha=0.7, edgecolors='black', linewidth=1)
    ax1.set_xlabel('经度')
    ax1.set_ylabel('纬度')
    ax1.set_title('地理分布散点图\n(大小和颜色表示裁员规模)')
    ax1.grid(True, alpha=0.3)
    
    # 添加地点标签
    for idx, row in location_data.iterrows():
        ax1.annotate(idx[:8], (row['lng'], row['lat']), 
                    xytext=(5, 5), textcoords='offset points', 
                    fontsize=8, alpha=0.8)
    
    # 颜色条
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('裁员总数')
    
    # 2. 垂直柱状图 - Top 10 地区
    top_10 = location_data.head(10)
    bars2 = ax2.bar(range(len(top_10)), top_10['total_layoffs'], 
                    color=plt.cm.viridis(np.linspace(0, 1, len(top_10))), 
                    alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('Top 10 地区裁员总数')
    ax2.set_xlabel('地区')
    ax2.set_ylabel('裁员总数')
    ax2.set_xticks(range(len(top_10)))
    ax2.set_xticklabels(top_10.index, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. 气泡图 - 公司数量 vs 平均裁员
    location_data['avg_layoffs'] = location_data['total_layoffs'] / location_data['companies']
    
    scatter3 = ax3.scatter(location_data['companies'], location_data['avg_layoffs'],
                          s=location_data['total_layoffs']/50,
                          c=range(len(location_data)), cmap='tab20',
                          alpha=0.7, edgecolors='black', linewidth=1)
    ax3.set_xlabel('公司数量')
    ax3.set_ylabel('平均每公司裁员数')
    ax3.set_title('公司数量 vs 平均裁员数\n(气泡大小=总裁员数)')
    ax3.grid(True, alpha=0.3)
    
    # 4. 饼图 - 地区占比
    wedges4, texts4, autotexts4 = ax4.pie(top_10['total_layoffs'], labels=top_10.index,
                                         autopct='%1.1f%%', startangle=90,
                                         colors=plt.cm.Set3(np.linspace(0, 1, len(top_10))))
    ax4.set_title('Top 10 地区裁员占比')
    
    plt.tight_layout()
    plt.show()
    
    return location_data

def create_comprehensive_dashboard(df):
    """创建综合仪表板"""
    
    # 创建一个大的综合图表
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
    
    fig.suptitle('科技公司裁员数据综合分析仪表板', fontsize=20, fontweight='bold')
    
    # 1. 时间趋势 (左上)
    ax1 = fig.add_subplot(gs[0, :2])
    df['Time'] = pd.to_datetime(df['Time'])
    time_data = df.groupby(df['Time'].dt.date)['Num'].sum().sort_index()
    ax1.plot(time_data.index, time_data.values, marker='o', linewidth=2, markersize=4)
    ax1.set_title('裁员时间趋势', fontweight='bold')
    ax1.set_xlabel('日期')
    ax1.set_ylabel('裁员人数')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. 行业Top 8 (右上)
    ax2 = fig.add_subplot(gs[0, 2:])
    industry_top8 = df.groupby('Industry')['Num'].sum().sort_values(ascending=False).head(8)
    bars2 = ax2.barh(range(len(industry_top8)), industry_top8.values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(industry_top8))))
    ax2.set_title('Top 8 行业裁员数', fontweight='bold')
    ax2.set_xlabel('裁员人数')
    ax2.set_yticks(range(len(industry_top8)))
    ax2.set_yticklabels(industry_top8.index)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. 融资阶段分布 (中左)
    ax3 = fig.add_subplot(gs[1, :2])
    stage_counts = df['State'].value_counts()
    wedges3, texts3, autotexts3 = ax3.pie(stage_counts.values, labels=stage_counts.index,
                                         autopct='%1.1f%%', startangle=90)
    ax3.set_title('融资阶段分布', fontweight='bold')
    
    # 4. 地理分布 Top 10 (中右)
    ax4 = fig.add_subplot(gs[1, 2:])
    location_top10 = df.groupby('Location')['Num'].sum().sort_values(ascending=False).head(10)
    bars4 = ax4.bar(range(len(location_top10)), location_top10.values,
                   color=plt.cm.plasma(np.linspace(0, 1, len(location_top10))))
    ax4.set_title('Top 10 地区裁员数', fontweight='bold')
    ax4.set_xlabel('地区')
    ax4.set_ylabel('裁员人数')
    ax4.set_xticks(range(len(location_top10)))
    ax4.set_xticklabels(location_top10.index, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. 公司规模vs裁员关系 (下方)
    ax5 = fig.add_subplot(gs[2, :])
    scale_data = df.groupby('Scale').agg({'Num': 'sum', 'Before': 'mean'}).round(0)
    
    # 双轴图
    ax5_twin = ax5.twinx()
    bars5 = ax5.bar(range(len(scale_data)), scale_data['Num'], 
                   alpha=0.7, color='lightblue', label='总裁员数')
    line5 = ax5_twin.plot(range(len(scale_data)), scale_data['Before'], 
                         'ro-', linewidth=2, markersize=6, label='平均公司规模')
    
    ax5.set_title('公司规模 vs 裁员数量关系', fontweight='bold')
    ax5.set_xlabel('公司规模区间')
    ax5.set_ylabel('裁员总数', color='blue')
    ax5_twin.set_ylabel('平均公司规模', color='red')
    ax5.set_xticks(range(len(scale_data)))
    ax5.set_xticklabels(scale_data.index, rotation=45, ha='right')
    ax5.grid(True, alpha=0.3)
    
    # 图例
    lines1, labels1 = ax5.get_legend_handles_labels()
    lines2, labels2 = ax5_twin.get_legend_handles_labels()
    ax5.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.show()

def main():
    """主函数"""
    print("🎨 使用Matplotlib重现Vue项目图表")
    print("="*60)
    
    # 加载数据
    df = load_data()
    if df is None:
        return
    
    print(f"✅ 数据加载成功: {len(df)} 条记录")
    print(f"📊 字段: {list(df.columns)}")
    
    # 基础统计
    total_layoffs = df['Num'].sum()
    total_companies = len(df)
    avg_layoffs = df['Num'].mean()
    
    print("\n📈 数据概览:")
    print(f"   总裁员人数: {total_layoffs:,}")
    print(f"   涉及公司数: {total_companies:,}")
    print(f"   平均裁员数: {avg_layoffs:.1f}")
    
    # 创建各种图表
    print("\n🎯 开始创建图表...")
    
    print("1️⃣ 创建柱状图 - 融资阶段分析")
    stage_data = create_bar_chart(df)
    
    print("2️⃣ 创建饼图/玫瑰图 - 行业分析") 
    industry_data = create_industry_pie_chart(df)
    
    print("3️⃣ 创建散点图 - 公司规模分析")
    scale_data = create_scatter_chart(df)
    
    print("4️⃣ 创建地理分布图")
    location_data = create_map_visualization(df)
    
    print("5️⃣ 创建综合仪表板")
    create_comprehensive_dashboard(df)
    
    print("\n🎉 所有图表创建完成!")
    print("💡 Matplotlib版本成功重现了Vue项目的所有核心图表功能")

if __name__ == "__main__":
    main()
