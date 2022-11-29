<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n()

const props = defineProps({
    app_errors: {
        required: true,
        default: []
    },
    app_error_type: {
        required: false,
        default: ''
    }
})
</script>


<template>
    <div v-if="props.app_errors.length > 0"  id="app_error" class="mes e" :data-error="props.app_error_type">
        <div v-for="(error, i) in props.app_errors" :key="i">{{ t(error) }}</div>
    </div>
</template>


<style lang="scss">
#app_error {z-index: 1000;position: relative;}
</style>


<i18n>
ru:
    Network Error. Check your internet connection.: Ошибка сети. Проверьте подключение к интернету.
    Sorry, but there was a programming error on page. A notification has already been sent to technical support. Please try again in a few minutes.: Извините, но на странице возникла программная ошибка. В техническую поддержку уже отправлено уведомление. Пожалуйста, попробуйте снова через несколько минут.
    Data is not found: Данные не найдены
</i18n>