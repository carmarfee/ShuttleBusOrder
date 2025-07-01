<template>
<view class="verification-container">
    <!-- 标题区域 -->
    <view class="header">
        <text class="title">身份验证上车</text>
        <text class="subtitle">扫描学生证或工作证验证身份</text>
    </view>

    <!-- 扫码区域 -->
    <view class="scan-area">
        <view class="scan-frame" :class="{ 'scanning': isScanning }">
            <view class="scan-border">
                <view class="corner corner-tl"></view>
                <view class="corner corner-tr"></view>
                <view class="corner corner-bl"></view>
                <view class="corner corner-br"></view>
            </view>
            <up-icon name="scan" size="80" color="#ffffff" class="scan-icon"></up-icon>
            <view class="scan-line" v-if="isScanning"></view>
        </view>

        <!-- 扫描状态提示 -->
        <view class="scan-status">
            <text v-if="!isScanning" class="status-text">点击下方按钮开始扫描</text>
            <text v-else class="status-text scanning-text">正在扫描中...</text>
        </view>
    </view>

    <!-- 控制按钮 -->
    <view class="control-area">
        <up-button :type="isScanning ? 'error' : 'primary'" size="large" :text="isScanning ? '停止上车' : '开始上车'"
            @click="toggleScanning" :loading="buttonLoading" loadingText="处理中..."
            customStyle="width: 100%; height: 100rpx; font-size: 32rpx; font-weight: bold;"></up-button>
    </view>

    <!-- 已上车乘客列表 -->
    <view class="passenger-list">
        <view class="list-header">
            <text class="list-title">车上师生 ({{ passengers.length }})</text>
            <view class="filter-tabs">
                <view class="tab-item" :class="{ 'active': activeFilter === 'all' }" @click="setFilter('all')">
                    全部 ({{ passengers.length }})
                </view>
                <view class="tab-item" :class="{ 'active': activeFilter === 'teacher' }" @click="setFilter('teacher')">
                    教职工 ({{ teacherCount }})
                </view>
                <view class="tab-item" :class="{ 'active': activeFilter === 'student' }" @click="setFilter('student')">
                    学生 ({{ studentCount }})
                </view>
            </view>
        </view>

        <scroll-view class="passenger-scroll" scroll-y="true" :style="{ height: scrollHeight + 'px' }"
            v-if="filteredPassengers.length > 0">
            <view class="passenger-item" v-for="(passenger, index) in filteredPassengers" :key="passenger.id">
                <view class="passenger-avatar">
                    <up-avatar :text="passenger.name.slice(-1)"
                        :bgColor="passenger.type === 'teacher' ? '#ff6b35' : '#4299ff'" size="80"></up-avatar>
                    <view class="status-badge" :class="passenger.type">
                        {{ passenger.type === 'teacher' ? '已验证' : '已验证' }}
                    </view>
                </view>

                <view class="passenger-info">
                    <view class="name-row">
                        <text class="passenger-name">{{ passenger.name }}</text>
                        <text class="passenger-id">{{ passenger.studentId }}</text>
                    </view>
                    <view class="detail-row">
                        <text class="passenger-dept">{{ passenger.department }}</text>
                        <text class="passenger-time">{{ passenger.boardTime }}</text>
                    </view>
                    <view class="route-row">
                        <text class="passenger-route">{{ passenger.route }}</text>
                    </view>
                </view>

                <view class="passenger-actions">
                    <up-button type="info" size="mini" text="详情" @click="showDetail(passenger)" plain></up-button>
                </view>
            </view>
        </scroll-view>

        <!-- 空状态 -->
        <view class="empty-state" v-else>
            <up-empty mode="data" :show="true" text="暂无乘客上车"></up-empty>
        </view>
    </view>

    <!-- 乘客详情弹窗 -->
    <up-popup v-model="showDetailPopup" mode="bottom" round="20" :safeAreaInsetBottom="true">
        <view class="detail-popup" v-if="selectedPassenger">
            <view class="popup-header">
                <text class="popup-title">乘客详情</text>
                <up-icon name="close" @click="showDetailPopup = false" size="40"></up-icon>
            </view>
            <view class="popup-content">
                <view class="detail-item">
                    <text class="detail-label">姓名：</text>
                    <text class="detail-value">{{ selectedPassenger.name }}</text>
                </view>
                <view class="detail-item">
                    <text class="detail-label">证件号：</text>
                    <text class="detail-value">{{ selectedPassenger.studentId }}</text>
                </view>
                <view class="detail-item">
                    <text class="detail-label">所属：</text>
                    <text class="detail-value">{{ selectedPassenger.department }}</text>
                </view>
                <view class="detail-item">
                    <text class="detail-label">上车时间：</text>
                    <text class="detail-value">{{ selectedPassenger.boardTime }}</text>
                </view>
                <view class="detail-item">
                    <text class="detail-label">乘车路线：</text>
                    <text class="detail-value">{{ selectedPassenger.route }}</text>
                </view>
            </view>
        </view>
    </up-popup>

    <!-- Toast 提示 -->
    <up-toast ref="uToast"></up-toast>
    <tabbar></tabbar>
</view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import tabbar from '@/components/tabbar.vue'

// 响应式数据
const isScanning = ref(false)
const buttonLoading = ref(false)
const activeFilter = ref('all')
const showDetailPopup = ref(false)
const selectedPassenger = ref(null)
const scrollHeight = ref(400)
const uToast = ref(null)

// 乘客数据
const passengers = ref([
    {
        id: 'A01',
        name: '张三',
        studentId: '2021001234',
        department: '计算机学院 • 大三',
        route: '主校区 → 大学城校区',
        boardTime: '07:25',
        type: 'student'
    },
    {
        id: 'A02',
        name: '李老师',
        studentId: 'T202101',
        department: '计算机学院 • 副教授',
        route: '主校区 → 大学城校区',
        boardTime: '07:28',
        type: 'teacher'
    }
])

// 计算属性
const filteredPassengers = computed(() => {
    if (activeFilter.value === 'all') return passengers.value
    return passengers.value.filter(p => p.type === activeFilter.value)
})

const teacherCount = computed(() =>
    passengers.value.filter(p => p.type === 'teacher').length
)

const studentCount = computed(() =>
    passengers.value.filter(p => p.type === 'student').length
)

// 扫描相关方法
const toggleScanning = () => {
    if (isScanning.value) {
        stopScanning()
    } else {
        startScanning()
    }
}

const startScanning = () => {
    isScanning.value = true
    showToast('开始扫描模式', 'success')
    // 开始连续扫描
    continuousScanning()
}

const stopScanning = () => {
    isScanning.value = false
    showToast('已停止扫描', 'warning')
}

const continuousScanning = () => {
    if (!isScanning.value) return

    uni.scanCode({
        success: (res) => {
            handleScanResult(res.result)
            // 延迟一点再继续扫描，避免过于频繁
            setTimeout(() => {
                if (isScanning.value) {
                    continuousScanning()
                }
            }, 1000)
        },
        fail: (err) => {
            console.log('扫码失败', err)
            if (isScanning.value) {
                // 如果用户取消扫码，停止扫描
                if (err.errMsg.includes('cancel')) {
                    stopScanning()
                } else {
                    // 其他错误继续扫描
                    setTimeout(() => {
                        if (isScanning.value) {
                            continuousScanning()
                        }
                    }, 1000)
                }
            }
        }
    })
}

const handleScanResult = (scanData: string) => {
    try {
        // 模拟扫码结果处理
        const mockPassenger = {
            id: 'A0' + (passengers.value.length + 1),
            name: '王五',
            studentId: '2021005678',
            department: '机械学院 • 大二',
            route: '主校区 → 大学城校区',
            boardTime: getCurrentTime(),
            type: 'student'
        }

        // 检查是否已经上车
        const existingPassenger = passengers.value.find(p => p.studentId === mockPassenger.studentId)
        if (existingPassenger) {
            showToast(`${existingPassenger.name}已经上车`, 'warning')
            playVoice(`${existingPassenger.name}已经上车`)
            return
        }

        // 添加到乘客列表
        passengers.value.push(mockPassenger)

        // 语音提示
        const message = `${mockPassenger.name}上车`
        showToast(message, 'success')
        playVoice(message)

    } catch (error) {
        showToast('扫码数据格式错误', 'error')
    }
}

// 语音播报
const playVoice = (text: string) => {
    // 在实际项目中，你可能需要使用TTS服务或预录音频
    // 这里使用系统提示音作为示例
    uni.showToast({
        title: text,
        icon: 'success',
        duration: 2000
    })

    // 可以集成讯飞语音或其他TTS服务
    // 示例：调用语音合成API
    console.log('语音播报:', text)
}

// 工具方法
const getCurrentTime = () => {
    const now = new Date()
    return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
}

const setFilter = (filter: string) => {
    activeFilter.value = filter
}

const showDetail = (passenger: any) => {
    selectedPassenger.value = passenger
    showDetailPopup.value = true
}

const showToast = (message: string, type: string = 'none') => {
    if (uToast.value) {
        uToast.value.show({
            type: type,
            message: message,
            duration: 2000
        })
    }
}

// 生命周期
onMounted(() => {
    // 计算滚动区域高度
    uni.getSystemInfo({
        success: (res) => {
            // 减去标题、扫码区域、按钮等高度
            scrollHeight.value = res.windowHeight - 600
        }
    })
})

onUnmounted(() => {
    // 页面销毁时停止扫描
    isScanning.value = false
})
</script>

<style lang="scss" scoped>
.verification-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20rpx;
}

.header {
    text-align: center;
    padding: 40rpx 0;

    .title {
        display: block;
        font-size: 48rpx;
        font-weight: bold;
        color: white;
        margin-bottom: 20rpx;
    }

    .subtitle {
        font-size: 28rpx;
        color: rgba(255, 255, 255, 0.8);
    }
}

.scan-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 40rpx;
}

.scan-frame {
    width: 500rpx;
    height: 500rpx;
    background: rgba(0, 0, 0, 0.8);
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;

    &.scanning {
        .scan-icon {
            animation: pulse 2s infinite;
        }
    }
}

.scan-border {
    position: absolute;
    top: 60rpx;
    left: 60rpx;
    right: 60rpx;
    bottom: 60rpx;
    border: 4rpx dashed rgba(255, 255, 255, 0.6);
    border-radius: 16rpx;
}

.corner {
    position: absolute;
    width: 60rpx;
    height: 60rpx;
    border: 6rpx solid #4299ff;

    &.corner-tl {
        top: -6rpx;
        left: -6rpx;
        border-right: none;
        border-bottom: none;
        border-radius: 16rpx 0 0 0;
    }

    &.corner-tr {
        top: -6rpx;
        right: -6rpx;
        border-left: none;
        border-bottom: none;
        border-radius: 0 16rpx 0 0;
    }

    &.corner-bl {
        bottom: -6rpx;
        left: -6rpx;
        border-right: none;
        border-top: none;
        border-radius: 0 0 0 16rpx;
    }

    &.corner-br {
        bottom: -6rpx;
        right: -6rpx;
        border-left: none;
        border-top: none;
        border-radius: 0 0 16rpx 0;
    }
}

.scan-icon {
    z-index: 2;
}

.scan-line {
    position: absolute;
    top: 60rpx;
    left: 60rpx;
    right: 60rpx;
    height: 4rpx;
    background: linear-gradient(90deg, transparent, #4299ff, transparent);
    animation: scanLine 3s linear infinite;
}

.scan-status {
    margin-top: 30rpx;

    .status-text {
        font-size: 28rpx;
        color: rgba(255, 255, 255, 0.9);

        &.scanning-text {
            color: #4299ff;
            font-weight: bold;
        }
    }
}

.control-area {
    margin-bottom: 40rpx;
    padding: 0 40rpx;
}

.passenger-list {
    background: white;
    border-radius: 20rpx 20rpx 0 0;
    flex: 1;
    min-height: 600rpx;
    padding: 30rpx;
}

.list-header {
    margin-bottom: 30rpx;

    .list-title {
        font-size: 36rpx;
        font-weight: bold;
        color: #333;
        margin-bottom: 20rpx;
        display: block;
    }
}

.filter-tabs {
    display: flex;
    background: #f5f5f5;
    border-radius: 12rpx;
    padding: 6rpx;

    .tab-item {
        flex: 1;
        text-align: center;
        padding: 16rpx 24rpx;
        font-size: 24rpx;
        border-radius: 8rpx;
        transition: all 0.3s;

        &.active {
            background: #4299ff;
            color: white;
            font-weight: bold;
        }
    }
}

.passenger-scroll {
    margin-top: 20rpx;
}

.passenger-item {
    display: flex;
    align-items: center;
    padding: 30rpx 0;
    border-bottom: 2rpx solid #f0f0f0;

    &:last-child {
        border-bottom: none;
    }
}

.passenger-avatar {
    position: relative;
    margin-right: 24rpx;

    .status-badge {
        position: absolute;
        bottom: -8rpx;
        right: -8rpx;
        background: #52c41a;
        color: white;
        font-size: 20rpx;
        padding: 4rpx 12rpx;
        border-radius: 20rpx;
        border: 3rpx solid white;

        &.teacher {
            background: #ff6b35;
        }
    }
}

.passenger-info {
    flex: 1;

    .name-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8rpx;

        .passenger-name {
            font-size: 32rpx;
            font-weight: bold;
            color: #333;
        }

        .passenger-id {
            font-size: 24rpx;
            color: #666;
        }
    }

    .detail-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8rpx;

        .passenger-dept {
            font-size: 26rpx;
            color: #666;
        }

        .passenger-time {
            font-size: 24rpx;
            color: #999;
        }
    }

    .route-row {
        .passenger-route {
            font-size: 24rpx;
            color: #4299ff;
        }
    }
}

.passenger-actions {
    margin-left: 20rpx;
}

.empty-state {
    padding: 100rpx 0;
    text-align: center;
}

.detail-popup {
    padding: 40rpx 30rpx;

    .popup-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30rpx;

        .popup-title {
            font-size: 36rpx;
            font-weight: bold;
            color: #333;
        }
    }

    .popup-content {
        .detail-item {
            display: flex;
            padding: 24rpx 0;
            border-bottom: 2rpx solid #f0f0f0;

            .detail-label {
                width: 160rpx;
                font-size: 28rpx;
                color: #666;
            }

            .detail-value {
                flex: 1;
                font-size: 28rpx;
                color: #333;
            }

            &:last-child {
                border-bottom: none;
            }
        }
    }
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.1);
        opacity: 0.7;
    }
}

@keyframes scanLine {
    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(380rpx);
    }
}
</style>