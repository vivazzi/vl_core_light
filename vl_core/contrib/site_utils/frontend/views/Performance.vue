<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n()

import state from "../../../../frontend/src/state"
const {add_app_error, urls} = state

import {computed, ref} from "vue";
import axios from "axios";

import SendButton from '../../../../frontend/src/components/SendButton.vue';


const results = ref({})
const sending = ref(false)

const btn_title = computed(() => {
    if (sending.value) return t('Processing')

    return t('Speed up')
})

const speed_up = () => {
    if (!sending.value) {
        sending.value = true
        axios.get(urls.value.speed_up)
            .then(response => {
                if (response.data.status === 'fail') add_app_error(t(response.data.message))

                results.value = response.data.results
                results.value.shown = true
            })
            .catch(error => {
                add_app_error('', error)
            })
            .finally(() => {
                sending.value = false
            })
    }
}
</script>


<template>
    <h1>{{ t('Performance') }}</h1>
    <h2>{{ t('Speed up the site') }}</h2>
    <p>{{ t('During site administration, unnecessary information may accumulate in the database when using the "Text" component and other system functions.') }}</p>

    <div class="mes i">{{ t('At the moment, the site acceleration function only removes unnecessary non-breaking spaces. The rest of the functions are optimized, and the excess temporary information is removed automatically.') }}</div>

    <SendButton :title="btn_title" :loading="sending" @click="speed_up" />

    <template v-if="results.shown">
        <h3 >{{ t('Acceleration results') }}</h3>
        <template v-if="results.accelerated">
            <template v-if="results.free_bytes">
                <h3>{{ t('Useless spaces') }}</h3>
                <p>{{ t('Removed unnecessary non-breaking spaces, which improved the display of text and free up') }} <strong>{{ results.free_bytes }}</strong>.</p>
            </template>
        </template>
        <p v-else>{{ t('The site has already been cleared of unnecessary information.') }}</p>
    </template>
</template>


<i18n>
ru:
    Performance: Производительность
    Speed up the site: Ускорение работы сайта
    ? During site administration, unnecessary information may accumulate in the database
        when using the "Text" component and other system functions.
    : Во время администрирования сайта в базе данных может накапливаться ненужная информация
        при использовании компонента "Текст" и других функциях системы.
    ? At the moment, the site acceleration function only removes unnecessary non-breaking
        spaces. The rest of the functions are optimized, and the excess temporary information
        is removed automatically.
    : На данный момент функция ускорения сайта только убирает лишние неразрывные пробелы.
        Остальные функции оптимизированы, а лишняя временная информация убирается в автоматическом
        режиме.
    Speed up: Ускорить
    Processing: Обработка
    Acceleration results: Результаты ускорения
    Useless spaces: Лишние пробелы
    Removed unnecessary non-breaking spaces, which improved the display of text and free up: Убраны
        лишние неразрывные пробелы, что позволило улучшить отображение текста и освободить
    The site has already been cleared of unnecessary information.: Сайт ранее уже был
        очищен от лишней информации.
</i18n>