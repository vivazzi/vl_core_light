import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import setupRouter from "./router";
import {setupI18n} from '../../../frontend/src/i18n';
import state from '../../../frontend/src/state';
import {define_locale_from_url} from "../../../frontend/src/utils/locale";

const {set_urls, set_locale, set_config, add_app_errors} = state

const _locale = define_locale_from_url()

axios.get(window.app_config.app_config_url)
    .then(function (response) {
        set_urls(response.data.urls)
        set_config(response.data.config)
        set_locale(_locale)

        const i18n = setupI18n({
            legacy: false,
            locale: _locale,
            fallbackLocale: 'en',
            missingWarn: false,
            fallbackWarn: false,
        })


        const app = createApp(App)
        app.use(i18n)
        app.use(setupRouter(response.data.urls.base_menu))
        app.mount('#app')
    })
    .catch(function (error) {
        add_app_errors(error)
    })
