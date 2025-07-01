<template>
<div class="page-container">
    <!-- 时间筛选器 -->
    <div class="time-filter">
        <u-tabs v-model="timeTab" :list="timeTabs" @change="switchTime" />
        <div v-if="timeTab === 3" class="custom-range">
            <u-datetime-picker v-model="startDate" mode="date">
                <u-input :value="startDate" placeholder="开始日期" readonly size="small" />
            </u-datetime-picker>
            <span>至</span>
            <u-datetime-picker v-model="endDate" mode="date">
                <u-input :value="endDate" placeholder="结束日期" readonly size="small" />
            </u-datetime-picker>
            <u-button size="small" type="primary" @click="applyCustomRange">应用</u-button>
        </div>
    </div>

    <!-- 核心统计 -->
    <div class="core-stats">
        <div v-for="(stat, key) in coreStats" :key="key" class="stat-card" :class="key">
            <div class="stat-icon">
                <u-icon :name="stat.icon" :color="stat.color" size="32" />
            </div>
            <div class="stat-content">
                <div class="stat-number">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-change" :class="stat.change >= 0 ? 'positive' : 'negative'">
                    {{ stat.change >= 0 ? '+' : '' }}{{ stat.change }}%
                </div>
            </div>
        </div>
    </div>

    <!-- 趋势图表 -->
    <div class="chart-section">
        <div class="chart-card">
            <div class="chart-header">
                <div class="chart-title">
                    <u-icon name="bar-chart-fill" color="#667eea" />
                    预约趋势分析
                </div>
                <u-button size="mini" @click="exportTrendData">导出</u-button>
            </div>
            <div class="chart-content">
                <div class="trend-chart">
                    <div class="chart-bars">
                        <div v-for="item in trendData" :key="item.date" class="bar-group">
                            <div class="bar-container">
                                <div class="bar booking" :style="{ height: getBarHeight(item.bookings) + 'px' }"></div>
                                <div class="bar boarding" :style="{ height: getBarHeight(item.boardings) + 'px' }">
                                </div>
                            </div>
                            <div class="bar-label">{{ item.date }}</div>
                        </div>
                    </div>
                    <div class="chart-legend">
                        <div class="legend-item">
                            <div class="legend-color booking"></div>
                            <span>预约人数</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color boarding"></div>
                            <span>上车人数</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 用户分布 -->
        <div class="distribution-card">
            <div class="chart-header">
                <div class="chart-title">
                    <u-icon name="pie-chart-fill" color="#67c23a" />
                    用户分布
                </div>
            </div>
            <div class="distribution-list">
                <div v-for="role in roleDistribution" :key="role.name" class="distribution-item">
                    <div class="role-info">
                        <div class="role-color" :style="{ backgroundColor: role.color }"></div>
                        <span class="role-name">{{ role.name }}</span>
                    </div>
                    <div class="role-stats">
                        <span class="role-count">{{ role.count }}</span>
                        <span class="role-percentage">{{ role.percentage }}%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 数据表格 -->
    <div class="data-table-section">
        <div class="table-header">
            <div class="table-title">
                <u-icon name="list-fill" color="#e6a23c" />
                班次统计详情
            </div>
            <div class="table-actions">
                <u-button size="small" type="info" @click="refreshData">
                    <u-icon name="reload" />刷新
                </u-button>
                <u-button size="small" type="primary" @click="exportTableData">
                    <u-icon name="download" />导出
                </u-button>
            </div>
        </div>

        <div class="table-filters">
            <u-input v-model="tableFilter.busNumber" placeholder="车牌号" size="small" />
            <u-input v-model="tableFilter.route" placeholder="线路" size="small" />
            <u-picker :columns="[statusOptions]" @confirm="selectStatus">
                <u-input v-model="tableFilter.status" placeholder="状态" readonly size="small" />
            </u-picker>
            <u-button size="small" @click="applyFilter">筛选</u-button>
        </div>

        <div class="data-table">
            <div class="table-row header">
                <div class="table-cell">班车</div>
                <div class="table-cell">时间</div>
                <div class="table-cell">预约</div>
                <div class="table-cell">上车</div>
                <div class="table-cell">利用率</div>
                <div class="table-cell">状态</div>
            </div>
            <div v-for="row in filteredTableData" :key="row.id" class="table-row">
                <div class="table-cell">{{ row.busNumber }}</div>
                <div class="table-cell">{{ row.tripTime }}</div>
                <div class="table-cell">{{ row.bookings }}</div>
                <div class="table-cell">{{ row.boardings }}</div>
                <div class="table-cell">
                    <div class="utilization-bar">
                        <div class="utilization-fill" :style="{ width: row.utilization + '%' }"></div>
                        <span>{{ row.utilization }}%</span>
                    </div>
                </div>
                <div class="table-cell">
                    <u-tag :text="getStatusText(row.status)" :type="getStatusType(row.status)" size="mini" />
                </div>
            </div>
        </div>
    </div>

    <!-- 运营报告 -->
    <div class="report-section">
        <div class="report-header">
            <div class="report-title">
                <u-icon name="document-fill" color="#f56c6c" />
                运营分析报告
            </div>
            <div class="report-actions">
                <u-button size="small" type="primary" @click="generateReport">生成报告</u-button>
                <u-button size="small" type="success" @click="scheduleReport">定期报告</u-button>
            </div>
        </div>

        <div class="report-content">
            <div class="report-summary">
                <div class="summary-item">
                    <span class="summary-label">数据时间</span>
                    <span class="summary-value">{{ reportPeriod }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">总班次</span>
                    <span class="summary-value">{{ reportData.totalTrips }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">服务人数</span>
                    <span class="summary-value">{{ reportData.totalPassengers }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">平均利用率</span>
                    <span class="summary-value">{{ reportData.avgUtilization }}%</span>
                </div>
            </div>

            <div class="insights">
                <div v-for="insight in insights" :key="insight.id" class="insight-item">
                    <div class="insight-icon" :class="insight.type">
                        <u-icon :name="insight.icon" />
                    </div>
                    <span class="insight-text">{{ insight.text }}</span>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 响应式数据
const timeTab = ref(0);
const startDate = ref('');
const endDate = ref('');

// 时间标签
const timeTabs = ref([
    { name: '今日' }, { name: '本周' }, { name: '本月' }, { name: '自定义' }
]);

// 核心统计
const coreStats = ref({
    bookings: { value: 1256, label: '总预约人数', icon: 'calendar-fill', color: '#667eea', change: 12.5 },
    boardings: { value: 1089, label: '实际上车', icon: 'checkmark-circle-fill', color: '#67c23a', change: 8.3 },
    cancelRate: { value: '13.3%', label: '取消率', icon: 'close-circle-fill', color: '#e6a23c', change: -3.2 },
    utilization: { value: '86.7%', label: '座位利用率', icon: 'account-fill', color: '#409eff', change: 5.4 }
});

// 趋势数据
const trendData = ref([
    { date: '7-25', bookings: 145, boardings: 128 },
    { date: '7-26', bookings: 156, boardings: 142 },
    { date: '7-27', bookings: 138, boardings: 125 },
    { date: '7-28', bookings: 167, boardings: 155 },
    { date: '7-29', bookings: 189, boardings: 172 },
    { date: '7-30', bookings: 178, boardings: 161 },
    { date: '7-01', bookings: 198, boardings: 185 }
]);

// 用户分布
const roleDistribution = ref([
    { name: '学生', count: 1089, percentage: 68.5, color: '#409eff' },
    { name: '教师', count: 356, percentage: 22.4, color: '#67c23a' },
    { name: '管理员', count: 45, percentage: 2.8, color: '#e6a23c' },
    { name: '其他', count: 100, percentage: 6.3, color: '#909399' }
]);

// 表格筛选
const tableFilter = ref({ busNumber: '', route: '', status: '' });
const statusOptions = ref(['全部', '运营中', '维护中', '停运']);

// 表格数据
const tableData = ref([
    { id: 1, busNumber: 'AYB30260', tripTime: '07:00', bookings: 42, boardings: 38, utilization: 84, status: 'active' },
    { id: 2, busNumber: 'AYB30260', tripTime: '07:30', bookings: 45, boardings: 43, utilization: 96, status: 'active' },
    { id: 3, busNumber: 'ALB328', tripTime: '08:00', bookings: 38, boardings: 35, utilization: 88, status: 'active' },
    { id: 4, busNumber: 'BXC156', tripTime: '09:00', bookings: 28, boardings: 25, utilization: 71, status: 'maintenance' }
]);

// 报告数据
const reportData = ref({
    totalTrips: 168, totalPassengers: 3245, avgUtilization: 82.3
});

// 洞察数据
const insights = ref([
    { id: 1, type: 'positive', icon: 'arrow-up', text: '预约人数较上期增长12%，用户活跃度提升' },
    { id: 2, type: 'positive', icon: 'arrow-down', text: '取消率较上期下降3%，服务满意度改善' },
    { id: 3, type: 'neutral', icon: 'info-circle', text: '早班车利用率最高，建议优化晚班车时刻表' }
]);

// 计算属性
const maxValue = computed(() => Math.max(...trendData.value.map(item => Math.max(item.bookings, item.boardings))));

const filteredTableData = computed(() => {
    let filtered = tableData.value;

    if (tableFilter.value.busNumber) {
        filtered = filtered.filter(row => row.busNumber.includes(tableFilter.value.busNumber));
    }

    if (tableFilter.value.route) {
        filtered = filtered.filter(row => row.busNumber.includes(tableFilter.value.route));
    }

    if (tableFilter.value.status && tableFilter.value.status !== '全部') {
        const statusMap = { '运营中': 'active', '维护中': 'maintenance', '停运': 'inactive' };
        filtered = filtered.filter(row => row.status === statusMap[tableFilter.value.status]);
    }

    return filtered;
});

const reportPeriod = computed(() => {
    if (timeTab.value === 3 && startDate.value && endDate.value) {
        return `${startDate.value} 至 ${endDate.value}`;
    }
    return ['今日', '本周', '本月', '自定义'][timeTab.value];
});

// 方法
const getBarHeight = (value: number) => (value / maxValue.value) * 150;

const getStatusText = (status: string) => {
    const map = { active: '运营中', maintenance: '维护中', inactive: '停运' };
    return map[status] || status;
};

const getStatusType = (status: string) => {
    const map = { active: 'success', maintenance: 'warning', inactive: 'error' };
    return map[status] || 'default';
};

const switchTime = () => {
    uni.showToast({ title: '数据更新中...', icon: 'loading' });
    setTimeout(() => {
        uni.showToast({ title: '更新完成', icon: 'success' });
    }, 1000);
};

const applyCustomRange = () => {
    if (!startDate.value || !endDate.value) {
        uni.showToast({ title: '请选择完整时间范围', icon: 'error' });
        return;
    }
    switchTime();
};

const selectStatus = (value: any) => {
    tableFilter.value.status = value.value[0];
};

const applyFilter = () => {
    uni.showToast({ title: '筛选完成', icon: 'success' });
};

const refreshData = () => {
    uni.showToast({ title: '数据刷新完成', icon: 'success' });
};

const exportTrendData = () => {
    uni.showToast({ title: '趋势数据导出成功', icon: 'success' });
};

const exportTableData = () => {
    uni.showToast({ title: '详细数据导出成功', icon: 'success' });
};

const generateReport = () => {
    uni.showToast({ title: '报告生成中...', icon: 'loading' });
    setTimeout(() => {
        uni.showToast({ title: '报告生成完成', icon: 'success' });
    }, 2000);
};

const scheduleReport = () => {
    uni.showActionSheet({
        itemList: ['每日报告', '每周报告', '每月报告'],
        success: (res) => {
            const types = ['每日', '每周', '每月'];
            uni.showToast({ title: `${types[res.tapIndex]}报告已设置`, icon: 'success' });
        }
    });
};
</script>

<style lang="scss" scoped>
.page-container {
    padding: 20rpx;
    background: #f5f6fa;
    min-height: 100vh;
}

.time-filter {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .custom-range {
        display: flex;
        align-items: center;
        gap: 20rpx;
        margin-top: 20rpx;
    }
}

.core-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20rpx;
    margin-bottom: 30rpx;
}

.stat-card {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx;
    display: flex;
    align-items: center;
    gap: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .stat-content {
        .stat-number {
            font-size: 36rpx;
            font-weight: 700;
            color: #303133;
            margin-bottom: 8rpx;
        }

        .stat-label {
            font-size: 24rpx;
            color: #909399;
            margin-bottom: 8rpx;
        }

        .stat-change {
            font-size: 22rpx;
            font-weight: 600;

            &.positive {
                color: #67c23a;
            }

            &.negative {
                color: #f56c6c;
            }
        }
    }
}

.chart-section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30rpx;
    margin-bottom: 30rpx;
}

.chart-card,
.distribution-card {
    background: white;
    border-radius: 16rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30rpx;
        border-bottom: 1rpx solid #f5f6fa;

        .chart-title {
            display: flex;
            align-items: center;
            gap: 15rpx;
            font-size: 28rpx;
            font-weight: 600;
            color: #303133;
        }
    }
}

.trend-chart {
    padding: 30rpx;

    .chart-bars {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        height: 200rpx;
        margin-bottom: 30rpx;

        .bar-group {
            display: flex;
            flex-direction: column;
            align-items: center;

            .bar-container {
                display: flex;
                gap: 3rpx;
                align-items: flex-end;
                height: 150rpx;
                margin-bottom: 10rpx;

                .bar {
                    width: 12rpx;
                    border-radius: 6rpx 6rpx 0 0;

                    &.booking {
                        background: #667eea;
                    }

                    &.boarding {
                        background: #67c23a;
                    }
                }
            }

            .bar-label {
                font-size: 20rpx;
                color: #909399;
            }
        }
    }

    .chart-legend {
        display: flex;
        justify-content: center;
        gap: 30rpx;

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8rpx;
            font-size: 24rpx;

            .legend-color {
                width: 16rpx;
                height: 16rpx;
                border-radius: 2rpx;

                &.booking {
                    background: #667eea;
                }

                &.boarding {
                    background: #67c23a;
                }
            }
        }
    }
}

.distribution-list {
    padding: 30rpx;

    .distribution-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20rpx 0;
        border-bottom: 1rpx solid #f5f6fa;

        &:last-child {
            border-bottom: none;
        }

        .role-info {
            display: flex;
            align-items: center;
            gap: 15rpx;

            .role-color {
                width: 20rpx;
                height: 20rpx;
                border-radius: 4rpx;
            }

            .role-name {
                font-size: 26rpx;
                color: #303133;
            }
        }

        .role-stats {
            display: flex;
            flex-direction: column;
            align-items: flex-end;

            .role-count {
                font-size: 24rpx;
                color: #606266;
            }

            .role-percentage {
                font-size: 28rpx;
                font-weight: 600;
                color: #667eea;
            }
        }
    }
}

.data-table-section {
    background: white;
    border-radius: 16rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30rpx;
        border-bottom: 1rpx solid #f5f6fa;

        .table-title {
            display: flex;
            align-items: center;
            gap: 15rpx;
            font-size: 28rpx;
            font-weight: 600;
            color: #303133;
        }

        .table-actions {
            display: flex;
            gap: 15rpx;
        }
    }

    .table-filters {
        display: flex;
        gap: 20rpx;
        padding: 30rpx;
        align-items: center;
    }

    .data-table {
        .table-row {
            display: flex;

            &.header {
                background: #f8f9ff;
                font-weight: 600;
            }

            &:not(.header) {
                border-bottom: 1rpx solid #f5f6fa;
            }

            .table-cell {
                flex: 1;
                padding: 20rpx 15rpx;
                font-size: 24rpx;
                display: flex;
                align-items: center;

                .utilization-bar {
                    width: 100%;
                    height: 20rpx;
                    background: #f5f6fa;
                    border-radius: 10rpx;
                    position: relative;
                    overflow: hidden;

                    .utilization-fill {
                        height: 100%;
                        background: linear-gradient(90deg, #67c23a, #409eff);
                        border-radius: 10rpx;
                    }

                    span {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        font-size: 18rpx;
                        color: #303133;
                        font-weight: 600;
                    }
                }
            }
        }
    }
}

.report-section {
    background: white;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .report-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30rpx;
        border-bottom: 1rpx solid #f5f6fa;

        .report-title {
            display: flex;
            align-items: center;
            gap: 15rpx;
            font-size: 28rpx;
            font-weight: 600;
            color: #303133;
        }

        .report-actions {
            display: flex;
            gap: 15rpx;
        }
    }

    .report-content {
        padding: 30rpx;

        .report-summary {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30rpx;
            margin-bottom: 40rpx;

            .summary-item {
                text-align: center;

                .summary-label {
                    font-size: 24rpx;
                    color: #909399;
                    margin-bottom: 8rpx;
                    display: block;
                }

                .summary-value {
                    font-size: 32rpx;
                    font-weight: 600;
                    color: #303133;
                }
            }
        }

        .insights {
            .insight-item {
                display: flex;
                align-items: center;
                gap: 20rpx;
                padding: 20rpx 0;
                border-bottom: 1rpx solid #f5f6fa;

                &:last-child {
                    border-bottom: none;
                }

                .insight-icon {
                    width: 40rpx;
                    height: 40rpx;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;

                    &.positive {
                        background: #f0f9ff;
                        color: #67c23a;
                    }

                    &.neutral {
                        background: #f8f9ff;
                        color: #909399;
                    }
                }

                .insight-text {
                    font-size: 26rpx;
                    color: #606266;
                    line-height: 1.5;
                }
            }
        }
    }
}
</style>