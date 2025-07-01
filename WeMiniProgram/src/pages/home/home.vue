<template>
<div class="u-page__item">

    <template v-if="role === 'student'">
        <div class="content">
            <up-row>
                <up-col span="12">
                    <div class="user-header">
                        <div class="user-info">
                            <h2 class="greeting">你好，{{ userInfo.name }}{{ userInfo.role }}</h2>
                            <p class="student-id">学工号：{{ userInfo.id }}</p>
                            <div class="stats">
                                <div class="stat-item">
                                    <span class="stat-label">本月取消：</span>
                                    <span class="stat-value">{{ userInfo.cancelappointments }}/{{
                                        userInfo.totalappointments
                                    }}</span>
                                </div>
                                <div class="credit-badge">
                                    <span class="credit-text">{{ userInfo.creditStatus }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </up-col>
            </up-row>
            <span style="margin-left: 20rpx;font-weight: bold;">快捷入口</span>
            <up-row>
                <up-col span="12">
                    <accessbar></accessbar>
                </up-col>
            </up-row>
            <span style="margin-left: 20rpx;font-weight: bold;">班车动态</span>
            <up-row>
                <up-col span="12">
                    <dynamiccard></dynamiccard>
                    <dynamiccard></dynamiccard>
                    <dynamiccard></dynamiccard>
                </up-col>
            </up-row>
        </div>
    </template>

    <template v-else-if="role === 'driver'">
        <div class="content">
            <!-- 司机信息卡片 -->
            <up-row>
                <up-col span="12">
                    <div class="driver-header">
                        <div class="driver-info">
                            <h2 class="greeting">你好，{{ driverInfo.name }}{{ driverInfo.role }}</h2>
                            <p class="driver-id">工号：{{ driverInfo.id }}</p>
                            <div class="route-info">
                                <div class="route-item">
                                    <span class="route-label">驾驶车辆</span>
                                    <span class="route-value">AYB30260</span>
                                </div>
                                <div class="status-badge">
                                    <span class="status-text">{{ driverInfo.workStatus }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </up-col>
            </up-row>

            <span style="margin-left: 20rpx;font-weight: bold;">快捷功能</span>
            <up-row>
                <up-col span="12">
                    <accessbarDriver></accessbarDriver>
                </up-col>
            </up-row>

            <span style="margin-left: 20rpx;font-weight: bold;">今日班次安排</span>
            <up-row>
                <up-col span="12">
                    <div class="schedule-list">
                        <div v-for="(schedule, index) in scheduleList" :key="index" class="schedule-item"
                            :class="{ 'current': schedule.isCurrent, 'completed': schedule.isCompleted }">
                            <div class="schedule-time">{{ schedule.time }}</div>
                            <div class="schedule-route">{{ schedule.route }}</div>
                            <div v-if="schedule.isCurrent" class="current-badge">当前班次</div>
                            <div class="schedule-vehicle">{{ schedule.vehicle }}</div>
                        </div>
                    </div>
                </up-col>
            </up-row>
        </div>
    </template>

    <template v-else-if="role === 'admin'">
        <div class="content">
            <!-- 管理员信息卡片 -->
            <up-row>
                <up-col span="12">
                    <div class="admin-header">
                        <div class="admin-info">
                            <h2 class="greeting">你好，{{ adminInfo.name }}{{ adminInfo.role }}</h2>
                            <p class="admin-id">管理员ID：{{ adminInfo.id }}</p>
                            <div class="admin-stats">
                                <div class="admin-stat-item">
                                    <span class="stat-label">系统状态：</span>
                                    <span class="stat-value">{{ adminInfo.systemStatus }}</span>
                                </div>
                                <div class="admin-badge">
                                    <span class="admin-text">{{ adminInfo.adminLevel }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </up-col>
            </up-row>

            <span style="margin-left: 20rpx;font-weight: bold;">管理功能</span>
            <up-row>
                <up-col span="12">
                    <accessbarAdmin></accessbarAdmin>
                </up-col>
            </up-row>

            <span style="margin-left: 20rpx;font-weight: bold;">今日数据概览</span>
            <up-row>
                <up-col span="12">
                    <div class="data-overview">
                        <div class="data-grid">
                            <div class="data-item">
                                <div class="data-number">{{ todayData.totalBookings }}</div>
                                <div class="data-label">今日预约</div>
                            </div>
                            <div class="data-item">
                                <div class="data-number">{{ todayData.totalTrips }}</div>
                                <div class="data-label">班次总数</div>
                            </div>
                            <div class="data-item">
                                <div class="data-number">{{ todayData.activeUsers }}</div>
                                <div class="data-label">活跃用户</div>
                            </div>
                            <div class="data-item">
                                <div class="data-number">{{ todayData.cancelRate }}%</div>
                                <div class="data-label">取消率</div>
                            </div>
                        </div>
                    </div>
                </up-col>
            </up-row>


        </div>
    </template>

    <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import tabbar from "@/components/tabbar.vue";
import { useUserStore } from "@/stores/userStore";
import dynamiccard from "@/components/dynamiccard.vue";
import accessbar from "@/components/accessbar.vue";
import accessbarDriver from "@/components/accessbar-driver.vue";
import accessbarAdmin from "@/components/accessbar-admin.vue";

const userStore = useUserStore();
const role = userStore.state.userInfo.role;

//-------------------------------学生+老师+游客--------------------------------

const userInfo = ref({
    name: '张小明',
    id: '2025302181111',
    role: '同学',
    totalappointments: 3,
    cancelappointments: 1,
    creditStatus: '信用良好'
})

//-------------------------------司机--------------------------------

// 司机信息
const driverInfo = ref({
    name: '李师傅',
    id: '2025D001',
    role: '',
    vehicleNumber: 'AYB260',
    currentRoute: '主校区→大学城校区',
    workStatus: '正在服务'
});

// 班次安排
const scheduleList = ref([
    { time: '07:00', route: '主校区→东西湖区', vehicle: 'AYB260', isCompleted: true, isCurrent: false },
    { time: '07:30', route: '主校区→东西湖区', vehicle: 'AYB260', isCompleted: false, isCurrent: true },
    { time: '12:40', route: '东西湖区→主校区', vehicle: 'ALB328', isCompleted: false, isCurrent: false },
]);

//-------------------------------管理员--------------------------------

// 管理员信息
const adminInfo = ref({
    name: '王管理',
    id: '2025A001',
    role: '',
    systemStatus: '运行正常',
    adminLevel: '超级管理员'
});

// 今日数据概览
const todayData = ref({
    totalBookings: 156,
    totalTrips: 12,
    activeUsers: 89,
    cancelRate: 8
});



</script>

<style lang="scss" scoped>
.u-page__item {
    background-color: #f5f5f5;
    min-height: 100vh;
    position: relative;
    padding-bottom: 80px;
}

.content {
    padding: 15px;
}

.user-header {
    background: linear-gradient(135deg, #4f7cff 0%, #7b5af0 100%);
    border-radius: 15px;
    margin: 20rpx;
    padding: 24rpx;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    box-shadow: 0 8px 32px rgba(79, 124, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.user-info {
    flex: 1;
    z-index: 1;
}

.greeting {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: white;
}

.student-id {
    font-size: 12px;
    margin: 0 0 24px 0;
    opacity: 0.9;
}

.stats {
    display: flex;
    align-items: center;
    gap: 16px;
}

.stat-item {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.stat-label {
    font-size: 14px;
    opacity: 0.9;
}

.stat-value {
    font-size: 14px;
    font-weight: 600;
    margin-left: 4px;
}

.credit-badge {
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
    cursor: pointer;
    transition: all 0.3s ease;
}

.credit-text {
    font-size: 14px;
    font-weight: 500;
}

//-------------------------------司机--------------------------------

.header {
    background: white;
    padding: 20rpx 30rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);

    .title {
        font-size: 36rpx;
        font-weight: 600;
        color: #333;
        margin: 0;
    }

    .date-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        font-size: 24rpx;
        color: #666;

        .vehicle-number {
            background: #4f7cff;
            color: white;
            padding: 8rpx 16rpx;
            border-radius: 20rpx;
            margin-top: 8rpx;
            font-weight: 500;
        }
    }
}

.status-bar {
    background: white;
    display: flex;
    align-items: center;
    padding: 20rpx 30rpx;
    gap: 40rpx;
    border-bottom: 1rpx solid #f0f0f0;

    .status-item {
        display: flex;
        align-items: center;
        gap: 8rpx;
        font-size: 28rpx;
        color: #666;

        &.weather {
            margin-left: auto;
        }
    }

    .status-icon.online {
        width: 16rpx;
        height: 16rpx;
        background: #52c41a;
        border-radius: 50%;
    }
}

.driver-header {
    background: linear-gradient(135deg, #4f7cff 0%, #7b5af0 100%);
    border-radius: 15px;
    margin: 20rpx;
    padding: 24rpx;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    box-shadow: 0 8px 32px rgba(79, 124, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.driver-info {
    flex: 1;
    z-index: 1;
}

.driver-id {
    font-size: 12px;
    margin: 0 0 24px 0;
    opacity: 0.9;
}

.route-info {
    display: flex;
    align-items: center;
    gap: 16px;
}

.route-item {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.route-label {
    font-size: 14px;
    opacity: 0.9;
}

.route-value {
    font-size: 14px;
    font-weight: 600;
    margin-left: 4px;
}

.status-badge {
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.status-text {
    font-size: 14px;
    font-weight: 500;
}

.main-route-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    margin: 20rpx;
    padding: 30rpx;
    color: white;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);

    .route-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24rpx;

        .route-title {
            font-size: 32rpx;
            font-weight: 600;
            margin: 0;
        }

        .prepare-btn {
            background: #ffa940;
            color: white;
            border: none;
            padding: 16rpx 32rpx;
            border-radius: 40rpx;
            font-size: 24rpx;
            font-weight: 500;
        }
    }

    .vehicle-number-display {
        font-size: 24rpx;
        opacity: 0.9;
        margin-bottom: 30rpx;
    }

    .time-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30rpx;

        .time-item {
            .time-label {
                font-size: 22rpx;
                opacity: 0.8;
                margin-bottom: 8rpx;
            }

            .time-value {
                font-size: 28rpx;
                font-weight: 600;

                &.passenger-count {
                    color: #ffa940;
                }
            }
        }
    }
}

.schedule-list {
    background: white;
    border-radius: 15px;
    margin: 20rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.schedule-item {
    display: flex;
    align-items: center;
    padding: 30rpx;
    border-bottom: 2rpx solid #f5f6fa;
    position: relative;

    &:last-child {
        border-bottom: none;
    }

    &.current {
        background: rgba(79, 124, 255, 0.05);

        .schedule-time {
            color: #4f7cff;
            font-weight: 600;
        }
    }

    &.completed {
        .schedule-time::before {
            content: '●';
            color: #52c41a;
            margin-right: 16rpx;
        }
    }

    .schedule-time {
        width: 120rpx;
        font-size: 28rpx;
        font-weight: 500;
        color: #333;

        &::before {
            content: '●';
            color: #d9d9d9;
            margin-right: 16rpx;
        }
    }

    .schedule-route {
        flex: 1;
        font-size: 28rpx;
        color: #666;
        margin-left: 40rpx;
    }

    .schedule-vehicle {
        font-size: 24rpx;
        color: #999;
        margin-right: 20rpx;
    }

    .current-badge {
        background: #4f7cff;
        color: white;
        padding: 8rpx 16rpx;
        border-radius: 20rpx;
        font-size: 20rpx;
        margin-right: 10rpx;
    }
}

//-------------------------------管理员--------------------------------

.admin-header {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    border-radius: 15px;
    margin: 20rpx;
    padding: 24rpx;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
    position: relative;
    overflow: hidden;
}

.admin-info {
    flex: 1;
    z-index: 1;
}

.admin-id {
    font-size: 12px;
    margin: 0 0 24px 0;
    opacity: 0.9;
}

.admin-stats {
    display: flex;
    align-items: center;
    gap: 16px;
}

.admin-stat-item {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.admin-badge {
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 12px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.admin-text {
    font-size: 14px;
    font-weight: 500;
}

.data-overview {
    background: white;
    border-radius: 15px;
    margin: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.data-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30rpx;
}

.data-item {
    text-align: center;

    .data-number {
        font-size: 32rpx;
        font-weight: 600;
        color: #ff6b6b;
        margin-bottom: 8rpx;
    }

    .data-label {
        font-size: 24rpx;
        color: #666;
    }
}
</style>