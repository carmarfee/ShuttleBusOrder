<template>
<div class="u-page__item">
  <div class="content">
    <up-row>
      <up-col span="12">
        <div class="user-header">
          <div class="user-info">
            <h2 class="greeting">你好，{{ userInfo.name }}</h2>
            <p class="student-id">学号：{{ userInfo.id }}</p>
            <div class="stats">
              <div class="stat-item">
                <span class="stat-label">本月取消：</span>
                <span class="stat-value">{{ userInfo.cancelappointments }}/{{ userInfo.totalappointments }}</span>
              </div>
              <div class="credit-badge">
                <span class="credit-text">{{ userInfo.creditStatus }}</span>
              </div>
            </div>
          </div>
        </div>
      </up-col>
    </up-row>
    <up-row justify="space-between">
      <up-col span="6">
        <div class="card card-1">
          <div class="card-1-icon">
            <up-icon size="60" name="a-Group177" customPrefix="custom-icon">
            </up-icon>
          </div>
          <div class="card-1-info">
            <span>
              立即预约
            </span>
            <br>
            <span>
              选择班车快速预约
            </span>
          </div>
        </div>
      </up-col>
      <up-col span="6">
        <div class="card card-1">
          <div class="card-1-icon"><up-icon size="60" name="saomashibie" customPrefix="custom-icon">
            </up-icon></div>
          <div class="card-1-info"><span>
              扫码乘车
            </span>
            <br>
            <span>
              出示二维码乘车
            </span>
          </div>
        </div>
      </up-col>
    </up-row>
    <up-row justify="space-between">
      <up-col span="4">
        <div class="card card-2">
          <div class="card-2-icon">
            <up-icon size="50" name="huiyixuzhi" customPrefix="custom-icon">
            </up-icon>
          </div>
          <div class="card-2-info">预约须知</div>
        </div>
      </up-col>
      <up-col span="4">
        <div class="card card-2">
          <div class="card-2-icon">
            <up-icon size="40" name="xiaoxi" customPrefix="custom-icon" customStyle="padding: 10rpx;">
            </up-icon>
          </div>
          <div class="card-2-info">消息中心</div>
        </div>
      </up-col>
      <up-col span="4">
        <div class="card card-2">
          <div class="card-2-icon">
            <up-icon size="40" name="a-kefufuwu" customPrefix="custom-icon" customStyle="padding: 10rpx;">
            </up-icon>
          </div>
          <div class="card-2-info">联系客服</div>
        </div>
      </up-col>
    </up-row>
  </div>
  <div class="card card-3">
    <div class="card-3-title">
      班车动态
    </div>
    <up-divider></up-divider>
    <div class="card-3-info">
      <span>NoData</span>
    </div>
  </div>
  <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import tabbar from "@/components/tabbar.vue";

const title = ref('班车动态');

const userInfo = ref({
  name: '张小明',
  id: '2025302181111',
  totalappointments: 3,
  cancelappointments: 1,
  creditStatus: '信用良好'
})

//-------------------------------分割线--------------------------------
</script>

<style lang="scss" scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;

  &-1 {
    height: 200rpx;
    margin: 20rpx;
    border-radius: 10px;
    box-shadow: 4px 4px 18px rgba(173, 172, 172, 0.2),
      -4px -4px 18px rgba(162, 160, 160, 0.2);

    &-info {
      text-align: center;
    }
  }

  &-2 {
    height: 140rpx;
    margin: 20rpx;
    border-radius: 10px;
    box-shadow: 4px 4px 18px rgba(173, 172, 172, 0.2),
      -4px -4px 18px rgba(162, 160, 160, 0.2);

    &-info {
      text-align: center;
    }
  }

  &-3 {
    height: 400rpx;
    margin: 20rpx;
    border-radius: 10px;
    box-shadow: 4px 4px 18px rgba(173, 172, 172, 0.2),
      -4px -4px 18px rgba(162, 160, 160, 0.2);

    &-title {
      width: 100%;
      padding-left: 30rpx;
      font-weight: bold;
      font-size: 20px;
      text-align: left;
    }

    &-info {
      text-align: center;
    }
  }
}

.u-page {
  padding: 0;

  &__item {

    &__title {
      color: $u-tips-color;
      background-color: $u-bg-color;
      padding: 15px 15px 5px 15px;
      font-size: 15px;

      &__slot-title {
        color: $u-primary;
        font-size: 14px;
      }
    }

    &__slot-icon {
      width: 17px;
      height: 17px;
    }
  }
}


.u-tabbar-item {
  &__text {
    font-size: 4px !important;
    color: #4e5161;
  }
}

//--------------------------------分割线--------------------------------
.user-header {
  background: linear-gradient(135deg, #4f7cff 0%, #7b5af0 100%);
  border-radius: 15px;
  margin: 20rpx;
  padding: 24rpx;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 8px 32px rgba(79, 124, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.user-info {
  flex: 1;
  z-index: 1;
}

.greeting {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: white;
}

.student-id {
  font-size: 12px;
  margin: 0 0 24px 0;
  opacity: 0.9;
}

.stats {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  margin-left: 4px;
}

.credit-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
}

.credit-text {
  font-size: 14px;
  font-weight: 500;
}

//--------------------------------分割线--------------------------------</style>
