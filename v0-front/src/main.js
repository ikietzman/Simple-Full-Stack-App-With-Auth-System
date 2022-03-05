import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/normalize.css'
import './assets/styles.scss'

createApp(App).use(router).mount('#app')
