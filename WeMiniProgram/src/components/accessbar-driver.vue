<template>
<div class="quick-entry-container">
    <div class="card">
        <div class="item item--1" @tap="handleItemClick(0)" :class="{ 'item-active': activeIndex === 0 }">
            <div class="icon-wrapper">
                <up-icon name="yuyue" customPrefix="custom-icon" size="40" color="rgba(149,149,255,1)"></up-icon>
            </div>
            <p class="quantity">乘客核验</p>
            <p class="description">点击进行乘客核验</p>
        </div>

        <div class="item item--2" @tap="handleItemClick(1)" :class="{ 'item-active': activeIndex === 1 }">
            <div class="icon-wrapper">
                <up-icon name="saomashibie" customPrefix="custom-icon" size="40" color="rgba(252,161,71,1)"></up-icon>
            </div>
            <p class="quantity">预约情况</p>
            <p class="description">查看当前班次预约情况</p>
        </div>
    </div>

</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';



const linkList = ref([
    {
        name: "核验",
        url: "/pages/verification/verification",
    },
    {
        name: "乘客",
        url: "/pages/passenger/passenger",
    }
])
//-------------------------------分割线--------------------------------


const handleItemClick = (index: number) => {

    // 重置动画
    setTimeout(() => {
    }, 300)

    // 处理不同的点击逻辑
    switch (index) {
        case 0:
            uni.navigateTo({
                url: linkList.value[0].url
            })
            break
        case 1:
            uni.navigateTo({
                url: linkList.value[1].url
            })
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
    margin-top: 20rpx;
    margin-bottom: 20rpx;
}

.card {
    width: 100%;
    color: white;
    display: grid;
    grid-template-columns: 1fr 1fr;
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

/* 新增：乘车码相关样式 */
.qrcode-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 20px;
    min-height: 100px;
}

.qrcode-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.loading-text {
    font-size: 14px;
    color: #666;
}

.qrcode-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.qrcode-tip {
    margin-top: 15px;
    text-align: center;
}

.qrcode-tip text {
    font-size: 14px;
    color: #999;
}

// 响应式适配
@media (max-width: 375px) {
    .card {
        height: 100px;
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
        height: 140px;
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