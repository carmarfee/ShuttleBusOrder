// utils/request.ts

// 请求配置接口
interface RequestConfig {
    url: string;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    data?: any;
    header?: Record<string, string>;
    timeout?: number;
}

// 响应数据接口
interface ResponseData<T = any> {
    code: number;
    message: string;
    data: T;
}

// 请求类
class Request {
    private baseURL: string = '';
    private timeout: number = 10000;
    private header: Record<string, string> = {
        'Content-Type': 'application/json;charset=UTF-8'
    };

    constructor(config?: {
        baseURL?: string;
        timeout?: number;
        header?: Record<string, string>;
    }) {
        if (config) {
            this.baseURL = config.baseURL || this.baseURL;
            this.timeout = config.timeout || this.timeout;
            this.header = { ...this.header, ...config.header };
        }
    }

    // 处理URL
    private getUrl(url: string): string {
        if (url.startsWith('http://') || url.startsWith('https://')) {
            return url;
        }
        return this.baseURL + url;
    }

    // 构建查询字符串
    private buildQuery(params: Record<string, any>): string {
        const query = Object.entries(params)
            .filter(([_, value]) => value !== null && value !== undefined)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
            .join('&');
        return query;
    }

    // 主请求方法
    private async request<T = any>(config: RequestConfig): Promise<ResponseData<T>> {
        // 处理请求头
        const headers = { ...this.header };
        const token = uni.getStorageSync('token');
        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const requestConfig = {
            url: this.getUrl(config.url),
            method: config.method || 'GET',
            data: config.data,
            header: { ...headers, ...config.header },
            timeout: config.timeout || this.timeout
        };

        // 打印请求信息（调试用）
        console.log('📤 请求发送:', {
            url: requestConfig.url,
            method: requestConfig.method,
            data: requestConfig.data,
            header: requestConfig.header
        });

        // 显示加载提示
        uni.showLoading({ title: '加载中...', mask: true });

        try {
            const response = await new Promise<any>((resolve, reject) => {
                uni.request({
                    ...requestConfig,
                    success: (res) => {
                        console.log('响应接收:', res);
                        resolve(res);
                    },
                    fail: (err) => {
                        console.error('请求失败:', err);
                        reject(err);
                    }
                });
            });

            // 隐藏加载提示
            uni.hideLoading();

            // 检查HTTP状态码
            if (response.statusCode >= 200 && response.statusCode < 300) {
                const data = response.data;

                // 检查是否是预期的数据格式
                if (typeof data === 'object' && data !== null) {
                    // 如果有code字段，按业务逻辑处理
                    if ('code' in data) {
                        const responseData = data as ResponseData<T>;

                        if (responseData.code === 0) {
                            return responseData;
                        } else if (responseData.code === 401) {
                            // token过期
                            uni.removeStorageSync('token');
                            uni.reLaunch({ url: '/pages/login/login' });
                            throw new Error('登录已过期');
                        } else {
                            // 业务错误
                            const errorMsg = responseData.message || '请求失败';
                            uni.showToast({ title: errorMsg, icon: 'none' });
                            throw new Error(errorMsg);
                        }
                    } else {
                        // 没有code字段，直接返回数据（兼容不同API格式）
                        return {
                            code: 0,
                            message: 'success',
                            data: data as T
                        } as ResponseData<T>;
                    }
                } else {
                    // 响应数据格式异常
                    throw new Error('响应数据格式错误');
                }
            } else {
                throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || '请求失败'}`);
            }

        } catch (error: any) {
            // 隐藏加载提示
            uni.hideLoading();

            let errorMessage = '网络错误';

            // 解析错误类型
            if (error.errMsg) {
                // uni.request的网络错误
                if (error.errMsg.includes('timeout')) {
                    errorMessage = '请求超时';
                } else if (error.errMsg.includes('fail')) {
                    errorMessage = '网络连接失败';
                } else {
                    errorMessage = '网络错误';
                }
                console.error('网络错误:', error.errMsg);
            } else if (error.message) {
                // 业务逻辑错误
                errorMessage = error.message;
                console.error('业务错误:', error.message);
            } else {
                console.error('未知错误:', error);
            }

            // 显示错误提示
            uni.showToast({
                title: errorMessage,
                icon: 'none',
                duration: 2000
            });

            throw new Error(errorMessage);
        }
    }

    // GET 请求
    public get<T = any>(url: string, params?: any): Promise<ResponseData<T>> {
        let requestUrl = url;
        if (params) {
            const query = this.buildQuery(params);
            requestUrl = query ? `${url}?${query}` : url;
        }

        return this.request<T>({ url: requestUrl, method: 'GET' });
    }

    // POST 请求
    public post<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
        return this.request<T>({ url, method: 'POST', data });
    }

    // PUT 请求
    public put<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
        return this.request<T>({ url, method: 'PUT', data });
    }

    // DELETE 请求
    public delete<T = any>(url: string): Promise<ResponseData<T>> {
        return this.request<T>({ url, method: 'DELETE' });
    }
}

// 创建请求实例
const request = new Request({
    baseURL: 'http://127.0.0.1:4523/m1/6669867-6378754-default',
    timeout: 10000
});

export default request;
export type { RequestConfig, ResponseData };