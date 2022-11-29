<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n()

import state from "../../../frontend/src/state";
const {app_errors, urls, config} = state

import {computed, ref} from "vue";
import axios from "axios";

import Reference from "./Reference.vue";
import BackupModuleItem from "./BackupModuleItem.vue";
import RingLoader from "vue-spinner/src/RingLoader.vue";

import AppError from "../../../frontend/src/components/AppError.vue";


const app_loaded = ref(false)

const stat = ref({})
const has_stat = computed(() => Object.keys(stat).length !== 0)
const lockfile_content = ref('')

const backup_date = ref('')
const next_backup_date = ref('')
const next_backup_delta = ref('')

const current_elapsed_time = ref(0)

const support_url = '//vuspace.pro/my/support/'
const products_url = '//vuspace.pro/my/products/'

let given_size = 0
const given_size_str = ref('')
const free_size = ref(0)
const free_size_str = ref('')

const files = ref({db: [], media: [], code: [],})

let run_get_backups = false
let get_backups_timer = 0

let can_update_given_size = true

const get_backups = () => {
    run_get_backups = true
    axios.get(urls.value.get_backups)
        .then(response => {
            if (response.data.status === 'fail') console.log(response.data.mes)
            else {
                lockfile_content.value = response.data.lockfile_content

                stat.value = response.data.stat

                let date

                if (response.data.stat.backup_date === 0) {
                    backup_date.value = ''
                    next_backup_date.value = ''
                    next_backup_delta.value = ''
                }
                else {
                    date = new Date(response.data.stat.backup_date * 1000)
                    backup_date.value = date.toLocaleDateString() + ' ' + date.toLocaleTimeString()

                    date = new Date(response.data.next_backup_date * 1000)
                    next_backup_date.value = date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
                    next_backup_delta.value = response.data.next_backup_delta
                }

                current_elapsed_time.value = response.data.current_elapsed_time

                // group files
                let group
                let _files = {db: [], media: [], code: []}
                for (let item in response.data.stat.sizes.backups.files) {
                    if (item.startsWith('db')) group = 'db'
                    else if (item.startsWith('media')) group = 'media'
                    else group = 'code'

                    let _item = response.data.stat.sizes.backups.files[item]
                    _item['filename'] = item

                    _files[group].push(_item)
                }

                let groups = ['db', 'media', 'code']
                for (let index in groups) {
                    _files[groups[index]].sort((a, b) => {
                        let name_A = a.created_date, name_B = b.created_date
                        if (name_A < name_B) return -1
                        if (name_A > name_B) return 1
                        return 0
                    }).reverse()
                }

                files.value = _files

                if (can_update_given_size && urls.value.get_given_size !== '' && stat.value.sizes.total !== undefined) {
                    axios.get(urls.value.get_given_size)
                        .then(response => {
                            if (response.data.status === 'fail') console.log(response.data.mes)
                            else {
                                given_size = response.data.size
                                given_size_str.value = format_bytes(given_size)
                                free_size.value = given_size - stat.value.sizes.total
                                free_size_str.value = format_bytes(free_size.value)
                            }
                        })
                        .catch(error => {
                            can_update_given_size = false
                            console.log(error)
                        })
                }

            }
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            app_loaded.value = true
            if (run_get_backups) {
                let timeout = (lockfile_content.value === '') ? 10 : 3  // for convenience, check more often if a backup is created

                get_backups_timer = setTimeout(() => {
                    get_backups()
                }, timeout * 1000)
            }
        })
}

const do_backup = () => {
    axios.get(urls.value.backup)
        .then(response => {
            if (response.data.status === 'fail') console.log(response.data.mes)
            else {
                lockfile_content.value = response.data.lockfile_content
            }
        })
        .catch(error => {
            console.log(error)
        })
}

const format_bytes = bytes => {
    let i = -1
    let byte_units = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    do {
        bytes = bytes / 1024
        i++
    } while (bytes >= 1024)

    return Math.max(bytes, 0).toFixed(1) + ' ' + byte_units[i]
}

const get_title = key => {
    let data = {
        db: t('Databases'),
        media: t('Uploaded files'),
        code: t('Site code'),
    }
    return data[key]
}

const init = () => {
    get_backups()

    // check on active page
    setInterval(() => {
        if (document.hidden){
            if (run_get_backups) {
                run_get_backups = false
                clearTimeout(get_backups_timer)
            }
        }
        else {
            if (!run_get_backups) get_backups()
        }
    }, 1000)
}

init()
</script>


<!--suppress ALL -->
<template>
    <AppError :app_errors="app_errors" />

    <RingLoader :loading="!app_loaded" size="30px" />

    <template v-if="app_loaded">
        <div class="cols">
            <div class="col">
                <h2>{{ t('Site data size') }}</h2>
                <table v-if="has_stat && stat.sizes.total_str">
                    <tbody>
                    <tr><td>{{ t('DB') }}</td><td>{{ stat.sizes.db_str }}</td></tr>
                    <tr><td>{{ t('Uploaded files') }}</td><td>{{ stat.sizes.media_str }}</td></tr>
                    <tr><td>{{ t('Site code') }}</td><td>{{ stat.sizes.code_str }}</td></tr>
                    <tr><td>{{ t('Backups') }}</td><td>{{ stat.sizes.backups.total_str }}</td></tr>
                    <tr>
                        <td><strong>{{ t('Full size of site data') }}</strong></td>
                        <td>
                            <strong>{{ stat.sizes.total_str }}</strong>&nbsp;
                            <template v-if="given_size_str">
                                {{ t('from') }} {{ given_size_str }}<br>

                                <span v-if="free_size >= 0" class="green">{{ t('Left') }} {{ free_size_str }}</span>
                                <span v-else>{{ t('Exceeded by') }} {{ free_size_str }}</span>

                                (<a target="_blank" :href="products_url">{{ t('change') }}</a>)
                            </template>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <p v-else>
                    {{ t('Not defined at this time.') }}<br/>{{ t('Statistics will be calculated after the data is backed up.') }}
                </p>
            </div>
            <div class="col">
                <h2>{{ t('Creating archives') }}</h2>

                <table>
                    <tbody>
                    <tr><td>{{ t('Automatic creation of archives is performed every') }}</td><td>{{ config.backup_interval }} (<a target="_blank" :href="products_url">{{ t('change') }}</a>)</td></tr>
                    <tr v-if="stat.backup_date_str"><td>{{ t('Date of the last backup creation') }}</td><td>{{ backup_date }} ({{ t('elapsed time') }} {{ stat.elapsed_time_str }})</td></tr>
                    <tr>
                        <td>{{ t('Next automatic backup creation') }}</td>
                        <td v-if="next_backup_date">{{ next_backup_date }} ({{ t('in') }} {{ next_backup_delta }})</td>
                        <td v-else>{{ t('In less than a minute') }}</td>
                    </tr>
                    <tr><td>{{ t('Acceptable storage of database backups') }}</td><td>{{ config.backup_db_count }} (<a target="_blank" :href="products_url">{{ t('change') }}</a>)</td></tr>
                    <tr><td>{{ t('Acceptable storage of uploaded files') }}</td><td>{{ config.backup_media_count }} (<a target="_blank" :href="products_url">{{ t('change') }}</a>)</td></tr>
                    </tbody>
                </table>
            </div>
        </div>


        <div class="mes i">{{ t('Be sure to download site backups from time to time - this way you will protect your data from loss in case of force majeure.') }}</div>

        <p v-if="lockfile_content !== ''" class="mes w">
            <template v-if="current_elapsed_time === ''">{{ t('The task "Create backups" is queued and will be launched within a minute.') }}</template>
            <template v-else>
                {{ t('Attention! Backups are currently being made. This process can take a long time. Wait until the process is complete to download the current backups.') }}<br>
                {{ t('Current elapsed time') }}: {{ current_elapsed_time }}>
                <template v-if="stat.elapsed_time_str"> {{ t('The previous backup was created for') }} {{ stat.elapsed_time_str }}</template>
            </template>
        </p>

        <div v-if="lockfile_content === ''">
            <p>{{ t('You can update your site data backups yourself to download the most current version of the data.') }}<br/><br/></p>
            <p><span class="button" @click="do_backup">{{ t('Create backups') }}</span></p>
        </div>

        <h2>{{ t('Download backups') }}</h2>

        <div class="backup_modules">
            <BackupModuleItem v-for="(items, key, i) in files" :key="i" :files="items" :title="get_title(key)"></BackupModuleItem>
        </div>
    </template>

    <Reference :products_url="products_url" :support_url="support_url"></Reference>
</template>


<style lang="scss">
@import "../../../static/vl_core/admin_styles";
@import "../../../static/vl_core/mes";

#app {
    a.button {padding: 10px;}

    .item {
        margin: 20px 0 40px;

        p {margin: 10px 0;padding: 0;}
    }

    table {
        margin-bottom: 20px;

        td, th {padding: 10px;font-size: 14px;line-height: 1.3em;}

        tr td:first-child {text-align: right;}
    }

    .green {color: #007600;}
    .red {color: #d02d22;}

    .cols {
        display: flex;

        .col {
            margin: 20px 30px;

            h2:first-child, h3:first-child {margin-top: 0;}

            &:first-child {margin-left: 0;}
            &:last-child {margin-right: 0;}
        }
    }

    @media (max-width: 767px) {
        .module {padding: 0!important;}
        .cols {
            flex-direction: column;
            .col {margin-left: 0;margin-right: 0;}
        }
    }
}

p {line-height: 1.5;}
</style>


<i18n>
ru:
    Site data size: Размер данных сайта
    DB: БД
    Uploaded files: Загруженные файлы
    Site code: Код сайта
    Backups: Резервные копии
    Full size of site data: Полный размер данных сайта
    from: из
    Left: Осталось
    Exceeded by: Превышено на
    change: изменить
    Not defined at this time.: На данный момент не определено.
    Statistics will be calculated after the data is backed up.: Статистика будет подсчитана после создания резервной копии данных.
    Creating archives: Создание архивов
    Automatic creation of archives is performed every: Автоматическое создание архивов производится каждые
    Date of the last backup creation: Дата последнего создания бекапа
    elapsed time: затраченное время
    Next automatic backup creation: Следующее автоматическое создание бекапа
    in: через
    In less than a minute: Менее чем через минуту
    Acceptable storage of database backups: Допустимое хранение резервных копий базы данных
    Acceptable storage of uploaded files: Допустимое хранение резервных копий загруженных файлов
    Be sure to download site backups from time to time - this way you will protect your data from loss in case of force majeure.: Обязательно
        время от времени скачивайте резервные копии сайтов - так вы защитите свои данные
        от потери в форс-мажорных случаях.
    The task "Create backups" is queued and will be launched within a minute.: Задача
        "Создание резервных копий" поставлена в очередь и будет запущена в течение минуты.
    ? Attention! Backups are currently being made. This process can take a long time.
        Wait until the process is complete to download the current backups.
    : Внимание! В настоящее время создаются резервные копии. Этот процесс может занимать
        длительное время. Для скачивания актуальных резервных копий дождитесь окончания
        процесса.
    Current elapsed time: Текущее затраченное время
    The previous backup was created for: Предыдущий бекап был создан за
    You can update the backup copies of the site data yourself to download the most current version of the data.: Вы
        можете самостоятельно обновить резервные копии данных сайта, чтобы скачать самую
        актуальную версию данных.
    You can update your site data backups yourself to download the most current version of the data.: Вы
        можете самостоятельно обновить резервные копии данных сайта, чтобы скачать самую
        актуальную версию данных.
    Create backups: Создать резервные копии
    Download backups: Скачать резервные копии
    Databases: Базы данных
</i18n>