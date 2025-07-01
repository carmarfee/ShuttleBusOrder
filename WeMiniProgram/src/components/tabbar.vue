<template>
<div class="u-page__item">
    <up-tabbar :value="activeTab" :fixed="true" :safeAreaInsetBottom="true" :placeholder="false">
        <up-tabbar-item v-for="(item, index) in tabbarList" :key="index" :text="item.name" @click="goToNext(item)"
            :icon=item.icon>
        </up-tabbar-item>
    </up-tabbar>
</div>
</template>

<script setup lang="ts">
import { ref} from "vue";
import { useUserStore } from "@/stores/userStore";
import { useTabbarStore } from "@/stores/tabbarStore";
import { storeToRefs } from "pinia";
import { onLoad } from "@dcloudio/uni-app";

const tabbarStore = useTabbarStore();
const { activeTab } = storeToRefs(tabbarStore)
const tabbarList = ref([
    {
        index: 0,
        name: "首页",
        url: "/pages/home/home",
        icon: "home1"
    },
    {
        index: 1,
        name: "我的",
        url: "/pages/user/user",
        icon: "wode",
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

onLoad(() => {
    uni.hideTabBar();
});
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

.u-tabbar__content {
    height: 60px !important;
}

.u-tabbar-item {
    &__text {
        font-size: 10px !important;
        color: #4e5161;
    }
}
</style>
