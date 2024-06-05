<template>
    <div class="card" id="userboard">
        <div class="shape" v-for="n in 4" :key="n" :id="'shape' + n"></div>
        <img src="../assets/title.png" id="title">
        <!-- activation -->
        <div class="input-group">
            <input required="" type="text" autocomplete="off" class="input" id="activationInput"
                :disabled="isSubmitted">
            <label class="user-label">产品激活码</label>
            <button id="submit" @click="submit" :disabled="isSubmitted">立刻激活</button>
        </div>
    </div>
    <Loader v-if="isSubmitted" />
</template>

<style scoped>
@import '../assets/ActivationBoard.css';
</style>

<script setup>
import Loader from './Loader.vue'
import { ref } from 'vue';
const isSubmitted = ref(false);
const submit = () => {
    const activationInput = document.getElementById('activationInput').value;
    electron.ipcRenderer.invoke('ipc', {
        module: 'submit_invitation',
        invitation: activationInput
    });
    isSubmitted.value = true;
}
</script>
