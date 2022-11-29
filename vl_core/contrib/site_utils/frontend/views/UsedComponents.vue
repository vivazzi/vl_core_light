<script setup>
import {ref} from "vue";

import {useI18n} from "vue-i18n";
const {t} = useI18n()

import RingLoader from "vue-spinner/src/RingLoader.vue";
import axios from "axios";

import state from "../../../../frontend/src/state"
const {add_app_error, urls} = state


const components = ref([])
const unused_components = ref([])

axios.get(urls.value.get_used_components)
    .then(response => {
        if (response.data.status === 'fail') add_app_error(t(response.data.message))

        components.value = response.data.components
        unused_components.value = response.data.unused_components
    })
    .catch(error => {
        add_app_error(error)
    })
</script>


<template>
    <h1>{{ t('Used components') }}</h1>

    <template v-if="components.length > 0">
        <template v-for="(component, i) in components" :key="i">
            <h2>{{ component.title }}</h2>

            <p v-for="(page, j) in component.pages" :key="j">
                <a :href="page.url" v-if="page.url">{{ page.title }}</a>
                <template v-else>{{ page.title }}</template>
            </p>
        </template>

        <h2>{{ t('No components on pages') }}</h2>
        <p v-for="(component, i) in unused_components" :key="i">{{ component }}</p>

    </template>
    <RingLoader v-else size="30px" />
</template>


<i18n>
ru:
    Used components: Используемые компоненты
    No components on pages: Нет компонентов на страницах
</i18n>