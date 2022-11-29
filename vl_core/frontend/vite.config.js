import {resolve} from 'path';
import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueI18n from '@intlify/vite-plugin-vue-i18n'

export default ({ mode }) => {
    process.env = {...process.env, ...loadEnv(mode, process.cwd())};

    return defineConfig({
        plugins: [
            vue(),
            vueI18n({defaultSFCLang: 'yml',})
        ],
        root: resolve('../../vl_core'),
        base: '/static/vl_core/frontend/',
        server: {
            host: 'localhost',
            port: process.env.VITE_VL_CORE_FRONTEND_PORT || 4000,
            open: false,
            watch: {
                usePolling: true,
                disableGlobbing: false,
            },
        },
        resolve: {
            extensions: ['.js', '.json'],
        },
        build: {
            outDir: resolve('../static/vl_core/frontend'),
            assetsDir: '',
            manifest: true,
            emptyOutDir: true,
            rollupOptions: {
                input: {
                    site_utils: resolve('../contrib/site_utils/frontend/main.js'),
                    backup: resolve('../contrib/backup/frontend/main.js'),
                },
                output: {
                    chunkFileNames: undefined,
                },
            },
        },
    });
};