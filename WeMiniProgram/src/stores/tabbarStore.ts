import { defineStore } from 'pinia';

export const useTabbarStore = defineStore('tabbar', {
    state: () => {
        return {
            // 当前选中的tabbar索引
            activeTab: 0
        };
    },
    getters: {
        getActiveTab(state) { return state.activeTab }
    },
    actions: {
        setActiveTab(index: number) {
            this.activeTab = index;
        },
        resetActiveTab() {
            this.activeTab = 0;
        }
    }
})