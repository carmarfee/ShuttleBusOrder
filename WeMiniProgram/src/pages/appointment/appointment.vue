<template>
<div class="booking-page">
    <!-- 步骤指示器 -->
    <div class="steps-container">
        <div class="steps-wrapper">
            <up-steps :current="currentStep" direction="row" activeColor="#667eea" inactiveColor="#cbd5e1">
                <up-steps-item title="路线选择"></up-steps-item>
                <up-steps-item title="日期选择"></up-steps-item>
                <up-steps-item title="班次选择"></up-steps-item>
            </up-steps>
        </div>
    </div>

    <!-- 步骤内容 -->
    <div class="content-container">
        <!-- 第一步：路线选择 -->
        <div v-if="currentStep === 0" class="step-content">
            <div class="card">
                <div class="card-header">
                    <div class="icon-wrapper">
                        <up-icon name="map-filling" customPrefix="custom-icon" color="#667eea" size="24"></up-icon>
                    </div>
                    <p class="card-title">选择出行路线</p>
                </div>

                <up-radio-group v-model="selectedRoute" placement="column">
                    <div class="option-item" v-for="route in routes" :key="route.value">
                        <up-radio :name="route.value" activeColor="#667eea" size="18">
                            <template #label>
                                <div class="option-card">
                                    <div class="option-main">
                                        <div class="route-path">
                                            <div class="path-item">
                                                <div class="dot start"></div>
                                                <p style="font-size: 30rpx;">{{ route.from }}</p>
                                            </div>
                                            <up-icon name="youjiantou" customPrefix="custom-icon" color="#667eea"
                                                size="16"></up-icon>

                                            <div class="path-item">
                                                <div class="dot end"></div>
                                                <p style="font-size: 30rpx;">{{ route.to }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </up-radio>
                    </div>
                </up-radio-group>
            </div>
        </div>

        <!-- 第二步：日期选择 -->
        <div v-if="currentStep === 1" class="step-content">
            <div class="card">
                <div class="card-header">
                    <div class="icon-wrapper">
                        <up-icon name="calender" customPrefix="custom-icon" color="#667eea" size="24"></up-icon>
                    </div>
                    <p class="card-title">选择出行日期</p>
                </div>

                <up-calendar :show="showCalendar" :defaultDate="selectedDate" @confirm="selectDate" mode="date"
                    :minDate="minDate" :maxDate="maxDate"></up-calendar>

                <div class="date-selector" @tap="showCalendar = true">
                    <div class="date-content">
                        <p class="date-label">出行日期</p>
                        <p class="date-value">{{ selectedDatep }}</p>
                    </div>
                    <up-icon name="youjiantou" customPrefix="custom-icon" color="#94a3b8" size="16"></up-icon>
                </div>
            </div>
        </div>

        <!-- 第三步：班次选择 -->
        <div v-if="currentStep === 2" class="step-content">
            <div class="card">
                <div class="card-header">
                    <div class="icon-wrapper">
                        <up-icon name="clock-filling" customPrefix="custom-icon" color="#667eea" size="24"></up-icon>
                    </div>
                    <p class="card-title">选择班次</p>
                </div>

                <up-radio-group v-model="selectedBus" placement="column">
                    <div class="option-item" v-for="bus in availableBuses" :key="bus.id">
                        <up-radio :name="bus.id" activeColor="#667eea" size="18">
                            <template #label>
                                <div class="option-card bus-card">
                                    <div class="bus-header">
                                        <div class="time-section">
                                            <p class="departure-time">{{ bus.time }}</p>
                                            <p class="vehicle-number">{{ bus.vehicle }}</p>
                                        </div>
                                        <div class="capacity-badge" :class="getCapacityClass(bus.booked, bus.capacity)">
                                            <p>{{ bus.booked }}/{{ bus.capacity }}</p>
                                        </div>
                                    </div>

                                    <div class="bus-route">
                                        <div class="route-line">
                                            <div class="dot start"></div>
                                            <div class="line"></div>
                                            <div class="dot end"></div>
                                        </div>
                                        <div class="route-info">
                                            <p class="from">{{ bus.from }}</p>
                                            <p class="to">{{ bus.to }}</p>
                                        </div>
                                    </div>

                                    <div class="bus-footer">
                                        <div class="driver-info">
                                            <up-icon name="account" customPrefix="custom-icon" color="#94a3b8"
                                                size="12"></up-icon>
                                            <p style="font-size: 18rpx;">{{ bus.driver }}</p>
                                            <up-icon name="phone" customPrefix="custom-icon" color="#94a3b8"
                                                size="14"></up-icon>
                                            <p style="font-size: 18rpx;">{{ bus.phone }}</p>
                                        </div>
                                        <p class="schedule">{{ bus.schedule }}</p>
                                    </div>
                                </div>
                            </template>
                        </up-radio>
                    </div>
                </up-radio-group>
            </div>
        </div>
    </div>

    <!-- 底部操作按钮 -->
    <div class="bottom-actions">
        <up-button v-if="currentStep > 0" @click="currentStep--" :customStyle="secondaryButtonStyle" size="large">
            <up-icon name="arrow-left" color="#64748b" size="16"></up-icon>
            上一步
        </up-button>

        <up-button @click="nextStep" type="primary" :customStyle="primaryButtonStyle" size="large" :loading="submitting"
            :loadingp="submitting ? '提交中...' : ''">
            {{ currentStep === 2 ? '确认预约' : '下一步' }}
            <up-icon v-if="currentStep < 2" name="arrow-right" color="white" size="16"></up-icon>
        </up-button>
    </div>

    <!-- Tabbar组件 -->
    <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import tabbar from '@/components/tabbar.vue'

// 响应式数据
const currentStep = ref(0)
const selectedRoute = ref('')
const selectedDate = ref<string[]>([])
const selectedBus = ref('')
const showCalendar = ref(false)
const submitting = ref(false)

// 静态数据
const routes = [
    { value: 'route1', from: '本部', to: '新校区' },
    { value: 'route2', from: '新校区', to: '本部' },
]

const buses: Record<string, any[]> = {
    route1: [
        {
            id: 'bus1', vehicle: 'AYB260', time: '07:00', driver: '杨师傅', phone: '13971341207',
            from: '信息学部国重门口', to: '新校区新珈楼', schedule: '周一到周五', capacity: 30, booked: 12
        },
        {
            id: 'bus2', vehicle: 'ALB328', time: '12:40', driver: '吴师傅', phone: '15907179119',
            from: '信息学部国重门口', to: '新校区新珈楼', schedule: '周一到周五', capacity: 30, booked: 25
        }
    ],
    route2: [
        {
            id: 'bus3', vehicle: 'ALB160', time: '06:40', driver: '范师傅', phone: '13449989991',
            from: '新校区一食堂', to: '本部当代楼校巴站', schedule: '周一到周日', capacity: 30, booked: 8
        }
    ],
    route3: [
        {
            id: 'bus4', vehicle: 'ALB160', time: '19:00', driver: '范师傅', phone: '13449989991',
            from: '本部当代楼校巴站', to: '新校区一食堂', schedule: '周一到周日', capacity: 30, booked: 15
        }
    ]
}

// 计算属性
const availableBuses = computed(() => buses[selectedRoute.value] || [])
const selectedDatep = computed(() => selectedDate.value[0] || '点击选择日期')
const minDate = computed(() => new Date().getTime())
const maxDate = computed(() => {
    const date = new Date()
    date.setDate(date.getDate() + 7)
    return date.getTime()
})

const primaryButtonStyle = computed(() => ({
    background: 'linear-gradient(135deg, #667eea, #764ba2)',
    borderRadius: '25rpx',
    border: 'none',
    boxShadow: '0 8rpx 25rpx rgba(102, 126, 234, 0.3)'
}))

const secondaryButtonStyle = computed(() => ({
    backgroundColor: '#f8fafc',
    color: '#64748b',
    borderRadius: '25rpx',
    border: 'none',
    boxShadow: 'inset 2rpx 2rpx 6rpx rgba(0,0,0,0.1), inset -2rpx -2rpx 6rpx rgba(255,255,255,0.8)'
}))

// 方法
const selectDate = (e: string[]) => {
    selectedDate.value = e
    showCalendar.value = false
}

const getCapacityClass = (booked: number, capacity: number) => {
    const ratio = booked / capacity
    if (ratio >= 0.9) return 'full'
    if (ratio >= 0.7) return 'warning'
    return 'available'
}

const showToast = (title: string) => {
    uni.showToast({ title, icon: 'none' })
}

const validateStep = () => {
    const validations = [
        () => !selectedRoute.value ? '请选择乘车路线' : null,
        () => !selectedDate.value.length ? '请选择出行日期' : null,
        () => !selectedBus.value ? '请选择班次' : null
    ]

    const error = validations[currentStep.value]()

    if (error) {
        console.log('Validation error:', error)
        showToast(error)
        return false
    }

    console.log('Validation passed for step:', currentStep.value)
    return true
}

const nextStep = () => {
    if (currentStep.value === 2) {
        if (!validateStep()) return

        submitting.value = true
        setTimeout(() => {
            submitting.value = false
            uni.showModal({
                title: '预约成功',
                content: '您的班车预约已成功提交，请按时到达候车点。',
                showCancel: false,
                success: () => uni.navigateBack()
            })
        }, 2000)
        return
    }

    if (validateStep()) {
        currentStep.value++
    }
}
</script>

<style lang="scss" scoped>
.booking-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
    // 调整底部间距，为tabbar和按钮预留空间
    padding-bottom: calc(160rpx + env(safe-area-inset-bottom));
}

// 步骤条样式优化
.steps-container {
    padding: 32rpx;
    position: sticky;
    top: 0;
    z-index: 10;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
}

.steps-wrapper {
    background: #ffffff;
    border-radius: 24rpx;
    padding: 32rpx 40rpx;
    box-shadow: 8rpx 8rpx 20rpx rgba(163, 177, 198, 0.6), -8rpx -8rpx 20rpx rgba(255, 255, 255, 0.8);

    // 确保步骤条内容居中对齐
    :deep(.u-steps) {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    :deep(.u-steps-item) {
        flex: 1;
        text-align: center;

        .u-steps-item__title {
            font-size: 24rpx;
            margin-top: 8rpx;
        }
    }

    :deep(.u-steps-item__line) {
        height: 2rpx;
        background: #e2e8f0;
    }

    :deep(.u-steps-item__icon) {
        width: 32rpx;
        height: 32rpx;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
}

.card {
    background: #ffffff;
    border-radius: 24rpx;
    padding: 40rpx;
    box-shadow: 8rpx 8rpx 20rpx rgba(163, 177, 198, 0.6), -8rpx -8rpx 20rpx rgba(255, 255, 255, 0.8);
}

.content-container {
    padding: 0 32rpx;
}

.step-content {
    margin-bottom: 32rpx;
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 40rpx;

    .icon-wrapper {
        width: 60rpx;
        height: 60rpx;
        border-radius: 30rpx;
        background: #f0f9ff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20rpx;
        box-shadow: inset 2rpx 2rpx 6rpx rgba(102, 126, 234, 0.2), inset -2rpx -2rpx 6rpx rgba(255, 255, 255, 0.8);
    }

    .card-title {
        font-size: 32rpx;
        font-weight: 600;
        color: #1f2937;
    }
}

// 选项通用样式
.option-item {
    margin-bottom: 24rpx;
}

.option-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 32rpx;
    margin-left: 40rpx;
    background: #f8fafc;
    border-radius: 20rpx;
    box-shadow: inset 2rpx 2rpx 6rpx rgba(0, 0, 0, 0.05), inset -2rpx -2rpx 6rpx rgba(255, 255, 255, 0.9);
}

.option-main {
    flex: 1;
}

.option-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 16rpx;
    display: block;
}

// 路线路径样式
.route-path {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;

    .path-item {
        display: flex;
        align-items: center;
        flex: 1;

        p {
            font-size: 20rpx;
            color: #6b7280;
            margin-left: 12rpx;
            white-space: nowrap;
        }
    }

    // 箭头图标居中显示
    .up-icon {
        margin: 0 20rpx;
        flex-shrink: 0;
    }
}

.dot {
    width: 12rpx;
    height: 12rpx;
    border-radius: 50%;

    &.start {
        background: #22c55e;
    }

    &.end {
        background: #ef4444;
    }
}

// 日期选择器
.date-selector {
    display: flex;
    align-items: center;
    padding: 24rpx;
    background: #f8fafc;
    border-radius: 16rpx;
    box-shadow: inset 2rpx 2rpx 6rpx rgba(0, 0, 0, 0.05), inset -2rpx -2rpx 6rpx rgba(255, 255, 255, 0.9);

    .date-icon {
        width: 40rpx;
        height: 40rpx;
        border-radius: 20rpx;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16rpx;
        box-shadow: 2rpx 2rpx 6rpx rgba(0, 0, 0, 0.1), -2rpx -2rpx 6rpx rgba(255, 255, 255, 0.8);
    }

    .date-content {
        flex: 1;

        .date-label {
            font-size: 24rpx;
            color: #6b7280;
            display: block;
            margin-bottom: 4rpx;
        }

        .date-value {
            font-size: 28rpx;
            font-weight: 500;
            color: #1f2937;
        }
    }
}

// 班次卡片样式
.bus-card {
    display: block !important;
}

.bus-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;

    .time-section {
        display: flex;
        align-items: center;
        gap: 16rpx;

        .departure-time {
            font-size: 36rpx;
            font-weight: bold;
            color: #1f2937;
        }

        .vehicle-number {
            font-size: 24rpx;
            color: #6b7280;
            background: #e2e8f0;
            padding: 4rpx 12rpx;
            border-radius: 8rpx;
        }
    }

    .capacity-badge {
        padding: 8rpx 16rpx;
        border-radius: 12rpx;
        font-size: 22rpx;
        font-weight: 500;

        &.available {
            background: #dcfce7;
            color: #166534;
        }

        &.warning {
            background: #fef3c7;
            color: #92400e;
        }

        &.full {
            background: #fee2e2;
            color: #991b1b;
        }
    }
}

.bus-route {
    margin-bottom: 20rpx;

    .route-line {
        display: flex;
        align-items: center;
        margin-bottom: 8rpx;

        .line {
            flex: 1;
            height: 2rpx;
            background: linear-gradient(to right, #22c55e, #ef4444);
            margin: 0 16rpx;
        }
    }

    .route-info {
        display: flex;
        justify-content: space-between;

        .from,
        .to {
            font-size: 24rpx;
            color: #6b7280;
            flex: 1;
        }

        .to {
            text-align: right;
        }
    }
}

.bus-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .driver-info {
        display: flex;
        align-items: center;
        gap: 8rpx;

        p {
            font-size: 22rpx;
            color: #9ca3af;
        }
    }

    .schedule {
        font-size: 22rpx;
        color: #9ca3af;
    }
}

// 底部操作按钮优化
.bottom-actions {
    padding: 24rpx 32rpx;
    backdrop-filter: blur(10rpx);
    border-top: 1rpx solid rgba(0, 0, 0, 0.05);
    display: flex;
    gap: 24rpx;
    z-index: 998; // 确保在tabbar下方

    :deep(.u-button) {
        flex: 1;
        border-radius: 25rpx !important;
        height: 88rpx !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8rpx;
        font-size: 28rpx;
        font-weight: 500;
    }
}
</style>