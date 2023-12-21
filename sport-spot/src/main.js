import "bootstrap/dist/css/bootstrap.css"
import { createApp } from 'vue'
import App from './App.vue'

import "bootstrap/dist/js/bootstrap.js"
import '@fortawesome/fontawesome-free/js/all'

import OpenLayersMap from "vue3-openlayers";
import "vue3-openlayers/styles.css";

import router from './router'

const app = createApp(App);
app.use(OpenLayersMap /* options */);
app.use(router);
app.mount("#app");