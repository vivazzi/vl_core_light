<script setup>
import {useI18n} from 'vue-i18n'
const {t} = useI18n()

import state from "../../../../frontend/src/state"
const {add_app_errors, urls, config} = state

import axios from 'axios';
import {ref, computed} from 'vue';

import SendButton from '../../../../frontend/src/components/SendButton.vue';


const status = ref('')
const sending = ref(false)

const btn_title = computed(() => {
    if (sending.value) return t('Sending...')

    return t('Send')
})

const send_test_letter = () => {
    if (!sending.value) {
        sending.value = true
        axios.get(urls.value.send_test_letter)
            .then(response => {
                if (response.data.status === 'fail') add_app_errors(t(response.data.message))

                status.value = response.data.status
            })
            .catch(error => {
                add_app_errors('', error)
            })
            .finally(() => {
                sending.value = false
            })
    }
}
</script>


<template>
    <h1>{{ t('Email testing') }}</h1>

    <p>{{ t('Designed to check the efficiency of receiving letters from the site. Test email will be sent to') }} <strong>{{ config.testing_email }}</strong></p>

    <SendButton :title="btn_title" :loading="sending" @click="send_test_letter" />

    <div class="mes s" v-if="status === 'ok'">{{ t('The letter was sent') }}</div>
</template>


<i18n>
ru:
    Email testing: Тестирование отправки письма
    Designed to check the efficiency of receiving letters from the site. Test email will be sent to: Предназначено для проверки работоспособности приёма писем с сайта. Тестовое письмо будет отправлено на
    Send: Отправить
    Sending...: Отправляется...
    The letter was sent: Письмо было отправлено
</i18n>