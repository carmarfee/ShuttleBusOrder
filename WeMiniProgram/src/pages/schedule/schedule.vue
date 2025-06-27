<template>
<div class="u-page__item">
    <!-- 状态筛选标签 -->
    <u-tabs :list="statusTabs" @click="switchTab" :current="currentIndex" :activeStyle="{
        color: '#667eea',
        fontWeight: 'bold',
        transform: 'scale(1.05)'
    }" :inactiveStyle="{
                color: '#606266'
            }" lineColor="#667eea" lineHeight="3px" :scrollable="false" />

    <!-- 内容区域 -->
    <div class="content">
        <!-- 已预约的行程 -->
        <div v-if="activeTab === 'booked'">
            <u-card v-for="trip in bookedTrips" :key="trip.id" :padding="20" margin="0 0 15px 0" :border-radius="16">
                <template #body>
                    <div class="trip-header">
                        <u-tag text="已预约" type="success" shape="circle" size="mini" />
                        <text class="order-number">{{ trip.orderNumber }}</text>
                    </div>

                    <div class="trip-route">{{ trip.route }}</div>

                    <div class="trip-details">
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="calendar" size="16" color="#666" />
                                <text>出发日期</text>
                            </div>
                            <text class="detail-value">{{ trip.date }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="clock" size="16" color="#666" />
                                <text>发车时间</text>
                            </div>
                            <text class="detail-value">{{ trip.time }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="car" size="16" color="#666" />
                                <text>班车号</text>
                            </div>
                            <text class="detail-value">{{ trip.busNumber }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="account" size="16" color="#666" />
                                <text>座位号</text>
                            </div>
                            <text class="detail-value">{{ trip.seatNumber }}</text>
                        </div>
                    </div>

                    <div class="trip-actions">
                        <u-button text="取消预约" type="info" size="small" :plain="true" @click="cancelTrip(trip.id)" />
                        <u-button text="查看详情" type="primary" size="small"
                            :custom-style="{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"
                            @click="viewDetails(trip.id)" />
                    </div>
                </template>
            </u-card>
        </div>

        <!-- 已完成的行程 -->
        <div v-if="activeTab === 'completed'">
            <u-card v-for="trip in completedTrips" :key="trip.id" :padding="20" margin="0 0 15px 0" :border-radius="16">
                <template #body>
                    <div class="trip-header">
                        <u-tag text="已完成" type="primary" shape="circle" size="mini" />
                        <text class="order-number">{{ trip.orderNumber }}</text>
                    </div>

                    <div class="trip-route">{{ trip.route }}</div>

                    <div class="trip-details">
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="calendar" size="16" color="#666" />
                                <text>出发日期</text>
                            </div>
                            <text class="detail-value">{{ trip.date }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="clock" size="16" color="#666" />
                                <text>发车时间</text>
                            </div>
                            <text class="detail-value">{{ trip.time }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="car" size="16" color="#666" />
                                <text>班车号</text>
                            </div>
                            <text class="detail-value">{{ trip.busNumber }}</text>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">
                                <u-icon name="star" size="16" color="#666" />
                                <text>行程评价</text>
                            </div>
                            <text class="detail-value">{{ trip.rating }}</text>
                        </div>
                    </div>

                    <div class="trip-actions">
                        <u-button text="再次预约" type="info" size="small" :plain="true" @click="bookAgain(trip)" />
                        <u-button text="评价服务" type="primary" size="small"
                            :custom-style="{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"
                            @click="rateTrip(trip.id)" />
                    </div>
                </template>
            </u-card>
        </div>

        <!-- 已取消的行程 -->
        <div v-if="activeTab === 'cancelled'">
            <div v-if="cancelledTrips.length === 0">
                <u-empty mode="car" text="暂无取消的行程记录" :icon-size="120" :text-size="14" :margin-top="80" />
            </div>
            <div v-else>
                <u-card v-for="trip in cancelledTrips" :key="trip.id" :padding="20" margin="0 0 15px 0"
                    :border-radius="16">
                    <template #body>
                        <div class="trip-header">
                            <u-tag text="已取消" type="error" shape="circle" size="mini" />
                            <text class="order-number">{{ trip.orderNumber }}</text>
                        </div>

                        <div class="trip-route">{{ trip.route }}</div>

                        <div class="trip-details">
                            <div class="detail-row">
                                <div class="detail-label">
                                    <u-icon name="calendar" size="16" color="#666" />
                                    <text>原定日期</text>
                                </div>
                                <text class="detail-value">{{ trip.date }}</text>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">
                                    <u-icon name="clock" size="16" color="#666" />
                                    <text>原定时间</text>
                                </div>
                                <text class="detail-value">{{ trip.time }}</text>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">
                                    <u-icon name="close-circle" size="16" color="#666" />
                                    <text>取消时间</text>
                                </div>
                                <text class="detail-value">{{ trip.cancelTime }}</text>
                            </div>
                        </div>

                        <div class="trip-actions">
                            <u-button text="重新预约" type="primary" size="small"
                                :custom-style="{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"
                                @click="bookAgain(trip)" />
                        </div>
                    </template>
                </u-card>
            </div>
        </div>
    </div>

    <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import tabbar from "@/components/tabbar.vue";

// 状态标签配置
const statusTabs = [
    { name: '已预约', value: 'booked' },
    { name: '已完成', value: 'completed' },
    { name: '已取消', value: 'cancelled' }
];

// 当前活动标签
const activeTab = ref<string>('booked');
const currentIndex = computed(() => {
    return statusTabs.findIndex(tab => tab.value === activeTab.value);
});

// 已预约的行程数据
const bookedTrips = ref([
    {
        id: 'BR20250627001',
        orderNumber: 'BR20250627001',
        route: '软件园 → 地铁站',
        date: '2025年6月28日',
        time: '18:30',
        busNumber: 'A线-01号',
        seatNumber: '15号'
    },
    {
        id: 'BR20250627002',
        orderNumber: 'BR20250627002',
        route: '地铁站 → 软件园',
        date: '2025年6月29日',
        time: '08:00',
        busNumber: 'B线-02号',
        seatNumber: '8号'
    }
]);

// 已完成的行程数据
const completedTrips = ref([
    {
        id: 'BR20250626001',
        orderNumber: 'BR20250626001',
        route: '软件园 → 地铁站',
        date: '2025年6月26日',
        time: '18:30',
        busNumber: 'A线-01号',
        rating: '★★★★★'
    },
    {
        id: 'BR20250625001',
        orderNumber: 'BR20250625001',
        route: '地铁站 → 软件园',
        date: '2025年6月25日',
        time: '08:00',
        busNumber: 'B线-02号',
        rating: '★★★★☆'
    }
]);

// 已取消的行程数据
const cancelledTrips = ref([]);

// 切换标签
const switchTab = (item: any, index: number) => {
    activeTab.value = statusTabs[index].value;
};

// 取消预约
const cancelTrip = (tripId: string) => {
    uni.showModal({
        title: '确认取消',
        content: '确定要取消这个预约吗？',
        success: (res) => {
            if (res.confirm) {
                console.log('取消预约:', tripId);
                uni.showToast({
                    title: '取消成功',
                    icon: 'success'
                });
            }
        }
    });
};

// 查看详情
const viewDetails = (tripId: string) => {
    console.log('查看详情:', tripId);
    uni.navigateTo({
        url: `/pages/trip/detail?id=${tripId}`
    });
};

// 再次预约
const bookAgain = (trip: any) => {
    console.log('再次预约:', trip);
    uni.navigateTo({
        url: '/pages/booking/index'
    });
};

// 评价服务
const rateTrip = (tripId: string) => {
    console.log('评价服务:', tripId);
    uni.navigateTo({
        url: `/pages/trip/rate?id=${tripId}`
    });
};
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

.trip-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.order-number {
    font-size: 12px;
    color: #909399;
}

.trip-route {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 15px;
}

.trip-details {
    margin-bottom: 15px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
}

.detail-label {
    display: flex;
    align-items: center;
    color: #606266;

    text {
        margin-left: 6px;
    }
}

.detail-value {
    color: #303133;
    font-weight: 500;
}

.trip-actions {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    padding-top: 15px;
    border-top: 1px solid #f4f4f5;
}

</style>