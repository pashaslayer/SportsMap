import "bootstrap/dist/css/bootstrap.css"
import { createApp } from 'vue'
import App from './App.vue'

import "bootstrap/dist/js/bootstrap.js"
import '@fortawesome/fontawesome-free/js/all'

// Vee - validate
// import { defineRule } from 'vee-validate';
import OpenLayersMap from "vue3-openlayers";

import router from './router'

const options = {
    debug: true,
  };


const app = createApp(App);
app.use(OpenLayersMap, options);

// vee - validate


app.use(router);
app.mount("#app");