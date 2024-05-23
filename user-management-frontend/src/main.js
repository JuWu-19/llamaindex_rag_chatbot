// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import axios from 'axios';

// Set withCredentials globally
axios.defaults.withCredentials = true;

const app = createApp(App);
app.use(router);
app.mount('#app');
