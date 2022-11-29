import {useI18n} from "vue-i18n";
import {computed} from "vue";
import {params_to_object} from "./other";
import {SUPPORT_LOCALES} from "../i18n";



export const is_home = computed(() => {
    if (window.location.pathname === '/') return true

    for (let i=0; i<SUPPORT_LOCALES.length; i++)
        if (window.location.pathname === `/${SUPPORT_LOCALES[i]}/`)
            return true

    return false
})


export const url0 = (locale, url, base_url, translations) => {
    if (translations !== undefined) {
        url = translations[locale]
        if (!url && locale !== 'en') url = translations['en']
        return url
    }

    if (base_url === undefined) base_url = '';

    if (locale !== 'en') url = '/' + locale + url

    return base_url + url
}

export const url = (url, base_url, translations) => {
    const { locale } = useI18n()

    return url0(locale.value, url, base_url, translations)
}

export const router_url = name => {
    const { locale } = useI18n()

    if (locale.value === 'en') return { 'name': 'en_' + name }

    return { 'name': name, params: { locale: locale.value } }
}


export const url_with_query_string = (url, query_dict) => {
    if (Object.keys(query_dict).length > 0) url += `?${new URLSearchParams(query_dict).toString()}`

    return url
}


export const url_with_add_query_string = (url, query_dict) => {
    let search_params = (new URL(document.location)).searchParams

    if (query_dict !== undefined) {
        let extended_query_dict = params_to_object(search_params)
        Object.assign(extended_query_dict, query_dict)

        if (Object.keys(extended_query_dict).length > 0) url += `?${new URLSearchParams(extended_query_dict).toString()}`
    } else {
        search_params = search_params.toString()
        if (search_params.length > 0) url += `?${search_params}`
    }

    return url
}