<template>
    <div class="container">
        <div class="checkbox">
            <input id="checkbox_input" class="checkbox__input" type="checkbox" @change="changeMain">
            <label for="checkbox_input" class="checkbox__label">
                <span class="checkbox__custom"></span>
            </label>
        </div>
        <img src="../assets/title.png" id="title">
        <button class="close" @click="close">╳</button>
    </div>


</template>

<style scoped>
@import '../assets/Main.css';
</style>

<script setup>
let mainOn = false;

const changeMain = () => {
    if (!mainOn) {
        // console.log('启动主程序')
        electron.ipcRenderer.invoke('ipc', {
            module: 'mainON',
            window: 'mainWindow'
        })
        mainOn = true
    } else {
        // console.log('关闭主程序')
        electron.ipcRenderer.invoke('ipc', {
            module: 'mainOFF',
            window: 'mainWindow'
        })
        mainOn = false
    }
}

const close = () => {
    electron.ipcRenderer.invoke('ipc', {
        module: 'close',
        window: 'mainWindow'
    })
}
</script>