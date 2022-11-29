<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n()

const props = defineProps({
    title: {
        type: String,
    },
    files: {
        type: Array,
    },
})
</script>


<template>
    <h3>{{ props.title }}</h3>
    <template v-for="(item, i) in props.files" :key="i">
        <p v-if="item.can_download"><a target="_blank" :href="item.url" v-text="item.filename + ' (' + item.size_str + ')'"></a></p>
        <p v-else><span v-text="item.filename"></span> ({{ t('in process') }})</p>
    </template>
    <p v-if="props.files.length === 0">{{ t('No backup has been created yet') }}</p>
</template>


<style lang="scss">

</style>


<i18n>
ru:
    in process: в процессе создания
    No backup has been created yet: Резервная копия ещё не была создана
</i18n>