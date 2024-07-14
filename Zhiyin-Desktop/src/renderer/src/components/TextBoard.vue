<template>
    <div class="chat-container">
        <div class="header">
            <img src="../assets/title.png" id="title">
            <span>· 文本模式</span>
            <button class="close" @click="close">
                <img src="../assets/hide.svg">
            </button>
        </div>
        <div class="chat-box" id="chat-box">
            <div v-for="message in messages" :key="message.id" :class="message.type">
                {{ message.text }}
            </div>
        </div>
        <div class="input-container">
            <div class="container">
                <input @click="sendMessage" class="checkbox" type="checkbox" :disabled="isWaitingForBot">
                <div class="mainbox">
                    <div class="iconContainer">
                        <img src="../assets/search.svg">
                    </div>
                    <input v-model="userInput" id="user-input" class="search_input" placeholder="来输入内容吧~" type="text"
                        @keyup.enter="sendMessage" :disabled="isWaitingForBot">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/TextBoard.css';
</style>

<script setup>
import { ref } from 'vue';

let mainOn = false;
const chatBox = ref(null);
const userInput = ref('');
const messages = ref([]);
const isWaitingForBot = ref(false);

const close = () => {
    electron.ipcRenderer.invoke('ipc', {
        module: 'close',
        window: 'textWindow'
    })
}

const sendMessage = async () => {
    if (userInput.value.trim() !== '' && !isWaitingForBot.value) {
        // 获取用户输入的内容
        const userMessage = { id: Date.now(), text: userInput.value, type: 'user-message' };
        messages.value.push(userMessage);
        // 等待返回之前禁止输入新的内容
        isWaitingForBot.value = true;
        const inputValue = userInput.value;
        // 刷新用户输入
        userInput.value = '';
        try {
            const botResponse = await electron.ipcRenderer.invoke('text-input', inputValue);
            const botMessage = { id: Date.now() + 1, text: botResponse, type: 'bot-message' };
            messages.value.push(botMessage);
        } catch (error) {
            const errorMessage = { id: Date.now() + 1, text: '发生错误，请稍后重试。', type: 'bot-message' };
            messages.value.push(errorMessage);
        } finally {
            isWaitingForBot.value = false;
        }
    }
}
</script>
