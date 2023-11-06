import axios from 'axios'

const apiClient = axios.create({
    baseURL: `http://localhost:3000/api/v1`,
    headers: {
        'Content-type': 'application/json'
    }
})

apiClient.interceptors.request.use(function (config) {
    const username = localStorage.getItem('username')
    const password = localStorage.getItem('password')

    if (username && password) {
        config.auth = {
            username,
            password
        }
    }

    return config
})

export default apiClient
