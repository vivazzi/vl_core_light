import {SUPPORT_LOCALES} from "../i18n";


export const define_locale_from_url = () => {
    let locale = 'en'
    const url = new URL(window.location.href)

    for (let i=0; i<SUPPORT_LOCALES.length; i++)
        if (url.pathname.startsWith(`/${SUPPORT_LOCALES[i]}`))
            return SUPPORT_LOCALES[i]

    return locale
}
