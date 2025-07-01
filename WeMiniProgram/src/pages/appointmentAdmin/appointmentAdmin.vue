<template>
<div class="page-container">
    <!-- 筛选栏 -->
    <div class="filter-section">
        <u-picker :columns="[busOptions]" @confirm="selectBus">
            <u-input v-model="selectedBus" placeholder="选择班车" readonly />
        </u-picker>
        <u-datetime-picker v-model="selectedDate" mode="date">
            <u-input :value="selectedDate" placeholder="选择日期" readonly />
        </u-datetime-picker>
        <u-button type="primary" size="small" @click="showNotifyModal = true">
            <u-icon name="volume-fill" />通知
        </u-button>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
        <div v-for="(stat, key) in bookingStats" :key="key" class="stat-card">
            <u-icon :name="stat.icon" :color="stat.color" size="24" />
            <div class="stat-info">
                <div class="stat-number">{{ stat.count }}</div>
                <div class="stat-label">{{ stat.label }}</div>
            </div>
        </div>
    </div>

    <!-- 班次选择 -->
    <u-tabs v-model="activeTripTab" :list="tripTabs" @change="handleTripChange" />

    <!-- 当前班次信息 -->
    <div class="trip-info-card">
        <div class="trip-header">
            <div class="trip-time">{{ currentTrip.time }}</div>
            <div class="trip-route">{{ currentTrip.route }}</div>
            <u-tag :text="getTripStatusText()" :type="getTripStatusType()" />
        </div>
        <div class="trip-stats">
            <span>{{ currentTrip.bookedSeats }}/{{ currentTrip.totalSeats }} 座位</span>
            <span>发车前1小时自动清理</span>
        </div>
        <div class="trip-actions">
            <u-button size="mini" type="primary" @click="adjustQueue">调整队列</u-button>
            <u-button size="mini" type="warning" @click="cleanupBookings">清理预约</u-button>
        </div>
    </div>

    <!-- 预约队列 -->
    <div class="booking-queue">
        <div v-for="booking in currentBookings" :key="booking.id" class="booking-item">
            <div class="queue-number">{{ booking.queueNumber }}</div>
            <div class="booking-info">
                <div class="user-name">{{ booking.userName }}</div>
                <div class="user-meta">
                    <span class="user-id">{{ booking.userId }}</span>
                    <u-tag :text="getRoleText(booking.userRole)" :type="getRoleType(booking.userRole)" size="mini" />
                    <span class="booking-time">{{ booking.bookingTime }}</span>
                </div>
            </div>
            <div class="booking-status">
                <u-tag :text="getStatusText(booking.status)" :type="getStatusType(booking.status)" />
                <div class="action-buttons">
                    <u-button v-if="booking.status === 'confirmed'" size="mini" type="warning"
                        @click="cancelBooking(booking)">取消</u-button>
                    <u-button v-if="booking.status === 'cancelled'" size="mini" type="success"
                        @click="restoreBooking(booking)">恢复</u-button>
                </div>
            </div>
        </div>
    </div>

    <!-- 队列调整弹窗 -->
    <u-modal v-model="showQueueModal" title="调整队列" @confirm="saveQueueAdjust">
        <view class="modal-content">
            <div class="queue-adjust">
                <u-button type="primary" size="small" @click="autoSort" style="margin-bottom: 20rpx;">
                    按优先级排序
                </u-button>
                <div class="adjustable-list">
                    <div v-for="(booking, index) in adjustableBookings" :key="booking.id" class="adjustable-item">
                        <span class="item-index">{{ index + 1 }}</span>
                        <span class="item-name">{{ booking.userName }}</span>
                        <u-tag :text="getRoleText(booking.userRole)" :type="getRoleType(booking.userRole)"
                            size="mini" />
                        <div class="item-actions">
                            <u-button size="mini" @click="moveUp(index)" :disabled="index === 0">上移</u-button>
                            <u-button size="mini" @click="moveDown(index)"
                                :disabled="index === adjustableBookings.length - 1">下移</u-button>
                        </div>
                    </div>
                </div>
            </div>
        </view>
    </u-modal>

    <!-- 通知弹窗 -->
    <u-modal v-model="showNotifyModal" title="发送通知" @confirm="sendNotification">
        <view class="modal-content">
            <u-form :model="notifyForm">
                <u-form-item label="通知类型">
                    <u-radio-group v-model="notifyForm.type">
                        <u-radio name="departure" label="发车提醒" />
                        <u-radio name="cancellation" label="取消通知" />
                        <u-radio name="queue_change" label="队列变更" />
                    </u-radio-group>
                </u-form-item>
                <u-form-item label="发送对象">
                    <u-checkbox-group v-model="notifyForm.targets">
                        <u-checkbox name="confirmed" label="已确认用户" />
                        <u-checkbox name="waiting" label="等待用户" />
                        <u-checkbox name="all" label="所有用户" />
                    </u-checkbox-group>
                </u-form-item>
                <u-form-item label="发送方式">
                    <u-checkbox-group v-model="notifyForm.methods">
                        <u-checkbox name="app" label="应用推送" />
                        <u-checkbox name="sms" label="短信通知" />
                    </u-checkbox-group>
                </u-form-item>
            </u-form>
        </view>
    </u-modal>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 响应式数据
const selectedBus = ref('');
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const activeTripTab = ref(0);
const showQueueModal = ref(false);
const showNotifyModal = ref(false);

// 班车选项
const busOptions = ref(['AYB30260 主校区↔东西湖校区', 'ALB328 主校区↔大学城校区']);

// 统计数据
const bookingStats = ref({
    total: { count: 156, label: '总预约', icon: 'calendar-fill', color: '#667eea' },
    confirmed: { count: 128, label: '已确认', icon: 'checkmark-circle-fill', color: '#67c23a' },
    cancelled: { count: 18, label: '已取消', icon: 'close-circle-fill', color: '#f56c6c' },
    waiting: { count: 10, label: '等待中', icon: 'time-fill', color: '#e6a23c' }
});

// 班次标签
const tripTabs = ref([
    { name: '07:00班次' }, { name: '07:30班次' },
    { name: '12:30班次' }, { name: '17:30班次' }
]);

// 当前班次信息
const currentTrip = ref({
    time: '07:00', route: '主校区→东西湖校区',
    totalSeats: 45, bookedSeats: 38
});

// 预约数据
const bookings = ref([
    {
        id: 1, queueNumber: 1, userName: '李教授', userId: 'T001',
        userRole: 'teacher', bookingTime: '14:30', status: 'confirmed', tripTime: '07:00'
    },
    {
        id: 2, queueNumber: 2, userName: '张同学', userId: 'S001',
        userRole: 'student', bookingTime: '15:45', status: 'confirmed', tripTime: '07:00'
    },
    {
        id: 3, queueNumber: 3, userName: '王同学', userId: 'S002',
        userRole: 'student', bookingTime: '16:20', status: 'cancelled', tripTime: '07:00'
    }
]);

// 队列调整数据
const adjustableBookings = ref([]);

// 通知表单
const notifyForm = ref({
    type: 'departure', targets: ['confirmed'], methods: ['app']
});

// 计算属性
const currentBookings = computed(() => {
    const currentTripTime = tripTabs.value[activeTripTab.value]?.name.split('班')[0];
    return bookings.value.filter(booking => booking.tripTime === currentTripTime)
        .sort((a, b) => a.queueNumber - b.queueNumber);
});

// 方法
const getRoleText = (role: string) => {
    const map = { teacher: '教师', student: '学生', admin: '管理员' };
    return map[role] || role;
};

const getRoleType = (role: string) => {
    const map = { teacher: 'success', student: 'primary', admin: 'error' };
    return map[role] || 'default';
};

const getStatusText = (status: string) => {
    const map = { confirmed: '已确认', cancelled: '已取消', waiting: '等待中' };
    return map[status] || status;
};

const getStatusType = (status: string) => {
    const map = { confirmed: 'success', cancelled: 'error', waiting: 'warning' };
    return map[status] || 'default';
};

const getTripStatusText = () => '等待发车';
const getTripStatusType = () => 'primary';

const selectBus = (value: any) => {
    selectedBus.value = value.value[0];
};

const handleTripChange = () => {
    const currentTripTime = tripTabs.value[activeTripTab.value]?.name.split('班')[0];
    currentTrip.value.time = currentTripTime;
};

const adjustQueue = () => {
    adjustableBookings.value = [...currentBookings.value.filter(b => b.status === 'confirmed')];
    showQueueModal.value = true;
};

const cleanupBookings = () => {
    uni.showModal({
        title: '清理预约',
        content: '确定清理已取消的预约？',
        success: (res) => {
            if (res.confirm) {
                uni.showToast({ title: '清理完成', icon: 'success' });
            }
        }
    });
};

const cancelBooking = (booking: any) => {
    booking.status = 'cancelled';
    uni.showToast({ title: '预约已取消', icon: 'success' });
};

const restoreBooking = (booking: any) => {
    booking.status = 'confirmed';
    uni.showToast({ title: '预约已恢复', icon: 'success' });
};

const autoSort = () => {
    adjustableBookings.value.sort((a, b) => {
        if (a.userRole === 'teacher' && b.userRole !== 'teacher') return -1;
        if (a.userRole !== 'teacher' && b.userRole === 'teacher') return 1;
        return new Date(a.bookingTime).getTime() - new Date(b.bookingTime).getTime();
    });
};

const moveUp = (index: number) => {
    if (index > 0) {
        [adjustableBookings.value[index], adjustableBookings.value[index - 1]] =
            [adjustableBookings.value[index - 1], adjustableBookings.value[index]];
    }
};

const moveDown = (index: number) => {
    if (index < adjustableBookings.value.length - 1) {
        [adjustableBookings.value[index], adjustableBookings.value[index + 1]] =
            [adjustableBookings.value[index + 1], adjustableBookings.value[index]];
    }
};

const saveQueueAdjust = () => {
    showQueueModal.value = false;
    uni.showToast({ title: '队列调整完成', icon: 'success' });
};

const sendNotification = () => {
    showNotifyModal.value = false;
    uni.showToast({ title: '通知发送成功', icon: 'success' });
};
</script>

<style lang="scss" scoped>
.page-container {
    padding: 20rpx;
    background: #f5f6fa;
    min-height: 100vh;
}

.filter-section {
    display: flex;
    gap: 20rpx;
    margin-bottom: 30rpx;
    align-items: center;
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

.trip-info-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16rpx;
    padding: 30rpx;
    color: white;
    margin-bottom: 30rpx;

    .trip-header {
        display: flex;
        align-items: center;
        gap: 20rpx;
        margin-bottom: 15rpx;

        .trip-time {
            font-size: 36rpx;
            font-weight: 600;
        }

        .trip-route {
            font-size: 28rpx;
        }
    }

    .trip-stats {
        display: flex;
        gap: 30rpx;
        font-size: 24rpx;
        opacity: 0.9;
        margin-bottom: 20rpx;
    }

    .trip-actions {
        display: flex;
        gap: 15rpx;
    }
}

.booking-queue {
    background: white;
    border-radius: 16rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.booking-item {
    display: flex;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid #f5f6fa;
    gap: 20rpx;

    &:last-child {
        border-bottom: none;
    }

    .queue-number {
        width: 60rpx;
        height: 60rpx;
        background: #667eea;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
    }

    .booking-info {
        flex: 1;

        .user-name {
            font-size: 32rpx;
            font-weight: 600;
            color: #303133;
            margin-bottom: 8rpx;
        }

        .user-meta {
            display: flex;
            align-items: center;
            gap: 15rpx;
            font-size: 24rpx;
            color: #909399;
        }
    }

    .booking-status {
        text-align: right;

        .action-buttons {
            margin-top: 10rpx;
        }
    }
}

.modal-content {
    padding: 20rpx;
}

.adjustable-list {
    .adjustable-item {
        display: flex;
        align-items: center;
        gap: 20rpx;
        padding: 20rpx;
        background: #f8f9ff;
        border-radius: 12rpx;
        margin-bottom: 15rpx;

        .item-index {
            width: 40rpx;
            height: 40rpx;
            background: #667eea;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24rpx;
            font-weight: 600;
        }

        .item-name {
            flex: 1;
            font-size: 28rpx;
            font-weight: 600;
        }

        .item-actions {
            display: flex;
            gap: 10rpx;
        }
    }
}
</style>