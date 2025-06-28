<template>
<div class="u-page__item">
  <div class="content">
    <up-row>
      <up-col span="12">
        <div class="user-header">
          <div class="user-info">
            <h2 class="greeting">你好，{{ userInfo.name }}{{ userInfo.role }}</h2>
            <p class="student-id">学工号：{{ userInfo.id }}</p>
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
    <span style="margin-left: 20rpx;font-weight: bold;">快捷入口</span>
    <up-row>
      <up-col span="12">
        <accessbar></accessbar>
      </up-col>
    </up-row>
    <span style="margin-left: 20rpx;font-weight: bold;">班车动态</span>
    <up-row>
      <up-col span="12">
        <dynamiccard></dynamiccard>
        <dynamiccard></dynamiccard>
        <dynamiccard></dynamiccard>
      </up-col>
    </up-row>
  </div>
  
  <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import tabbar from "@/components/tabbar.vue";
import accessbar from "@/components/accessbar.vue";
import dynamiccard from "@/components/dynamiccard.vue";
import { onLoad } from "@dcloudio/uni-app";

const userInfo = ref({
  name: '张小明',
  id: '2025302181111',
  role: '同学',
  totalappointments: 3,
  cancelappointments: 1,
  creditStatus: '信用良好'
})
//-------------------------------分割线--------------------------------

// 定义方法  

onLoad(() => {
  uni.hideTabBar();
});

</script>

<style lang="scss" scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;

  &-rule {
    margin: 20rpx;
    height: 250rpx;
    border: #465bd0 1px solid;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    &-title {
      width: 100%;
      padding-left: 30rpx;
      font-weight: bold;
      font-size: 20px;
      text-align: left;
    }

    &-info {
      text-align: left;
      padding-left: 35rpx;
      font-size: 14px;
      color: #333;
    }
  }

  &-access {
    height: 140rpx;
    margin: 20rpx;
    border-radius: 10px;
    background-image: linear-gradient(to top, #c471f5 0%, #fa71cd 100%);
    box-shadow: 4px 4px 18px rgba(173, 172, 172, 0.2),
      -4px -4px 18px rgba(162, 160, 160, 0.2);

    &-info {
      font-size: smaller;
      font-weight: bold;
      text-align: center;
    }
  }

  &-dynamic {
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
      font-size: small;
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
</style>
