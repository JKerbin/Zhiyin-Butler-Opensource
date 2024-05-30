<template>
    <div class="window">
        <div class="card" id="userpad">
            <div id="shadow"></div>
        </div>
        <div class="card" id="background">
            <img src="../assets/triangle.svg" class="triangle" v-for="n in 4" :key="n" :id="'triangle' + n">
            <div class="shape" v-for="n in 4" :key="n" :id="'shape' + n"></div>
            <ActivationBoard />
            <button class="close" @click="close">╳</button>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/Common.css';
</style>

<script setup>
import ActivationBoard from '../components/ActivationBoard.vue'
const close = () => {
    electron.ipcRenderer.invoke('ipc', {
        module: 'close',
        window: 'activationWindow'
    })
}
</script>
