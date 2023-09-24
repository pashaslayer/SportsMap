import "bootstrap/dist/css/bootstrap.css"
import { createApp } from 'vue'
import App from './App.vue'

import "bootstrap/dist/js/bootstrap.js"
import '@fortawesome/fontawesome-free/js/all'

// importing and registration route
import router from './router'

createApp(App).use(router).mount('#app')

