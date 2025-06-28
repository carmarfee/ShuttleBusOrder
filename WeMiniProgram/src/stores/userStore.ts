import { defineStore } from 'pinia';
import { computed } from 'vue'
import request from '@/utils/request';


export const useUserStore = defineStore('user', () => {
    const state = {
        // 用户基本信息
        token: uni.getStorageSync('token'),
        userInfo: {
            id: '',
            name: '',
            role: '',
            department: '',
        }
    };
    const getters = {
        isGuest: computed(() => {
            return state.userInfo.role === 'guest';
        }),
        //状态管理
        isLogin: computed(() => { return !!state.token }),
    };

    const actions = {
        LoginIn: async (form: { id: string; password: string, role: string }) => {
            console.log('Login', form);
            // 发送请求
            const res = await request.post('/api/auth/login', {
                id: form.id,
                password: form.password,
                role: form.role
            });
            console.log('登录结果', res);
            // 模拟登录
            state.userInfo = res.data.userInfo;
            state.token = res.data.token;
            // 存储用户信息
            uni.setStorageSync('userInfo', res.data.userInfo);
            // 存储token
            uni.setStorageSync('token', res.data.token);

            uni.switchTab({ url: '/pages/home/home' });
            console.log('登录成功', state.userInfo);
        },
        LoginOut: () => {
            // 清除token
            state.userInfo = {
                id: '',
                name: '',
                role: '',
                department: '',
            };
            state.token = '';
            // 清除用户信息和token
            uni.removeStorageSync('userInfo');
            uni.removeStorageSync('token');
        },
    };
    return { state, getters, actions };
});