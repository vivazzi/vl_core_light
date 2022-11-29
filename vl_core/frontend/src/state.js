import { reactive, computed } from 'vue';


const _state = reactive({
    urls: {},
    app_errors: [],
    config: {},
});


// ---------------------------------------------------------
const set_urls = urls => _state.urls = urls
const urls = computed(() => _state.urls)


const set_locale = locale => _state.locale = locale
const locale = computed(() => _state.locale)


// --- error handler ---
const add_app_errors = (errors=null, error=null) => {
    // errors can be string or array
    if (errors === null && error === undefined) return;

    _state.app_errors = []

    if (errors) {
        if (errors.constructor === Array) _state.app_errors = errors
        else _state.app_errors = [errors]
    }

    if (error) {
        console.log(error.stack)

        if (error.response === undefined) {
            _state.app_errors.push('Network Error. Check your internet connection.')
        } else {
            switch (error.response.status) {
                case 500:
                    _state.app_errors.push('Sorry, but there was a programming error on page. A notification has already been sent to technical support. Please try again in a few minutes.')
                    break;
                case 404:
                    _state.app_errors.push('Data is not found')
                    break;
                default:
                    _state.app_errors.push(error.message)
            }
        }
    }
}
const clear_app_errors = () => _state.app_errors = []
const app_errors = computed(() => _state.app_errors)
// --- end error handler ---

const set_config = config => _state.config = config
const config = computed(() => _state.config)
// ---------------------------------------------------------

const state = {
    set_urls, urls,
    set_locale, locale,

    add_app_errors, clear_app_errors, app_errors,

    set_config, config,
}

export default state