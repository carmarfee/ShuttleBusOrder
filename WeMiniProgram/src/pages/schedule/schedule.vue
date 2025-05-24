<template>
<div class="u-page__item">
    

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


</style>
