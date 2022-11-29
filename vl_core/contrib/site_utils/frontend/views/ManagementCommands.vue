<script setup>
import {useI18n} from "vue-i18n";

const {t} = useI18n()

import RingLoader from "vue-spinner/src/RingLoader.vue";

import state from "../../../../frontend/src/state"

const {add_app_errors, urls} = state

import {computed, ref} from "vue";
import axios from "axios";

import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';

import SendButton from '../../../../frontend/src/components/SendButton.vue';


const commands = ref([])
const command = ref('')
const params = ref('')

const result = ref({})
const sending = ref(false)
const init_running = ref(false)

const btn_title = computed(() => {
    if (sending.value) return t('Running')

    return t('Run')
})

const options = {
    headers: {
        'Cache-Control': 'no-cache',
        'X-CSRFToken': window.app_config.csrf_token
    }
};

const run_command = () => {
    if (!sending.value) {
        sending.value = true

        const data = new URLSearchParams();
        data.append('command', command.value);
        data.append('params', params.value);

        axios.post(urls.value.run_command, data, options)
            .then(response => {
                if (response.data.status === 'fail') add_app_errors(t(response.data.message))

                result.value.content = response.data.result
                result.value.message = response.data.message
                result.value.elapsed_time = response.data.elapsed_time
                result.value.shown = true
            })
            .catch(error => {
                add_app_errors('', error)
            })
            .finally(() => {
                sending.value = false
            })
    }
}

const command_obj = computed(() => {
    return commands.value[command.value] || {}
})

const command_options = computed(() => {
    let data = []

    for (let key in commands.value) data.push({id: key, label: commands.value[key].command, desc: commands.value[key].option_help})

    data.sort(function(a, b){
        let v_a = a.label, v_b = b.label

        if (v_a < v_b) return -1
        if (v_a > v_b) return 1
        return 0
    })

    return data
})

const init = () => {
    init_running.value = true
    axios.get(urls.value.run_command)
        .then(response => {
            if (response.data.status === 'fail') add_app_error(t(response.data.message))

            commands.value = response.data.commands
            command.value = response.data.selected_command
        })
        .catch(error => {
            add_app_error('', error)
        })
        .finally(() => {
            init_running.value = false
        })
}

init()
</script>


<template>
    <h1>{{ t('Management commands') }}</h1>

    <p class="mes w"><strong>{{ t('Attention') }}:</strong>
        {{ t('execution of some commands may disrupt the operation of the site. Make sure you understand the output of the command.') }}</p>


    <div class="form">
        <div class="row">
            <!--suppress XmlInvalidId -->
            <label for="id_command">{{ t('Command') }}:</label>

            <div class="select_wr">
                <vSelect v-model="command" label="label" :options="command_options" :reduce="command => command.id" >
                    <template #option="{ label, id, desc }">
                        <div class="option_desc">
                            <h3 style="margin: 0">{{ label }}</h3>
                            <em>{{ desc }}</em>
                        </div>
                    </template>
                </vSelect>
            </div>
        </div>

    </div>
    <RingLoader :loading="init_running" size="30px"/>

    <div v-if="command_obj">
        <h2>{{ t('Selected Command') }}: <strong>{{ command_obj.command }}</strong></h2>
        <p>{{ command_obj.option_help }}</p>

        <div class="form">
            <div class="row">
                <label for="id_params">{{ t('Parameters') }}:</label>
                <input type="text" v-model="params" id="id_params" :placeholder="t('Parameters')">
            </div>

            <div class="row row_reverse">
                <SendButton :title="btn_title" :loading="sending" @click="run_command"/>
            </div>
        </div>

        <template v-if="result.shown">
            <p class="mes s">{{ result.message }}. {{ t('Elapsed time') }}: {{ result.elapsed_time }}</p>

            <div class="panel i">
                <div class="t">{{ t('Log') }}</div>
                <div class="c">
                    <div v-if="result.content" v-html="result.content"></div>
                    <p v-else>{{ t('Empty') }}</p>
                </div>
            </div>

        </template>

        <h2>{{ t('Full description') }}</h2>
        <pre v-html="command_obj.desc"></pre>
    </div>
</template>


<style lang="scss">
@import "../../../../static/vl_core/panel.scss";

$input_height: 30px;

#app {
    .form {max-width: 600px;margin-top: 20px;margin-bottom: 20px;}
    .row {
        margin-bottom: 10px;display: flex;align-items: center;
        label {margin-right: 30px;text-align: right;display: inline-block;width: 200px;}
        input {height: $input_height;line-height: $input_height;padding: 5px 6px;}
        input, .select_wr {box-sizing: border-box;flex-grow: 1;}
        &.row_reverse {flex-direction: row-reverse;}
        .button {padding-left: 30px;padding-right: 30px;}
    }
    pre {word-wrap: break-word;white-space: pre-wrap;line-height: 1.9em;}
    p {margin: .2em 0;}

    .select2-container .select2-selection--single {height: $input_height;}

    .v-ring {margin: 0 auto;}

    .vs__dropdown-option{
        white-space: pre-wrap;
        h3 {color: inherit;}
    }
    .option_desc {
        padding-top: 4px;padding-bottom: 4px;
        em {word-wrap: break-word;}
    }
}
</style>


<i18n>
ru:
    Management commands: Команды сайта
    Attention: Внимание
    execution of some commands may disrupt the operation of the site. Make sure you understand the output of the command.: выполнение
        некоторых команд может нарушить работу сайта. Убедитесь, что вы понимаете результат
        выполнения команды.
    Log: Лог
    Run: Выполнить
    Running: Выполнение
    Parameters: Параметры
    Command: Команда
    Selected Command: Выбранная команда
    Full description: Полное описание
    Elapsed time: Затраченное время
</i18n>