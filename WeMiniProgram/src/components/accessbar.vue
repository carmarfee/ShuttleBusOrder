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
            <p class="description">出示下一次的乘车码</p>
        </div>

        <div class="item item--3" @tap="handleItemClick(2)" :class="{ 'item-active': activeIndex === 2 }">
            <div class="icon-wrapper">
                <up-icon name="hangchengxinxi" customPrefix="custom-icon" size="40"
                    color="rgba(150,193,183,1)"></up-icon>
            </div>
            <p class="quantity">我的行程</p>
            <p class="description">查看我的行程</p>
        </div>

        <div class="item item--4" @tap="handleItemClick(3)" :class="{ 'item-active': activeIndex === 3 }">
            <div class="icon-wrapper">
                <up-icon name="huiyixuzhi" customPrefix="custom-icon" size="45" color="rgba(220,91,183,1)"></up-icon>
            </div>
            <p class="quantity">预约须知</p>
            <p class="description">预约相关事项</p>
        </div>
    </div>

    <u-modal title="预约规则" :show="showRule" @confirm="() => showRule = false">
        <div class="card-rule-info">
            <p>1. 每位学生每月可预约班车次数为2次，超过2次将无法预约。</p>
            <p>2. 每次预约需提前24小时进行，预约时间截止到班车发车前1小时。</p>
            <p>3. 预约成功后，如需取消，请在发车前1小时内取消，否则将视为违约。</p>
        </div>
    </u-modal>

    <u-modal title="乘车码" :show="showQcode" @confirm="closeQcode" @close="closeQcode">
        <div class="qrcode-container">
            <!-- 加载状态 -->
            <div v-if="!qrcodeReady && showQcode" class="qrcode-loading">
                <up-loading-icon mode="spinner" color="#409eff" size="40"></up-loading-icon>
                <text class="loading-text">正在生成乘车码...</text>
            </div>

            <!-- 二维码 -->
            <div v-if="showQcode" class="qrcode-wrapper">
                <up-qrcode :cid="'qcode'" :size="150" showLoading loadingText="正在加载" v-show="qrcodeReady"
                    val="https://click.meituan.com/t?t=1&c=2&p=WhaD2b5zGU-h" @result="onQrcodeResult"
                    @error="onQrcodeError">
                </up-qrcode>
            </div>

            <!-- 使用提示 -->
            <div v-if="qrcodeReady" class="qrcode-tip">
                <text>请将此码靠近扫码区</text>
            </div>
        </div>
    </u-modal>

</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from "pinia";
import { useTabbarStore } from '@/stores/tabbarStore';



// 响应式数据
const activeIndex = ref(-1)
const showRule = ref(false)
const showQcode = ref(false)
const qrcodeReady = ref(false) 

const tabbarStore = useTabbarStore();
const { activeTab } = storeToRefs(tabbarStore)

const tabbarList = ref([
    {
        index: 1,
        name: "预约",
        url: "/pages/appointment/appointment",
        icon: "yuyue",
    },
    {
        index: 2,
        name: "行程",
        url: "/pages/schedule/schedule",
        icon: "hangchengxinxi",
    }
])
//-------------------------------分割线--------------------------------


const goToNext = (item: any) => {
    if (item.index === activeTab.value) {
        // 阻止切换
        return;
    }
    tabbarStore.setActiveTab(item.index);
    uni.switchTab({
        url: item.url
    });
};


const handleItemClick = (index: number) => {
    activeIndex.value = index

    // 重置动画
    setTimeout(() => {
        activeIndex.value = -1
    }, 300)

    // 处理不同的点击逻辑
    switch (index) {
        case 0:
            console.log('跳转到预约页面')
            goToNext(tabbarList.value[0])
            break
        case 1:
            console.log('打开扫码页面')
            qrcodeReady.value = false // 重置二维码状态
            showQcode.value = true
            break
        case 2:
            console.log('跳转到我的行程')
            goToNext(tabbarList.value[1])
            break
        case 3:
            console.log('显示预约须知')
            showRule.value = true
            break;
        default:
            break
    }
}

// 新增：二维码生成成功回调
const onQrcodeResult = (result: any) => {
    console.log('二维码生成成功:', result)
    // 延迟0.8秒后显示二维码
    setTimeout(() => {
        qrcodeReady.value = true
    }, 500)
}

// 新增：二维码生成错误回调
const onQrcodeError = (error: any) => {
    console.error('二维码生成失败:', error)
    qrcodeReady.value = false
    uni.showToast({
        title: '二维码生成失败',
        icon: 'error'
    })
}

// 新增：关闭乘车码模态框
const closeQcode = () => {
    qrcodeReady.value = false // 立即隐藏二维码
    showQcode.value = false
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

/* 新增：乘车码相关样式 */
.qrcode-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 20px;
    min-height: 200px;
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