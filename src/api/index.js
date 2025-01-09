import axios from 'axios';

// 创建 Axios 实例
const api = axios.create({
  baseURL: 'http://192.168.0.107:8000', // API 基础地址
  timeout: 1000000, // 超时时间
});

// 添加请求拦截器
api.interceptors.request.use(
  (config) => {
    // 在请求发送之前做一些处理，比如添加 token
    console.log('请求拦截器:', config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('响应拦截器:', response);
    return response.data; // 直接返回数据
  },
  (error) => {
    console.error('响应错误:', error);
    return Promise.reject(error);
  }
);

export default api;
