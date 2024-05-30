import { createRouter, createWebHashHistory } from "vue-router"
import Start from '../views/Start.vue'
import Activation from '../views/Activation.vue'
import Main from '../views/Main.vue'

export default createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: "/", component: Start },
        { path: "/activation", component: Activation },
        { path: "/main", component: Main }
    ]
})