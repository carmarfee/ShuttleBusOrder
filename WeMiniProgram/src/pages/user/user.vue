<template>
<div class="u-page__item">
    <!-- 顶部个人信息区域 -->
    <div class="profile-header">
        <div class="profile-bg-decoration">
            <div class="bg-circle circle-1"></div>
            <div class="bg-circle circle-2"></div>
            <div class="bg-circle circle-3"></div>
        </div>
        <div class="profile-info">
            <div class="avatar-wrapper">
                <u-avatar :src="userInfo.avatar" size="80" :text="userInfo.name" />
                <div class="avatar-status"></div>
            </div>
            <div class="user-details">
                <div class="user-name">{{ userInfo.name }}</div>
                <div class="user-id">
                    <u-icon name="bookmark-fill" size="12" color="rgba(255,255,255,0.8)" />
                    工号：{{ userInfo.employeeId }}
                </div>
                <div class="user-department">
                    <u-icon name="home-fill" size="12" color="rgba(255,255,255,0.8)" />
                    {{ userInfo.department }}
                </div>
            </div>
            <div class="edit-btn" @click="editProfile">
                <u-icon name="edit-pen-fill" color="white" size="18" />
            </div>
        </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
        <u-row :gutter="12">
            <u-col span="4">
                <div class="stat-card booked" @click="navToTrips('booked')">
                    <div class="stat-icon">
                        <u-icon name="calendar-fill" size="24" color="#667eea" />
                    </div>
                    <div class="stat-number">{{ stats.booked }}</div>
                    <div class="stat-label">已预约</div>
                    <div class="stat-bg"></div>
                </div>
            </u-col>
            <u-col span="4">
                <div class="stat-card completed" @click="navToTrips('completed')">
                    <div class="stat-icon">
                        <u-icon name="checkmark-circle-fill" size="24" color="#67c23a" />
                    </div>
                    <div class="stat-number">{{ stats.completed }}</div>
                    <div class="stat-label">已完成</div>
                    <div class="stat-bg"></div>
                </div>
            </u-col>
            <u-col span="4">
                <div class="stat-card cancelled" @click="navToTrips('cancelled')">
                    <div class="stat-icon">
                        <u-icon name="close-circle-fill" size="24" color="#f56c6c" />
                    </div>
                    <div class="stat-number">{{ stats.cancelled }}</div>
                    <div class="stat-label">已取消</div>
                    <div class="stat-bg"></div>
                </div>
            </u-col>
        </u-row>
    </div>

    <!-- 功能菜单 -->
    <div class="content">
        <!-- 我的服务 -->
        <u-card :padding="0" margin="0 0 20px 0" :border-radius="16" class="menu-card">
            <template #body>
                <div class="section-header">
                    <div class="section-title">
                        <u-icon name="grid-fill" size="18" color="#667eea" />
                        我的服务
                    </div>
                    <up-divider lineColor="#cca8e9"></up-divider>
                </div>
                <u-cell-group :border="false">
                    <u-cell v-for="item in serviceMenus" :key="item.name" :title="item.title" :icon="item.icon"
                        :iconStyle="{ color: item.color, fontSize: '22px' }" is-link :border="false"
                        @click="handleMenuClick(item.name)" class="menu-cell">
                        <template #label>
                            <span class="menu-desc">{{ item.desc }}</span>
                        </template>
                        <template #right-icon>
                            <div class="menu-right">
                                <u-badge v-if="item.badge" :count="item.badge" :offset="[0, 0]" />
                                <u-icon name="arrow-right" size="16" color="#c0c4cc" />
                            </div>
                        </template>
                    </u-cell>
                </u-cell-group>
            </template>
        </u-card>

        <!-- 系统设置 -->
        <u-card :padding="0" margin="0 0 20px 0" :border-radius="16" class="menu-card">
            <template #body>
                <div class="section-header">
                    <div class="section-title">
                        <u-icon name="setting-fill" size="18" color="#909399" />
                        系统设置
                    </div>
                    <up-divider lineColor="#71c9ce"></up-divider>
                </div>
                <u-cell-group :border="false">
                    <u-cell v-for="item in settingMenus" :key="item.name" :title="item.title" :icon="item.icon"
                        :iconStyle="{ color: item.color, fontSize: '22px' }" is-link :border="false"
                        @click="handleMenuClick(item.name)" class="menu-cell">
                        <template #label>
                            <span class="menu-desc">{{ item.desc }}</span>
                        </template>
                        <template #right-icon>
                            <div class="menu-right">
                                <u-switch v-if="item.name === 'notification'" v-model="notificationEnabled" size="25"
                                    active-color="#667eea" @change="toggleNotification" />
                                <u-icon v-else name="arrow-right" size="16" color="#c0c4cc" />
                            </div>
                        </template>
                    </u-cell>
                </u-cell-group>
            </template>
        </u-card>

        <!-- 帮助与反馈 -->
        <u-card :padding="0" margin="0 0 20px 0" :border-radius="16" class="menu-card">
            <template #body>
                <div class="section-header">
                    <div class="section-title">
                        <u-icon name="question-circle-fill" size="18" color="#409eff" />
                        帮助与反馈
                    </div>
                    <up-divider lineColor="#ff0000"></up-divider>
                </div>
                <u-cell-group :border="false">
                    <u-cell v-for="item in helpMenus" :key="item.name" :title="item.title" :icon="item.icon"
                        :iconStyle="{ color: item.color, fontSize: '22px' }" is-link :border="false"
                        @click="handleMenuClick(item.name)" class="menu-cell">
                        <template #label>
                            <span class="menu-desc">{{ item.desc }}</span>
                        </template>
                        <template #right-icon>
                            <u-icon name="arrow-right" size="16" color="#c0c4cc" />
                        </template>
                    </u-cell>
                </u-cell-group>
            </template>
        </u-card>

        <!-- 退出登录 -->
        <div class="logout-section">
            <u-button text="退出登录" type="error" :plain="true" size="large" :custom-style="{
                marginTop: '10px',
                border: '1px solid #f56c6c',
                borderRadius: '16px',
                background: 'linear-gradient(135deg, #fff 0%, #fef5f5 100%)'
            }" @click="logout" />
        </div>
    </div>

    <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import tabbar from "@/components/tabbar.vue";

// 用户信息
const userInfo = ref({
    name: '张小明同学',
    employeeId: '202530181111',
    department: '软件开发部',
    avatar: ''
});

// 统计数据
const stats = ref({
    booked: 2,
    completed: 15,
    cancelled: 1
});

// 通知开关
const notificationEnabled = ref(true);

// 我的服务菜单
const serviceMenus = ref([
    {
        name: 'trips',
        title: '我的行程',
        desc: '查看和管理您的出行计划',
        icon: 'calendar-fill',
        color: '#667eea'
    },
    {
        name: 'wallet',
        title: '我的钱包',
        desc: '管理您的账户余额和交易',
        icon: 'wallet-fill',
        color: '#67c23a'
    }
]);

// 系统设置菜单
const settingMenus = ref([
    {
        name: 'notification',
        title: '消息推送',
        desc: '接收重要通知和提醒',
        icon: 'volume-fill',
        color: '#909399'
    },
    {
        name: 'cache',
        title: '清理缓存',
        desc: '释放存储空间，提升性能',
        icon: 'trash-fill',
        color: '#909399'
    }
]);

// 帮助与反馈菜单
const helpMenus = ref([
    {
        name: 'contact',
        title: '联系客服',
        desc: '24小时在线客服支持',
        icon: 'phone-fill',
        color: '#409eff'
    },
    {
        name: 'about',
        title: '关于我们',
        desc: '了解更多产品信息',
        icon: 'info-circle-fill',
        color: '#409eff'
    }
]);

// 编辑个人资料
const editProfile = () => {
    uni.navigateTo({
        url: '/pages/profile/edit'
    });
};

// 跳转到行程页面
const navToTrips = (type: string) => {
    uni.switchTab({
        url: `/pages/trips/index?tab=${type}`
    });
};

// 处理菜单点击
const handleMenuClick = (name: string) => {
    const routeMap: Record<string, string> = {
        trips: '/pages/trips/index',
        favorites: '/pages/profile/favorites',
        messages: '/pages/profile/messages',
        wallet: '/pages/profile/wallet',
        privacy: '/pages/profile/privacy',
        language: '/pages/profile/language',
        cache: '/pages/profile/cache',
        help: '/pages/profile/help',
        feedback: '/pages/profile/feedback',
        contact: '/pages/profile/contact',
        about: '/pages/profile/about'
    };

    if (name === 'notification') {
        return; // 通知开关直接处理，不跳转
    }

    if (name === 'cache') {
        clearCache();
        return;
    }

    const url = routeMap[name];
    if (url) {
        uni.navigateTo({ url });
    }
};

// 切换通知
const toggleNotification = (value: boolean) => {
    uni.showToast({
        title: value ? '已开启通知' : '已关闭通知',
        icon: 'success'
    });
};

// 清理缓存
const clearCache = () => {
    uni.showModal({
        title: '清理缓存',
        content: '确定要清理应用缓存吗？',
        success: (res) => {
            if (res.confirm) {
                // 执行清理缓存逻辑
                setTimeout(() => {
                    uni.showToast({
                        title: '缓存清理完成',
                        icon: 'success'
                    });
                }, 1000);
            }
        }
    });
};

// 退出登录
const logout = () => {
    uni.showModal({
        title: '退出登录',
        content: '确定要退出当前账号吗？',
        success: (res) => {
            if (res.confirm) {
                // 清理用户数据
                uni.removeStorageSync('userToken');
                uni.removeStorageSync('userInfo');

                // 跳转到登录页
                uni.reLaunch({
                    url: '/pages/login/index'
                });
            }
        }
    });
};
</script>

<style lang="scss" scoped>
.u-page__item {
    background: linear-gradient(180deg, #f8f9ff 0%, #f5f5f5 50%);
    min-height: 100vh;
    position: relative;
    padding-bottom: 80px;
}

/* 个人信息头部 */
.profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 20px 35px;
    color: white;
    position: relative;
    overflow: hidden;
    border-radius: 50rpx;
    margin: 20rpx;
}

.profile-bg-decoration {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
}

.bg-circle {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);

    &.circle-1 {
        width: 120px;
        height: 120px;
        top: -30px;
        right: -30px;
        animation: float 6s ease-in-out infinite;
    }

    &.circle-2 {
        width: 80px;
        height: 80px;
        top: 50%;
        right: 20px;
        animation: float 8s ease-in-out infinite reverse;
    }

    &.circle-3 {
        width: 60px;
        height: 60px;
        bottom: 20px;
        left: 30px;
        animation: float 10s ease-in-out infinite;
    }
}

@keyframes float {
    0%,
    100% {
        transform: translateY(0px) rotate(0deg);
    }

    50% {
        transform: translateY(-20px) rotate(180deg);
    }
}

.profile-info {
    display: flex;
    align-items: center;
    gap: 15px;
    position: relative;
    z-index: 2;
}

.avatar-wrapper {
    position: relative;
}

.avatar-status {
    position: absolute;
    bottom: 5px;
    right: 5px;
    width: 16px;
    height: 16px;
    background: #67c23a;
    border: 2px solid white;
    border-radius: 50%;
}

.user-details {
    flex: 1;
}

.user-name {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-id,
.user-department {
    font-size: 13px;
    opacity: 0.9;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.edit-btn {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);

    &:active {
        transform: scale(0.95);
        background: rgba(255, 255, 255, 0.3);
    }
}

/* 统计卡片 */
.stats-section {
    padding: 25px 15px 20px;
    margin-top: -20px;
    position: relative;
    z-index: 2;
}

.stat-card {
    background: white;
    border-radius: 16px;
    padding: 20px 15px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;

    &:active {
        transform: translateY(2px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
    }

    &.booked {
        border-left: 4px solid #667eea;
    }

    &.completed {
        border-left: 4px solid #67c23a;
    }

    &.cancelled {
        border-left: 4px solid #f56c6c;
    }
}

.stat-bg {
    position: absolute;
    top: 0;
    right: 0;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(102, 126, 234, 0.05) 100%);
    border-radius: 0 16px 0 50px;
}

.stat-icon {
    margin-bottom: 8px;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #303133;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 12px;
    color: #909399;
    font-weight: 500;
}

/* 内容区域 */
.content {
    padding: 0 15px;
}

.menu-card {
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;

    &:active {
        transform: translateY(1px);
    }
}

.section-header {
    padding: 20px 20px 15px;
    border-bottom: 1px solid #f8f9fa;
}

.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.section-subtitle {
    font-size: 12px;
    color: #909399;
    margin-left: 26px;
}

.menu-cell {
    padding: 16px 20px !important;
    transition: background-color 0.2s ease;

    &:active {
        background-color: #f8f9ff;
    }
}

.menu-desc {
    font-size: 12px;
    color: #c0c4cc;
    margin-top: 2px;
}

.menu-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 退出登录区域 */
.logout-section {
    padding: 10px 0 20px;
}
</style>