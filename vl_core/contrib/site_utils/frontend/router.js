import { createWebHistory, createRouter } from 'vue-router';

export let urls = [
    {'path': 'command-runner/', 'title': 'Management commands', 'component': 'ManagementCommands'},
    {'path': 'performance/', 'title': 'Performance', 'component': 'Performance'},
    {'path': 'email-testing/', 'title': 'Email testing', 'component': 'EmailTesting'},
    {'path': 'used-components/', 'title': 'Used components', 'component': 'UsedComponents'},
]

const get_routes = (base_menu_url) => {
    let routes = []
    urls.forEach((url) => {
        routes.push({
            path: base_menu_url + url.path,
            name: url.component,
            component: () => import(`./views/${url.component}.vue`),
        })
    });

    routes.push({path: base_menu_url, redirect: {name: 'ManagementCommands'}})

    return routes
}

export default function setupRouter(base_menu_url) {
    return createRouter({
        history: createWebHistory(),
        routes: get_routes(base_menu_url),
    });
}