import { createI18n } from 'vue-i18n'
import {nextTick} from "vue";

export const SUPPORT_LOCALES = ['en', 'ru', 'fr', 'es', 'it', 'de', 'zh-hans', 'ja', 'uk']
export const LANGUAGES = {
    en: 'English',
    ru: 'Russian',
    fr: 'French',
    es: 'Spanish',
    it: 'Italian',
    de: 'German',
    'zh-hans': 'Chinese',
    ja: 'Japanese',
    uk: 'Ukrainian',
}

export const lang_title = locale => LANGUAGES[locale]

export function getLocale(i18n) {
    return i18n.mode === 'legacy' ? i18n.global.locale : i18n.global.locale.value
}


export function setLocale(i18n, locale) {
    if (i18n.mode === 'legacy') i18n.global.locale = locale
    else i18n.global.locale.value = locale
}


export function setupI18n(options = { locale: 'en' }) {
    const i18n = createI18n(options)
    setI18nLanguage(i18n, options.locale)
    return i18n
}


export function setI18nLanguage(i18n, locale) {
    // set locale
    setLocale(i18n, locale)

    // apply headers if it needs
    // axios.defaults.headers.common['Accept-Language'] = locale
    document.querySelector('html').setAttribute('lang', locale)
}
