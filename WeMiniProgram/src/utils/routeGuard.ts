import { useUserStore } from "@/stores/userStore";

const whitePageList = [
    '/pages/login/login',
    '/pages/error/error',
]

const loginPage = '/pages/login/login'

export const setupRouteGuard = () => {
    const methodList = ['navigateTo', 'redirectTo', 'reLaunch', 'switchTab']
    methodList.forEach(method => {
        uni.addInterceptor(method, {
            invoke(args) {
                console.log(args)
                const currentPage = getCurrentPages()[0].route;
                const targetPage = args.url.split('?')[0];
                const userStore = useUserStore();
                console.log('当前页面', currentPage)
                console.log('目标页面', targetPage)
                // 判断是否登录
                // if (!userStore.getters.isLogin && !whitePageList.includes(targetPage)) {
                //     console.log(userStore.state.token)
                //     // 如果没有登录，跳转到登录页
                //     args.url = loginPage;
                // }
                console.log('继续跳转')
                console.log('目标页面', args.url)
            },
            fail(e) {
                const currentPage = getCurrentPages();
                console.log('当前页面', currentPage)
                console.error(`为 ${method} 拦截器添加权限校验失败：`, e);
            }
        })
    })
}