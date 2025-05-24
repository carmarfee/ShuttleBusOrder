<template>
<div class="u-page__item">
    <div class="card card-rule">
        <div class="card-rule-title">
            预约规则
        </div>
        <div class="card-rule-info">
            <p>1. 每位学生每月可预约班车次数为2次，超过2次将无法预约。</p>
            <p>2. 每次预约需提前24小时进行，预约时间截止到班车发车前1小时。</p>
            <p>3. 预约成功后，如需取消，请在发车前1小时内取消，否则将视为违约。</p>
        </div>
    </div>
    <tabbar></tabbar>
</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import tabbar from "@/components/tabbar.vue";


//-------------------------------分割线--------------------------------

</script>

<style lang="scss" scoped>
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

.card {
    &-rule {
        margin: 20rpx;
        height: 250rpx;
        background-color: #88aaeb4b;
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
}
</style>
