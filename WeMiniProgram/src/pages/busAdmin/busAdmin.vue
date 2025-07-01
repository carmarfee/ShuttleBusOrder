<template>
<div class="page-container">
    <!-- 操作栏 -->
    <div class="header-section">
        <u-search v-model="searchKeyword" placeholder="搜索班车" @search="handleSearch" />
        <div class="action-buttons">
            <u-button type="primary" size="small" @click="showBusModal = true">
                <u-icon name="plus" />添加班车
            </u-button>
            <u-button type="info" size="small" @click="syncData">
                <u-icon name="reload" />同步数据
            </u-button>
        </div>
    </div>

    <!-- 统计概览 -->
    <div class="stats-grid">
        <div v-for="(stat, key) in busStats" :key="key" class="stat-card">
            <u-icon :name="stat.icon" :color="stat.color" size="24" />
            <div class="stat-info">
                <div class="stat-number">{{ stat.count }}</div>
                <div class="stat-label">{{ stat.label }}</div>
            </div>
        </div>
    </div>

    <!-- 班车列表 -->
    <div class="bus-list">
        <div v-for="bus in filteredBuses" :key="bus.id" class="bus-item">
            <div class="bus-header">
                <div class="bus-info">
                    <div class="bus-number">{{ bus.busNumber }}</div>
                    <div class="bus-route">{{ bus.route }}</div>
                    <u-tag :text="getStatusText(bus.status)" :type="getStatusType(bus.status)" size="mini" />
                </div>
                <div class="bus-actions">
                    <u-button size="mini" type="info" @click="editBus(bus)">编辑</u-button>
                    <u-button size="mini" type="warning" @click="manageSeat(bus)">座位配置</u-button>
                    <u-button size="mini" type="primary" @click="editSchedule(bus)">时刻表</u-button>
                </div>
            </div>

            <div class="bus-details">
                <view class="detail-row">
                    <span>司机：{{ bus.driverName }}</span>
                    <span>座位：{{ bus.totalSeats }}</span>
                    <span>班次：{{ bus.schedule.length }}</span>
                </view>
                <div class="schedule-times">
                    <u-tag v-for="time in bus.schedule" :key="time" :text="time" type="primary" plain size="mini" />
                </div>
            </div>
        </div>
    </div>

    <!-- 班车信息弹窗 -->
    <u-modal v-model="showBusModal" title="班车信息" @confirm="saveBus">
        <view class="modal-content">
            <u-form :model="busForm" ref="busFormRef">
                <u-form-item label="车牌号">
                    <u-input v-model="busForm.busNumber" placeholder="请输入车牌号" />
                </u-form-item>
                <u-form-item label="线路">
                    <u-input v-model="busForm.route" placeholder="如：主校区↔东西湖校区" />
                </u-form-item>
                <u-form-item label="座位数">
                    <u-number-box v-model="busForm.totalSeats" :min="10" :max="60" />
                </u-form-item>
                <u-form-item label="司机">
                    <u-picker :columns="[driverList]" @confirm="selectDriver">
                        <u-input v-model="busForm.driverName" placeholder="选择司机" readonly />
                    </u-picker>
                </u-form-item>
                <u-form-item label="状态">
                    <u-radio-group v-model="busForm.status">
                        <u-radio name="active" label="运营中" />
                        <u-radio name="maintenance" label="维护中" />
                        <u-radio name="inactive" label="停运" />
                    </u-radio-group>
                </u-form-item>
            </u-form>
        </view>
    </u-modal>

    <!-- 座位配置弹窗 -->
    <u-modal v-model="showSeatModal" title="座位配置" @confirm="saveSeatConfig">
        <view class="modal-content">
            <div class="seat-config">
                <div class="config-item">
                    <span>教师预留：</span>
                    <u-number-box v-model="seatConfig.teacherSeats" :min="0" :max="20" />
                </div>
                <div class="config-item">
                    <span>学生开放：</span>
                    <u-number-box v-model="seatConfig.studentSeats" :min="0" :max="50" />
                </div>
                <div class="config-item">
                    <span>管理预留：</span>
                    <u-number-box v-model="seatConfig.reservedSeats" :min="0" :max="10" />
                </div>
                <div class="config-summary">
                    <span>总计：{{ totalAllocated }}/{{ currentBus?.totalSeats || 0 }}</span>
                </div>
            </div>
        </view>
    </u-modal>

    <!-- 时刻表弹窗 -->
    <u-modal v-model="showScheduleModal" title="编辑时刻表" @confirm="saveSchedule">
        <view class="modal-content">
            <div class="schedule-edit">
                <div class="time-inputs">
                    <div v-for="(time, index) in scheduleForm.times" :key="index" class="time-item">
                        <u-datetime-picker v-model="scheduleForm.times[index]" mode="time">
                            <u-input :value="scheduleForm.times[index]" placeholder="选择时间" readonly />
                        </u-datetime-picker>
                        <u-button size="mini" type="error" @click="removeTime(index)">删除</u-button>
                    </div>
                </div>
                <u-button type="primary" size="small" @click="addTime">添加时间</u-button>
                <div class="quick-templates">
                    <u-button v-for="template in timeTemplates" :key="template.name" size="mini"
                        @click="applyTemplate(template)">
                        {{ template.name }}
                    </u-button>
                </div>
            </div>
        </view>
    </u-modal>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 响应式数据
const searchKeyword = ref('');
const showBusModal = ref(false);
const showSeatModal = ref(false);
const showScheduleModal = ref(false);
const currentBus = ref(null);

// 统计数据
const busStats = ref({
    total: { count: 18, label: '总班车', icon: 'car-fill', color: '#667eea' },
    active: { count: 15, label: '运营中', icon: 'checkmark-circle-fill', color: '#67c23a' },
    maintenance: { count: 2, label: '维护中', icon: 'pause-circle-fill', color: '#e6a23c' },
    totalSeats: { count: 720, label: '总座位', icon: 'account-fill', color: '#409eff' }
});

// 司机列表
const driverList = ref(['张师傅', '李师傅', '王师傅', '赵师傅']);

// 时间模板
const timeTemplates = ref([
    { name: '早班车', times: ['07:00', '07:30', '08:00'] },
    { name: '午班车', times: ['12:30', '13:00', '13:30'] },
    { name: '晚班车', times: ['17:30', '18:00', '18:30'] }
]);

// 班车数据
const buses = ref([
    {
        id: 1, busNumber: 'AYB30260', route: '主校区↔东西湖校区',
        driverName: '张师傅', totalSeats: 45, status: 'active',
        schedule: ['07:00', '07:30', '12:30', '17:30']
    },
    {
        id: 2, busNumber: 'ALB328', route: '主校区↔大学城校区',
        driverName: '李师傅', totalSeats: 40, status: 'active',
        schedule: ['08:00', '14:00', '19:00']
    }
]);

// 表单数据
const busForm = ref({
    busNumber: '', route: '', totalSeats: 40,
    driverName: '', status: 'active'
});

const seatConfig = ref({
    teacherSeats: 10, studentSeats: 30, reservedSeats: 5
});

const scheduleForm = ref({
    times: ['07:00']
});

// 计算属性
const filteredBuses = computed(() => {
    if (!searchKeyword.value) return buses.value;
    return buses.value.filter(bus =>
        bus.busNumber.includes(searchKeyword.value) ||
        bus.route.includes(searchKeyword.value)
    );
});

const totalAllocated = computed(() =>
    seatConfig.value.teacherSeats + seatConfig.value.studentSeats + seatConfig.value.reservedSeats
);

// 方法
const getStatusText = (status: string) => {
    const map = { active: '运营中', maintenance: '维护中', inactive: '停运' };
    return map[status] || status;
};

const getStatusType = (status: string) => {
    const map = { active: 'success', maintenance: 'warning', inactive: 'error' };
    return map[status] || 'default';
};

const handleSearch = () => { };

const editBus = (bus: any) => {
    busForm.value = { ...bus };
    showBusModal.value = true;
};

const manageSeat = (bus: any) => {
    currentBus.value = bus;
    showSeatModal.value = true;
};

const editSchedule = (bus: any) => {
    currentBus.value = bus;
    scheduleForm.value.times = [...bus.schedule];
    showScheduleModal.value = true;
};

const selectDriver = (value: any) => {
    busForm.value.driverName = value.value[0];
};

const addTime = () => {
    scheduleForm.value.times.push('08:00');
};

const removeTime = (index: number) => {
    scheduleForm.value.times.splice(index, 1);
};

const applyTemplate = (template: any) => {
    scheduleForm.value.times = [...template.times];
};

const saveBus = () => {
    showBusModal.value = false;
    uni.showToast({ title: '保存成功', icon: 'success' });
};

const saveSeatConfig = () => {
    showSeatModal.value = false;
    uni.showToast({ title: '座位配置已保存', icon: 'success' });
};

const saveSchedule = () => {
    if (currentBus.value) {
        currentBus.value.schedule = [...scheduleForm.value.times];
    }
    showScheduleModal.value = false;
    uni.showToast({ title: '时刻表已保存', icon: 'success' });
};

const syncData = () => {
    uni.showToast({ title: '数据同步完成', icon: 'success' });
};
</script>

<style lang="scss" scoped>
.page-container {
    padding: 20rpx;
    background: #f5f6fa;
    min-height: 100vh;
}

.header-section {
    display: flex;
    gap: 20rpx;
    align-items: center;
    margin-bottom: 30rpx;

    .u-search {
        flex: 1;
    }

    .action-buttons {
        display: flex;
        gap: 15rpx;
    }
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20rpx;
    margin-bottom: 30rpx;
}

.stat-card {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx 20rpx;
    display: flex;
    align-items: center;
    gap: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .stat-info {
        .stat-number {
            font-size: 32rpx;
            font-weight: 600;
            color: #303133;
        }

        .stat-label {
            font-size: 24rpx;
            color: #909399;
        }
    }
}

.bus-list {
    .bus-item {
        background: white;
        border-radius: 16rpx;
        margin-bottom: 20rpx;
        padding: 30rpx;
        box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

        .bus-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20rpx;

            .bus-info {
                .bus-number {
                    font-size: 32rpx;
                    font-weight: 600;
                    color: #303133;
                    margin-bottom: 8rpx;
                }

                .bus-route {
                    font-size: 26rpx;
                    color: #606266;
                    margin-bottom: 10rpx;
                }
            }

            .bus-actions {
                display: flex;
                gap: 10rpx;
                flex-wrap: wrap;
            }
        }

        .bus-details {
            .detail-row {
                display: flex;
                gap: 30rpx;
                font-size: 24rpx;
                color: #909399;
                margin-bottom: 15rpx;
            }

            .schedule-times {
                display: flex;
                gap: 10rpx;
                flex-wrap: wrap;
            }
        }
    }
}

.modal-content {
    padding: 20rpx;
}

.seat-config {
    .config-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20rpx 0;
        border-bottom: 1rpx solid #f5f6fa;

        span {
            font-size: 28rpx;
            color: #303133;
        }
    }

    .config-summary {
        padding: 20rpx 0;
        text-align: center;
        font-size: 28rpx;
        font-weight: 600;
        color: #667eea;
    }
}

.schedule-edit {
    .time-inputs {
        margin-bottom: 20rpx;

        .time-item {
            display: flex;
            gap: 20rpx;
            align-items: center;
            margin-bottom: 15rpx;
        }
    }

    .quick-templates {
        display: flex;
        gap: 15rpx;
        margin-top: 20rpx;
        flex-wrap: wrap;
    }
}
</style>