<template>
<view class="notice-card" @tap="handleCardClick">
    <!-- 左侧状态指示器 -->
    <view class="status-indicator"></view>

    <!-- 内容区域 -->
    <view class="content-area">
        <text class="notice-title">{{ noticeData.title }}</text>
        <text class="publish-time">{{ formatTime(noticeData.publishTime) }}</text>
    </view>

    <!-- 右侧箭头 -->
    <view class="arrow-area">
        <up-icon name="youjiantou" customPrefix="custom-icon" size="16" color="#9ca3af"></up-icon>
    </view>
</view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 定义通知数据类型
interface NoticeData {
    id: string | number
    title: string
    publishTime: string | number
}

// 定义组件属性
interface Props {
    noticeData: NoticeData
}

const props = withDefaults(defineProps<Props>(), {
    noticeData: () => ({
        id: '1',
        title: '班车路线临时调整通知',
        publishTime: Date.now() - 1000 * 60 * 30
    })
})

// 定义事件
const emit = defineEmits<{
    cardClick: [noticeData: NoticeData]
}>()

// 格式化时间
const formatTime = computed(() => {
    return (time: string | number) => {
        const now = new Date()
        const publishDate = new Date(time)
        const diff = now.getTime() - publishDate.getTime()

        const minutes = Math.floor(diff / (1000 * 60))
        const hours = Math.floor(diff / (1000 * 60 * 60))
        const days = Math.floor(diff / (1000 * 60 * 60 * 24))

        if (minutes < 1) return '刚刚'
        if (minutes < 60) return `${minutes}分钟前`
        if (hours < 24) return `${hours}小时前`
        if (days < 7) return `${days}天前`

        return publishDate.toLocaleDateString('zh-CN', {
            month: 'short',
            day: 'numeric'
        })
    }
})

// 点击处理
const handleCardClick = () => {
    emit('cardClick', props.noticeData)

    // 跳转到详情页
    uni.navigateTo({
        url: `/pages/notice-detail/index?id=${props.noticeData.id}`
    })
}
</script>

<style lang="scss" scoped>
.notice-card {
    display: flex;
    align-items: center;
    background: #ffffff;
    border-radius: 16rpx;
    margin: 20rpx;
    padding: 24rpx;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease;

    &:active {
        transform: scale(0.98);
        background: #f8fafc;
    }

    &:last-child {
        margin-bottom: 0;
    }
}

/* 左侧状态指示器 */
.status-indicator {
    width: 6rpx;
    height: 40rpx;
    background: #667eea;
    border-radius: 3rpx;
    margin-right: 24rpx;
    flex-shrink: 0;
}

/* 内容区域 */
.content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8rpx;
    min-width: 0;
}

.notice-title {
    font-size: 28rpx;
    font-weight: 500;
    color: #1f2937;
    line-height: 36rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.publish-time {
    font-size: 22rpx;
    color: #9ca3af;
}

/* 右侧箭头 */
.arrow-area {
    margin-left: 16rpx;
    flex-shrink: 0;
}
</style>