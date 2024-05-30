<template>
    <div class="card" id="userboard">
        <div class="shape" v-for="n in 4" :key="n" :id="'shape' + n"></div>
        <img src="../assets/title.png" id="title">
        <!-- start -->
        <span class="welcome">- 智音 • 语音助手 -</span>
        <div id="letsbegin">
            <button id="begin" @click="begin">即刻体验</button>
        </div>
        <span id="version">version-beta-0.1.0<br>developed by Jason JKerbin</span>
    </div>
</template>

<style scoped>
@import '../assets/StartBoard.css';
</style>

<script setup>
const begin = () => {
    electron.ipcRenderer.invoke('ipc', {
        module: 'begin'
    })
}
</script>