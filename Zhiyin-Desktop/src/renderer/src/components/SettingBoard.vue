<template>
    <div class="card" id="userboard">
        <div class="shape" v-for="n in 4" :key="n" :id="'shape' + n"></div>
        <span id="version">version-beta-0.3.0<br>developed by Jason JKerbin</span>
        <div id="header">设置</div>
        <div id="header1">语音模式</div>
        <div class="container">
            <form>
                <label>
                    <input type="radio" name="radio" checked="" @click="smLocal">
                    <span>本地（Win语音接口）</span>
                </label>
                <label>
                    <input type="radio" name="radio" @click="smNormal">
                    <span>普通（百度语音接口）</span>
                </label>
                <label>
                    <input type="radio" name="radio" @click="smHD">
                    <span>增强（开智语音接口）</span>
                </label>
            </form>
        </div>
        <div id="header2">收音阈值</div>
        <div class="slider">
            <input type="range" v-model="sliderValue" min="100" max="1000" />
            <div>{{ sliderValue }}</div>
        </div>
        <button class="cta" @click="confirmValue">
            <span>应用设置</span>
            <svg width="15px" height="10px" viewBox="0 0 13 10">
                <path d="M1,5 L11,5"></path>
                <polyline points="8 1 12 5 8 9"></polyline>
            </svg>
        </button>
    </div>

</template>

<style scoped>
@import '../assets/SettingBoard.css';
</style>

<script setup>
import { ref } from 'vue';
const sliderValue = ref(500);
let serverMod = 'local';
// 确定按钮点击处理函数
const confirmValue = () => {
    electron.ipcRenderer.invoke('ipc', {
        module: 'setconfig',
        audioThreshold: sliderValue.value.toString(),
        serverMod: serverMod,
    })
}

// 选择语音服务模式
const smLocal = () => {
    serverMod = 'local'
}
const smNormal = () => {
    serverMod = 'normal'
}
const smHD = () => {
    serverMod = 'hd'
}
</script>