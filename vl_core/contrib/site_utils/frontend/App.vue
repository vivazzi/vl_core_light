<script setup>
import {useI18n} from "vue-i18n"
const {t} = useI18n()

import {urls} from "./router"

import state from "../../../frontend/src/state"
const {app_error} = state
</script>


<template>
    <div class="mes e" v-if="app_error">{{ app_error }}</div>

    <main>
        <div class="sidebar">
            <ul>
                <li v-for="(url, i) in urls" :key="i"><router-link :to="{name: url.component}">{{ t(url.title) }}</router-link></li>
            </ul>
        </div>
        <div class="cb">
            <router-view />
        </div>
    </main>
</template>


<style lang="scss">
@import "../../../static/vl_core/vars";
@import "../../../static/vl_core/admin_styles";
@import "../../../static/vl_core/mes";

$sidebar_border_color: #8bbdd4;

#app {
    main {display: flex;}

    h1 {margin-top: 7px;font-weight: normal;color: #555;}

    .sidebar {
        border-right: 1px solid $sidebar_border_color;margin-right: 40px;
        ul {margin: 0;padding-left:0;list-style: none}
        li {
            list-style-type: none;
            &:first-child {padding-top: 0;}
            a {
                padding: 10px 30px 10px 15px;display: block;font-size: 1.2em;text-decoration: none;

                &.router-link-active, &:hover {color: #fff;background-color: $brand_color_blue;}
            }
        }
    }

    @media (max-width: 767px) {
        main {flex-direction: column;}
        .sidebar {margin-right: 0;border-right: none;border-bottom: 2px solid $sidebar_border_color;margin-bottom: 30px;}
    }
}
</style>


<i18n>
ru:
    Management commands: Команды сайта
    Performance: Производительность
    Email testing: Тестирование отправки письма
    Used components: Используемые компоненты
</i18n>
