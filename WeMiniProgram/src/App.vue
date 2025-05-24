<script lang="ts" setup>
import {
    onLaunch,
    onShow,
    onHide
} from "@dcloudio/uni-app";

onLaunch(() => {
    console.log("App Launch");
});
onShow(() => {
    console.log("App Show");
    uni.hideTabBar({
        animation: false
    })
});

onHide(() => {
    console.log("App Hide");
});

</script>

<style lang="scss">
@import "uview-plus/index.scss";
@import "./static/css/iconfont.css";

page {
    background-color: rgb(247, 247, 255);
}
</style>
