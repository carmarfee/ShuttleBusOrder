import { defineStore } from 'pinia';
import { computed } from 'vue'

export const useUserStore = defineStore('user', () => {
    const state = {
        // 用户基本信息
        userInfo: {
            id: '',
            name: '',
            role: ''
        },
        token: uni.getStorageSync('token'),


    };
    const getters = {
        isGuest: computed(() => {
            return state.userInfo.role === 'guest';
        }),
        //状态管理
        isLogin: computed(() => { return !!state.token }),
    };

    const actions = {
        LoginIn: async (form: { id: string; password: string }) => {
            console.log('Login', form);
            // 发送请求
            const res = {
                userInfo: {
                    id: '123456',
                    name: '张三',
                    role: 'stu',
                },
                token: 'token'
            }
            // 模拟登录
            state.userInfo = res.userInfo;
            state.token = res.token;
            // 存储用户信息
            uni.setStorageSync('userInfo', res.userInfo);
            // 存储token
            uni.setStorageSync('token', res.token);

            uni.redirectTo({
                url: '../home/home'
            })
            console.log('登录成功', state.userInfo);
        },
        LoginOut: () => {
            // 清除token
            state.userInfo = {
                id: '',
                name: '',
                role: ''
            };
            state.token = '';
            // 清除用户信息和token
            uni.removeStorageSync('userInfo');
            uni.removeStorageSync('token');
        },
    };
    return { state, getters, actions };
});