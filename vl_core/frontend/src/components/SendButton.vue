<script setup>
import PulseLoader from "vue-spinner/src/PulseLoader.vue";

const props = defineProps({
    loading: {
        type: Boolean,
        default: true
    },
    title: {
        type: String,
        default: 'Send'
    },
})

const emit = defineEmits(['click'])
</script>


<template>
    <div class="button_wr">
        <div class="button" @click="emit('click')">{{ props.title }} <PulseLoader :loading="props.loading" size="8px" color="#fff" /></div>
    </div>
</template>


<style lang="scss">
.button .v-spinner {display: inline-block;vertical-align: middle;margin-left: 6px;}
</style>