<template>
<div class="container">
    <div class=" bg margin-b30">
        <div class="bubble bubble-1"></div>
        <div class="bubble bubble-2"></div>
        <div class="bubble bubble-3"></div>
        <div class="bubble bubble-4"></div>
        <div class="bubble bubble-5"></div>
        <div class="bubble bubble-6"></div>
    </div>

    <div class="tab vs-row vs-align-center">
        <image class="tab-bg" src="@/static/images/login.png" mode=""></image>
        <div class="vs-row vs-align-center">
            <div class="vs-column vs-align-center margin-r40">
                <span class="font-80 font-weight-500 margin-b20">智约班车</span>
            </div>
        </div>
    </div>

    <div class="login margin-b80">
        <div class="input vs-row vs-align-center margin-b40">
            <image class="input-icon margin-r20" src="@/static/images/id.png" mode=""></image>
            <input class="vs-flex-item color-black-9 font-30" type="span" v-model="id" :maxlength="11"
                placeholder="请输入您的学工号" placeholder-class="input-placeholder" />
        </div>
        <div class="input vs-row vs-align-center margin-b40">
            <image class="input-icon margin-r20" src="@/static/images/pwd.png" mode=""></image>
            <input class="vs-flex-item color-black-9 font-30" type="span" password v-model="password"
                placeholder="请输入您的登录密码" placeholder-class="input-placeholder" />
        </div>
    </div>

    <div class="button bg-color-base vs-row vs-align-center vs-space-center margin-b20 hover-effect" @click="userLogin">
        <span class="color-white font-34">立即登录</span>
    </div>

    <div class="vs-row vs-align-center vs-space-center margin-b40">
        <span class="color-base font-28 hover-text">忘记密码？</span>
    </div>


    <div class="other">
        <up-divider text="更多登录方式"></up-divider>

        <div class="other-items vs-row vs-align-center vs-space-center">
            <div class="guest-button vs-row vs-align-center vs-space-center hover-effect">
                <image class="guest-icon margin-r10" src="@/static/images/guest.png" mode=""></image>
                <span class="color-black-6 font-30">游客登录</span>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';

// 登录表单数据
const id = ref('');
const password = ref('');

const userStore = useUserStore();

//-------------------------------分割线--------------------------------


// 用户登录方法
const userLogin = () => {
    if (id.value === '' || password.value === '') {
        uni.showToast({
            title: '请输入用户名和密码',
            icon: 'none'
        });
        return;
    }
    userStore.actions.LoginIn({ id: id.value, password: password.value });
};
// 游客登录方法
const guestLogin = () => {
    console.log('游客登录');
    // 这里可以添加游客登录的逻辑
};
</script>

<style lang="scss">
.container {
    position: relative;
    font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
}

.bg {
    position: relative;
    width: 750rpx;
    height: 400rpx;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
}

.bubble {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    pointer-events: none;
    animation: float 6s ease-in-out infinite;
}

.bubble-1 {
    width: 60px;
    height: 60px;
    top: -30px;
    right: -30px;
    animation-delay: 0s;
    background: rgba(255, 255, 255, 0.08);
}

.bubble-2 {
    width: 40px;
    height: 40px;
    top: 20px;
    right: 40px;
    animation-delay: 1s;
    background: rgba(255, 255, 255, 0.12);
}

.bubble-3 {
    width: 20px;
    height: 20px;
    top: 60px;
    right: 80px;
    animation-delay: 2s;
    background: rgba(255, 255, 255, 0.15);
}

.bubble-4 {
    width: 80px;
    height: 80px;
    bottom: -40px;
    left: -40px;
    animation-delay: 0.5s;
    background: rgba(255, 255, 255, 0.06);
}

.bubble-5 {
    width: 30px;
    height: 30px;
    bottom: 40px;
    left: 60px;
    animation-delay: 3s;
    background: rgba(255, 255, 255, 0.1);
}

.bubble-6 {
    width: 15px;
    height: 15px;
    top: 50%;
    left: 20px;
    animation-delay: 4s;
    background: rgba(255, 255, 255, 0.2);
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0px) rotate(0deg);
        opacity: 0.7;
    }

    33% {
        transform: translateY(-10px) rotate(120deg);
        opacity: 1;
    }

    66% {
        transform: translateY(5px) rotate(240deg);
        opacity: 0.8;
    }
}

.tab {
    position: absolute;
    top: 250rpx;
    left: 20rpx;
    right: 20rpx;
    height: 150rpx;
    padding: 0 50rpx;
    background-color: #fff;
    border-top-left-radius: 20rpx;
    border-top-right-radius: 20rpx;
    box-shadow: 0 -5rpx 15rpx rgba(0, 0, 0, 0.05);

    &-bg {
        position: absolute;
        top: -200rpx;
        right: -50rpx;
        width: 440rpx;
        height: 365rpx;
    }
}

.line {
    width: 25rpx;
    height: 7rpx;
}

.login {
    padding: 0 60rpx;
}

.input {
    width: 580rpx;
    height: 90rpx;
    padding: 0 30rpx;
    background-color: rgba(80, 100, 235, 0.1);
    border-radius: 100rpx;
    transition: all 0.3s ease;

    &:focus-within {
        box-shadow: 0 0 10rpx rgba(80, 100, 235, 0.3);
        background-color: rgba(80, 100, 235, 0.15);
    }

    &-icon {
        width: 38rpx;
        height: 38rpx;
    }

    &-placeholder {
        color: #52545f;
        opacity: 0.5;
    }
}

.button {
    width: 630rpx;
    height: 90rpx;
    margin-left: 60rpx;
    border-radius: 100rpx;
    transition: all 0.3s ease;
    box-shadow: 0 5rpx 15rpx rgba(80, 100, 235, 0.3);
}

/* 游客登录样式 */
.guest-login {
    width: 100%;
}

.guest-button {
    height: 80rpx;
    width: 240rpx;
    border-radius: 100rpx;
    border: 1rpx solid rgba(80, 100, 235, 0.2);
    transition: all 0.3s ease;
    cursor: pointer;

    &:active {
        background-color: rgba(80, 100, 235, 0.1);
    }
}

.guest-icon {
    width: 36rpx;
    height: 36rpx;
}

.hover-effect:active {
    transform: scale(0.98);
    opacity: 0.9;
}

.hover-text:active {
    opacity: 0.7;
}

.hover-scale:active {
    transform: scale(1.1);
}

.separator {
    height: 2rpx;
    margin: 0 30rpx;
    background-color: #f5f5f5;
}

// 下边距
.margin-b5 {
    margin-bottom: 5rpx;
}

.margin-b10 {
    margin-bottom: 10rpx;
}

.margin-b15 {
    margin-bottom: 15rpx;
}

.margin-b20 {
    margin-bottom: 20rpx;
}

.margin-b25 {
    margin-bottom: 25rpx;
}

.margin-b30 {
    margin-bottom: 30rpx;
}

.margin-b40 {
    margin-bottom: 40rpx;
}

.margin-b60 {
    margin-bottom: 60rpx;
}

.margin-b80 {
    margin-bottom: 80rpx;
}

.margin-b100 {
    margin-bottom: 100rpx;
}

// 右边距
.margin-r5 {
    margin-right: 5rpx;
}

.margin-r10 {
    margin-right: 10rpx;
}

.margin-r15 {
    margin-right: 15rpx;
}

.margin-r20 {
    margin-right: 20rpx;
}

.margin-r25 {
    margin-right: 25rpx;
}

.margin-r30 {
    margin-right: 30rpx;
}

.margin-r40 {
    margin-right: 40rpx;
}

.margin-r60 {
    margin-right: 60rpx;
}

// 字体大小
.font-18 {
    font-style: normal;
    font-size: 18rpx;
}

.font-20 {
    font-style: normal;
    font-size: 20rpx;
}

.font-22 {
    font-style: normal;
    font-size: 22rpx;
}

.font-24 {
    font-style: normal;
    font-size: 24rpx;
}

.font-26 {
    font-style: normal;
    font-size: 26rpx;
}

.font-28 {
    font-style: normal;
    font-size: 28rpx;
}

.other {
    .u-divider {
        font-style: normal;

        .u-divider__text {
            font-size: 8px !important;
        }
    }
}


.font-30 {
    font-style: normal;
    font-size: 30rpx;
}

.font-32 {
    font-style: normal;
    font-size: 32rpx;
}

.font-34 {
    font-style: normal;
    font-size: 34rpx;
}

.font-36 {
    font-style: normal;
    font-size: 36rpx;
}

.font-38 {
    font-style: normal;
    font-size: 38rpx;
}

.font-40 {
    font-style: normal;
    font-size: 40rpx;
}

.font-46 {
    font-style: normal;
    font-size: 46rpx;
}

.font-50 {
    font-style: normal;
    font-size: 50rpx;
}

.font-60 {
    font-style: normal;
    font-size: 60rpx;
}

.font-80 {
    font-style: normal;
    font-size: 80rpx;
}

// 字体对齐
.span-left {
    span-align: left;
}

.span-center {
    span-align: center;
}

.span-right {
    span-align: right;
}

// color相关
.color-white {
    color: #FFFFFF;
}

.color-red {
    color: #dc0000;
}

.color-blue {
    color: #3f97d1;
}

// 黑色色阶向下
.color-black {
    color: #000;
}

.color-black-3 {
    color: #333;
}

.color-black-6 {
    color: #666;
}

.color-black-9 {
    color: #5b4f4f;
}

// 字体宽度
.font-weight-400 {
    font-weight: 400;
}

.font-weight-500 {
    font-weight: bold;
}

// 间隔
.spacing-20 {
    width: 750rpx;
    height: 20rpx;
    background-color: #f8f8f8;
}

// 圆角
.radius-10 {
    border-radius: 10rpx;
}

.radius-20 {
    border-radius: 20rpx;
}

.radius-30 {
    border-radius: 30rpx;
}

.radius-circle {
    border-radius: 50%;
}

.radius-height {
    border-radius: 10000px;
}

// flex相关
.vs-flex-item {
    flex: 1;
}

.vs-space-between {
    justify-content: space-between;
}

.vs-space-around {
    justify-content: space-around;
}

.vs-space-center {
    justify-content: center;
}

.vs-space-end {
    justify-content: flex-end;
}

.vs-row {
    flex-direction: row;
}

.vs-column {
    flex-direction: column;
}

.vs-align-end {
    align-items: flex-end;
}

.vs-align-center {
    display: flex;
    align-items: center;
}

.vs-align-start {
    align-items: flex-start;
}

.vs-item-hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.vs-btn-hover {
    opacity: 0.8;
}

.color-base {
    color: #5064eb;
}

.bg-color-base {
    background-color: #5064eb;
}
</style>