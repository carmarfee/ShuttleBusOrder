<template>
<div class="notification-detail">
    <div class="content-container">
        <!-- 通知头部信息 -->
        <div class="notification-header">
            <div class="header-card">
                <div class="title-section">
                    <div class="icon-wrapper">
                        <up-icon name="bell" size="24" color="#667eea"></up-icon>
                    </div>
                    <h1 class="notification-title">{{ notificationData.title }}</h1>
                </div>

                <div class="meta-info">
                    <div class="time-info">
                        <up-icon name="clock" size="16" color="#999"></up-icon>
                        <text class="time-text">{{ formatTime(notificationData.publishTime) }}</text>
                    </div>
                </div>
            </div>
        </div>

        <!-- 通知正文 -->
        <div class="notification-content">
            <div class="content-card">
                <div class="content-header">
                    <div class="header-line"></div>
                    <text class="content-label">通知内容</text>
                </div>
                <div class="content-text">
                    <text>{{ notificationData.content }}</text>
                </div>
            </div>
        </div>

        <!-- 附件区域 -->
        <div class="attachment-section">
            <div class="attachment-card">
                <div class="attachment-header">
                    <div class="header-line"></div>
                    <text class="attachment-label">相关附件</text>
                </div>

                <!-- 有附件时显示 -->
                <div v-if="notificationData.attachments && notificationData.attachments.length > 0"
                    class="attachment-list">
                    <div v-for="(attachment, index) in notificationData.attachments" :key="index"
                        class="attachment-item" @tap="downloadAttachment(attachment)">
                        <div class="attachment-info">
                            <div class="file-icon">
                                <up-icon :name="getFileIcon(attachment.type)" size="20" color="#667eea"></up-icon>
                            </div>
                            <div class="file-details">
                                <text class="file-name">{{ attachment.name }}</text>
                                <text class="file-size">{{ formatFileSize(attachment.size) }}</text>
                            </div>
                        </div>
                        <div class="download-btn">
                            <up-icon name="download" size="18" color="#667eea"></up-icon>
                        </div>
                    </div>
                </div>

                <!-- 无附件时显示 -->
                <div v-else class="no-attachment">
                    <div class="no-attachment-icon">
                        <up-icon name="folder-open" size="32" color="#ddd"></up-icon>
                    </div>
                    <text class="no-attachment-text">暂无附件</text>
                </div>
            </div>
        </div>

    </div>

    <!-- 加载提示 -->
    <up-loading-page :loading="loading" loadingText="加载中..." loadingColor="#667eea"></up-loading-page>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 接口定义
interface Attachment {
    name: string
    type: string
    size: number
    url: string
}

interface NotificationData {
    id: string
    title: string
    content: string
    publishTime: string
    isConfirmed: boolean
    attachments?: Attachment[]
}

// 响应式数据
const loading = ref(true)
const notificationData = ref<NotificationData>({
    id: '',
    title: '',
    content: '',
    publishTime: '',
    isConfirmed: false,
    attachments: []
})

// 获取按钮样式
const getButtonStyle = () => {
    if (notificationData.value.isConfirmed) {
        return {
            background: '#52c41a',
            border: 'none',
            boxShadow: '0 4px 12px rgba(82, 196, 26, 0.3)',
            opacity: '0.8'
        }
    } else {
        return {
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
        }
    }
}

// 页面加载
onMounted(() => {
    loadNotificationDetail()
})

// 加载通知详情
const loadNotificationDetail = async () => {
    try {
        loading.value = true

        // 模拟数据 - 实际开发中这里应该是API调用
        setTimeout(() => {
            notificationData.value = {
                id: '1',
                title: '班车路线临时调整通知',
                content: '亲爱的同学们，由于道路施工原因，明日（3月21日）早班车路线将临时调整。新路线：学校正门→建设路→人民路→目的地。请各位同学提前做好准备，给您带来的不便敬请谅解。如有疑问请联系班车管理员。',
                publishTime: '2025-03-20 15:30:00',
                isConfirmed: false,
                attachments: [
                    {
                        name: '班车调整路线图.pdf',
                        type: 'pdf',
                        size: 2048576, // 2MB
                        url: 'https://example.com/route-map.pdf'
                    },
                    {
                        name: '联系方式.docx',
                        type: 'docx',
                        size: 524288, // 512KB
                        url: 'https://example.com/contact.docx'
                    }
                ]
            }
            loading.value = false
        }, 1000)
    } catch (error) {
        console.error('加载通知详情失败:', error)
        loading.value = false
        uni.showToast({
            title: '加载失败',
            icon: 'error'
        })
    }
}

// 返回上一页
const goBack = () => {
    uni.navigateBack()
}

// 格式化时间
const formatTime = (timeStr: string) => {
    const date = new Date(timeStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()

    // 小于1小时显示分钟
    if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}分钟前`
    }

    // 小于24小时显示小时
    if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}小时前`
    }

    // 超过24小时显示具体日期
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString().slice(0, 5)
}

// 获取文件图标
const getFileIcon = (fileType: string) => {
    const iconMap: { [key: string]: string } = {
        'pdf': 'file-text',
        'docx': 'file-text',
        'doc': 'file-text',
        'xlsx': 'grid',
        'xls': 'grid',
        'pptx': 'play-circle',
        'ppt': 'play-circle',
        'jpg': 'image',
        'jpeg': 'image',
        'png': 'image',
        'gif': 'image',
        'zip': 'folder',
        'rar': 'folder'
    }
    return iconMap[fileType.toLowerCase()] || 'file'
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// 下载附件
const downloadAttachment = (attachment: Attachment) => {
    uni.showLoading({
        title: '下载中...'
    })

    // 模拟下载
    setTimeout(() => {
        uni.hideLoading()
        uni.showToast({
            title: '下载完成',
            icon: 'success'
        })
    }, 2000)
}

// 确认通知
const confirmNotification = () => {
    if (!notificationData.value.isConfirmed) {
        notificationData.value.isConfirmed = true
        uni.showToast({
            title: '已确认',
            icon: 'success'
        })
    }
}
</script>

<style lang="scss" scoped>
.notification-detail {
    min-height: 100vh;
    background: linear-gradient(180deg, #f8f9ff 0%, #f0f2ff 100%);
}

.content-container {
    padding: 0 15px 20px;
    padding-top: 10px;
}

// 通知头部
.notification-header {
    margin-bottom: 20px;
}

.header-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    position: relative;
    overflow: hidden;

    &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
}

.title-section {
    display: flex;
    align-items: flex-start;
    margin-bottom: 15px;
}

.icon-wrapper {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
    flex-shrink: 0;
}

.notification-title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    line-height: 1.4;
    margin: 0;
    flex: 1;
}

.meta-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.time-info {
    display: flex;
    align-items: center;
    gap: 6px;
}

.time-text {
    font-size: 14px;
    color: #999;
}

.status-tag {
    margin-left: 10px;
}

// 通知内容
.notification-content {
    margin-bottom: 20px;
}

.content-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.content-header,
.attachment-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.header-line {
    width: 4px;
    height: 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 2px;
    margin-right: 10px;
}

.content-label,
.attachment-label {
    font-size: 16px;
    font-weight: 600;
    color: #333;
}

.content-text {
    font-size: 15px;
    line-height: 1.6;
    color: #666;
    text-align: justify;
}

// 附件区域
.attachment-section {
    margin-bottom: 30px;
}

.attachment-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.attachment-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.attachment-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    background: #f8f9ff;
    border-radius: 12px;
    border: 1px solid #e8ebff;
    transition: all 0.3s ease;

    &:active {
        background: #f0f2ff;
        transform: scale(0.98);
    }
}

.attachment-info {
    display: flex;
    align-items: center;
    flex: 1;
}

.file-icon {
    width: 36px;
    height: 36px;
    background: white;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.file-details {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.file-name {
    font-size: 14px;
    font-weight: 500;
    color: #333;
    margin-bottom: 2px;
}

.file-size {
    font-size: 12px;
    color: #999;
}

.download-btn {
    width: 32px;
    height: 32px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;

    &:active {
        background: rgba(102, 126, 234, 0.2);
    }
}

// 无附件状态
.no-attachment {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 20px;
}

.no-attachment-icon {
    margin-bottom: 10px;
}

.no-attachment-text {
    font-size: 14px;
    color: #999;
}

// 操作按钮
.action-section {
    padding-bottom: 20px;
}

.action-buttons {
    display: flex;
    justify-content: center;
}

.action-buttons .up-button {
    width: 200px;
    height: 48px;
}

// 响应式适配
@media (max-width: 375px) {
    .content-container {
        padding: 0 12px 20px;
    }

    .notification-title {
        font-size: 16px;
    }

    .content-text {
        font-size: 14px;
    }

    .action-buttons .up-button {
        width: 100%;
    }
}
</style>