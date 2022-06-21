import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import 'font-awesome/css/font-awesome.min.css'
import './assets/css/mainStyle.css'
import './assets/css/bear_animation.css'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(ElementPlus)

app.mount('#app')
