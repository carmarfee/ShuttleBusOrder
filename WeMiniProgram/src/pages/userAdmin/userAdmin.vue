<template>
<div class="page-container">
    <!-- 搜索和操作栏 -->
    <div class="header-section">
        <u-search v-model="searchKeyword" placeholder="搜索用户" @search="handleSearch" />
        <div class="action-buttons">
            <u-button type="primary" size="small" @click="showAddModal = true">
                <u-icon name="plus" />添加用户
            </u-button>
            <u-button type="info" size="small" @click="exportData">
                <u-icon name="download" />导出
            </u-button>
        </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
        <div v-for="(stat, key) in userStats" :key="key" class="stat-card" :class="key">
            <u-icon :name="stat.icon" :color="stat.color" size="24" />
            <div class="stat-info">
                <div class="stat-number">{{ stat.count }}</div>
                <div class="stat-label">{{ stat.label }}</div>
            </div>
        </div>
    </div>

    <!-- 角色筛选 -->
    <u-tabs v-model="activeTab" :list="tabList" @change="handleTabChange" />

    <!-- 用户列表 -->
    <div class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-item">
            <u-avatar :text="user.name" size="50" />
            <div class="user-info">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-meta">
                    <span class="user-id">{{ user.employeeId }}</span>
                    <u-tag :text="getRoleText(user.role)" :type="getRoleType(user.role)" size="mini" />
                </div>
                <div class="user-details">{{ user.department }}</div>
            </div>
            <div class="user-actions">
                <u-button size="mini" type="info" @click="editUser(user)">编辑</u-button>
                <u-button size="mini" type="warning" @click="resetPassword(user)">重置</u-button>
                <u-button size="mini" :type="user.status === 'active' ? 'error' : 'success'"
                    @click="toggleStatus(user)">
                    {{ user.status === 'active' ? '禁用' : '启用' }}
                </u-button>
            </div>
        </div>
    </div>

    <!-- 添加/编辑用户弹窗 -->
    <u-modal v-model="showAddModal" title="用户信息" @confirm="saveUser">
        <view class="modal-content">
            <u-form :model="userForm" ref="formRef">
                <u-form-item label="姓名" prop="name">
                    <u-input v-model="userForm.name" placeholder="请输入姓名" />
                </u-form-item>
                <u-form-item label="工号" prop="employeeId">
                    <u-input v-model="userForm.employeeId" placeholder="请输入工号" />
                </u-form-item>
                <u-form-item label="角色" prop="role">
                    <u-radio-group v-model="userForm.role">
                        <u-radio v-for="role in roleOptions" :key="role.value" :name="role.value" :label="role.label" />
                    </u-radio-group>
                </u-form-item>
                <u-form-item label="部门" prop="department">
                    <u-input v-model="userForm.department" placeholder="请输入部门" />
                </u-form-item>
                <u-form-item label="权限">
                    <u-checkbox-group v-model="userForm.permissions">
                        <u-checkbox v-for="perm in permissionOptions" :key="perm.value" :name="perm.value"
                            :label="perm.label" />
                    </u-checkbox-group>
                </u-form-item>
            </u-form>
        </view>
    </u-modal>
</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 响应式数据
const searchKeyword = ref('');
const activeTab = ref(0);
const showAddModal = ref(false);

// 用户统计
const userStats = ref({
    admin: { count: 5, label: '管理员', icon: 'shield-fill', color: '#ff6b6b' },
    teacher: { count: 156, label: '教师', icon: 'account-fill', color: '#4CAF50' },
    student: { count: 1089, label: '学生', icon: 'account-fill', color: '#2196F3' },
    driver: { count: 12, label: '司机', icon: 'car-fill', color: '#FF9800' }
});

// 标签页
const tabList = ref([
    { name: '全部' }, { name: '管理员' }, { name: '教师' },
    { name: '学生' }, { name: '司机' }
]);

// 角色选项
const roleOptions = ref([
    { value: 'admin', label: '管理员' },
    { value: 'teacher', label: '教师' },
    { value: 'student', label: '学生' },
    { value: 'driver', label: '司机' }
]);

// 权限选项
const permissionOptions = ref([
    { value: 'booking', label: '班车预约' },
    { value: 'cancel', label: '取消预约' },
    { value: 'priority', label: '优先权限' },
    { value: 'manage', label: '管理权限' }
]);

// 用户数据
const users = ref([
    {
        id: 1, name: '张管理', employeeId: 'A001', role: 'admin',
        department: '系统管理部', status: 'active', permissions: ['manage']
    },
    {
        id: 2, name: '李教授', employeeId: 'T001', role: 'teacher',
        department: '计算机学院', status: 'active', permissions: ['booking', 'priority']
    },
    {
        id: 3, name: '王同学', employeeId: 'S001', role: 'student',
        department: '软件工程', status: 'active', permissions: ['booking']
    }
]);

// 用户表单
const userForm = ref({
    name: '', employeeId: '', role: 'student',
    department: '', permissions: []
});

// 计算属性
const filteredUsers = computed(() => {
    let filtered = users.value;

    if (searchKeyword.value) {
        filtered = filtered.filter(user =>
            user.name.includes(searchKeyword.value) ||
            user.employeeId.includes(searchKeyword.value)
        );
    }

    if (activeTab.value > 0) {
        const roleMap = ['', 'admin', 'teacher', 'student', 'driver'];
        filtered = filtered.filter(user => user.role === roleMap[activeTab.value]);
    }

    return filtered;
});

// 方法
const getRoleText = (role: string) => {
    const map = { admin: '管理员', teacher: '教师', student: '学生', driver: '司机' };
    return map[role] || role;
};

const getRoleType = (role: string) => {
    const map = { admin: 'error', teacher: 'success', student: 'primary', driver: 'warning' };
    return map[role] || 'default';
};

const handleSearch = () => { };
const handleTabChange = () => { };

const editUser = (user: any) => {
    userForm.value = { ...user };
    showAddModal.value = true;
};

const resetPassword = (user: any) => {
    uni.showModal({
        title: '重置密码',
        content: `确定重置${user.name}的密码？`,
        success: (res) => {
            if (res.confirm) {
                uni.showToast({ title: '重置成功', icon: 'success' });
            }
        }
    });
};

const toggleStatus = (user: any) => {
    user.status = user.status === 'active' ? 'inactive' : 'active';
    uni.showToast({ title: '操作成功', icon: 'success' });
};

const saveUser = () => {
    showAddModal.value = false;
    uni.showToast({ title: '保存成功', icon: 'success' });
};

const exportData = () => {
    uni.showToast({ title: '导出成功', icon: 'success' });
};
</script>

<style lang="scss" scoped>
.page-container {
    padding: 20rpx;
    background: #f5f6fa;
    min-height: 100vh;
}

.header-section {
    display: flex;
    gap: 20rpx;
    align-items: center;
    margin-bottom: 30rpx;

    .u-search {
        flex: 1;
    }

    .action-buttons {
        display: flex;
        gap: 15rpx;
    }
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20rpx;
    margin-bottom: 30rpx;
}

.stat-card {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx 20rpx;
    display: flex;
    align-items: center;
    gap: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);

    .stat-info {
        .stat-number {
            font-size: 32rpx;
            font-weight: 600;
            color: #303133;
        }

        .stat-label {
            font-size: 24rpx;
            color: #909399;
        }
    }
}

.user-list {
    background: white;
    border-radius: 16rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.user-item {
    display: flex;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid #f5f6fa;
    gap: 20rpx;

    &:last-child {
        border-bottom: none;
    }

    .user-info {
        flex: 1;

        .user-name {
            font-size: 32rpx;
            font-weight: 600;
            color: #303133;
            margin-bottom: 8rpx;
        }

        .user-meta {
            display: flex;
            align-items: center;
            gap: 15rpx;
            margin-bottom: 8rpx;

            .user-id {
                font-size: 24rpx;
                color: #909399;
            }
        }

        .user-details {
            font-size: 24rpx;
            color: #c0c4cc;
        }
    }

    .user-actions {
        display: flex;
        gap: 10rpx;
    }
}

.modal-content {
    padding: 20rpx;
}
</style>