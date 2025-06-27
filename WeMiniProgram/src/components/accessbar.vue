<template>
<div class="quick-entry-container">
    <div class="card">
        <div class="item item--1" @tap="handleItemClick(0)" :class="{ 'item-active': activeIndex === 0 }">
            <div class="icon-wrapper">
                <up-icon name="yuyue" customPrefix="custom-icon" size="40" color="rgba(149,149,255,1)"></up-icon>
            </div>
            <p class="quantity">立即预约</p>
            <p class="description">点击开始预约</p>
        </div>

        <div class="item item--2" @tap="handleItemClick(1)" :class="{ 'item-active': activeIndex === 1 }">
            <div class="icon-wrapper">
                <up-icon name="saomashibie" customPrefix="custom-icon" size="40" color="rgba(252,161,71,1)"></up-icon>
            </div>
            <p class="quantity">扫码乘车</p>
            <p class="description">出示乘车码</p>
        </div>

        <div class="item item--3" @tap="handleItemClick(2)" :class="{ 'item-active': activeIndex === 2 }">
            <div class="icon-wrapper">
                <up-icon name="xiaoxi" customPrefix="custom-icon" size="40" color="rgba(66,193,110,1)"></up-icon>
            </div>
            <p class="quantity">消息中心</p>
            <p class="description">消息通知中心</p>
        </div>

        <div class="item item--4" @tap="handleItemClick(3)" :class="{ 'item-active': activeIndex === 3 }">
            <div class="icon-wrapper">
                <up-icon name="huiyixuzhi" customPrefix="custom-icon" size="45" color="rgba(220,91,183,1)"></up-icon>
            </div>
            <p class="quantity">预约须知</p>
            <p class="description">预约相关事项</p>
        </div>
    </div>

    <u-modal :content="content" title="预约规则" :show="show" @confirm="() => show = false">
        <div class="card-rule-info">
            <p>1. 每位学生每月可预约班车次数为2次，超过2次将无法预约。</p>
            <p>2. 每次预约需提前24小时进行，预约时间截止到班车发车前1小时。</p>
            <p>3. 预约成功后，如需取消，请在发车前1小时内取消，否则将视为违约。</p>
        </div>
    </u-modal>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义组件属性
interface Props {
    items?: Array<{
        quantity: string
        description: string
        icon: string
        color: string
        bgColor: string
    }>
}

const props = withDefaults(defineProps<Props>(), {
    items: () => [
        {
            quantity: '立即预约',
            description: '点击开始预约',
            icon: 'yuyue',
            color: 'rgba(149,149,255,1)',
            bgColor: '#c7c7ff'
        },
        {
            quantity: '扫码乘车',
            description: '出示乘车码',
            icon: 'saomashibie',
            color: 'rgba(252,161,71,1)',
            bgColor: '#ffd8be'
        },
        {
            quantity: '消息中心',
            description: '消息通知中心',
            icon: 'xiaoxi',
            color: 'rgba(66,193,110,1)',
            bgColor: '#a9ecbf'
        },
        {
            quantity: '预约须知',
            description: '预约相关事项',
            icon: 'huiyixuzhi',
            color: 'rgba(220,91,183,1)',
            bgColor: '#f3bbe1'
        }
    ]
})

// 定义事件
const emit = defineEmits<{
    itemClick: [index: number, item: any]
}>()

// 响应式数据
const activeIndex = ref(-1)
const show = ref(false)
const content = ref('')

// 方法
const handleItemClick = (index: number) => {
    activeIndex.value = index

    // 重置动画
    setTimeout(() => {
        activeIndex.value = -1
    }, 300)

    // 如果点击预约须知，显示弹窗
    if (index === 3) {
        show.value = true
        return
    }

    // 触发事件
    emit('itemClick', index, props.items[index])

    // 处理不同的点击逻辑
    switch (index) {
        case 0:
            console.log('跳转到预约页面')
            // uni.navigateTo({ url: '/pages/booking/index' })
            break
        case 1:
            console.log('打开扫码页面')
            // uni.navigateTo({ url: '/pages/qrcode/index' })
            break
        case 2:
            console.log('跳转到消息中心')
            // uni.navigateTo({ url: '/pages/message/index' })
            break
        default:
            break
    }
}
</script>

<style lang="scss" scoped>
.quick-entry-container {
    width: 100%;
    padding: 0 15px;
    box-sizing: border-box;
}

.card {
    width: 100%;
    height: 220px;
    color: white;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 12px;
    overflow: visible;
    box-sizing: border-box;
}

.item {
    border-radius: 16px;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

    // 添加微妙的光泽效果
    &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, transparent 50%);
        pointer-events: none;
    }

    // 添加底部反光效果
    &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 30%;
        background: linear-gradient(to top, rgba(0, 0, 0, 0.1) 0%, transparent 100%);
        border-radius: 0 0 16px 16px;
        pointer-events: none;
    }

    &:active {
        transform: scale(0.95);
    }

    &.item-active {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        z-index: 1;
    }
}

.icon-wrapper {
    margin-bottom: 8px;
    transition: all 0.3s ease;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));

    .item-active & {
        transform: scale(1.1);
    }
}

.item--1 {
    background: linear-gradient(135deg, #c7c7ff, #b8b8ff);
}

.item--2 {
    background: linear-gradient(135deg, #ffd8be, #ffcba4);
}

.item--3 {
    background: linear-gradient(135deg, #a9ecbf, #94e7b0);
}

.item--4 {
    background: linear-gradient(135deg, #f3bbe1, #f0aedd);
}

.quantity {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 2px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    letter-spacing: 0.5px;
}

.description {
    font-size: 11px;
    font-weight: 400;
    text-align: center;
    line-height: 1.2;
    opacity: 0.9;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}

.card-rule-info {
    padding: 20px;

    p {
        margin-bottom: 12px;
        line-height: 1.6;
        color: #606266;
        font-size: 14px;

        &:last-child {
            margin-bottom: 0;
        }
    }
}

// 响应式适配
@media (max-width: 375px) {
    .card {
        height: 200px;
        gap: 10px;
    }

    .quantity {
        font-size: 14px;
    }

    .description {
        font-size: 10px;
    }

    .icon-wrapper {
        margin-bottom: 6px;
    }
}

// 大屏适配
@media (min-width: 768px) {
    .quick-entry-container {
        max-width: 600px;
        margin: 0 auto;
    }

    .card {
        height: 240px;
        gap: 15px;
    }

    .quantity {
        font-size: 18px;
    }

    .description {
        font-size: 12px;
    }
}
</style>