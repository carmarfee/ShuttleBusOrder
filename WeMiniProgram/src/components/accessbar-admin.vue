<template>
<div class="quick-entry-container">
    <div class="card">
        <div class="item item--1" @tap="handleItemClick(0)" :class="{ 'item-active': activeIndex === 0 }">
            <div class="icon-wrapper">
                <up-icon name="account-fill" size="40" color="rgba(102,126,234,1)"></up-icon>
            </div>
            <p class="quantity">用户管理</p>
            <p class="description">管理员工、学生、司机账号</p>
        </div>

        <div class="item item--2" @tap="handleItemClick(1)" :class="{ 'item-active': activeIndex === 1 }">
            <div class="icon-wrapper">
                <up-icon name="car-fill" size="40" color="rgba(103,194,58,1)"></up-icon>
            </div>
            <p class="quantity">班车管理</p>
            <p class="description">管理班车信息和路线配置</p>
        </div>

        <div class="item item--3" @tap="handleItemClick(2)" :class="{ 'item-active': activeIndex === 2 }">
            <div class="icon-wrapper">
                <up-icon name="list-fill" size="40" color="rgba(230,162,60,1)"></up-icon>
            </div>
            <p class="quantity">预约管理</p>
            <p class="description">查看预约情况和数据导出</p>
        </div>

        <div class="item item--4" @tap="handleItemClick(3)" :class="{ 'item-active': activeIndex === 3 }">
            <div class="icon-wrapper">
                <up-icon name="bar-chart-fill" size="40" color="rgba(245,108,108,1)"></up-icon>
            </div>
            <p class="quantity">数据统计</p>
            <p class="description">查看各类报表和分析</p>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const activeIndex = ref(-1);

const linkList = ref([
    {
        name: "用户管理",
        url: "/pages/userAdmin/userAdmin",
    },
    {
        name: "班车管理",
        url: "/pages/busAdmin/busAdmin",
    },
    {
        name: "预约管理",
        url: "/pages/appointmentAdmin/appointmentAdmin",
    },
    {
        name: "数据统计",
        url: "/pages/dataStatistics/dataStatistics",
    }
])

const handleItemClick = (index: number) => {
    activeIndex.value = index;

    // 重置动画
    setTimeout(() => {
        activeIndex.value = -1;
    }, 300)

    // 处理不同的点击逻辑
    if (linkList.value[index]) {
        uni.navigateTo({
            url: linkList.value[index].url
        })
    }
}
</script>

<style lang="scss" scoped>
.quick-entry-container {
    width: 100%;
    padding: 0 20rpx;
    box-sizing: border-box;
    margin: 20rpx 0;
    position: relative;
    z-index: 1;
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
    height: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    z-index: 2;

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
        z-index: 1;
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
        z-index: 1;
    }

    &:active {
        transform: scale(0.95);
    }

    &.item-active {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        z-index: 10;
    }
}

.icon-wrapper {
    margin-bottom: 8px;
    transition: all 0.3s ease;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    position: relative;
    z-index: 3;

    .item-active & {
        transform: scale(1.1);
    }
}

.item--1 {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(102, 126, 234, 0.8));
}

.item--2 {
    background: linear-gradient(135deg, rgba(103, 194, 58, 0.9), rgba(103, 194, 58, 0.8));
}

.item--3 {
    background: linear-gradient(135deg, rgba(230, 162, 60, 0.9), rgba(230, 162, 60, 0.8));
}

.item--4 {
    background: linear-gradient(135deg, rgba(245, 108, 108, 0.9), rgba(245, 108, 108, 0.8));
}

.quantity {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 2px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    letter-spacing: 0.5px;
    position: relative;
    z-index: 3;
}

.description {
    font-size: 11px;
    font-weight: 400;
    text-align: center;
    line-height: 1.2;
    opacity: 0.9;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 3;
}

// 响应式适配
@media (max-width: 375px) {
    .quick-entry-container {
        padding: 0 15rpx;
    }

    .card {
        gap: 10px;
    }

    .item {
        height: 90px;
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
        margin: 20rpx auto;
        padding: 0 30rpx;
    }

    .item {
        height: 120px;
    }

    .card {
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