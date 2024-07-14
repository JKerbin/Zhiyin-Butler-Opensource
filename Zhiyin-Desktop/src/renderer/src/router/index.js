import { createRouter, createWebHashHistory } from "vue-router"
import Start from '../views/Start.vue'
import Activation from '../views/Activation.vue'
import Main from '../views/Main.vue'
import Setting from '../views/Setting.vue'
import Text from '../views/Text.vue'

export default createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: "/", component: Start },
        { path: "/activation", component: Activation },
        { path: "/main", component: Main },
        { path: "/setting", component: Setting },
        { path: "/text", component: Text },
    ]
})