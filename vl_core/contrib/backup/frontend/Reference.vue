<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n()

const props = defineProps({
    products_url: {
        type: String,
    },
    support_url: {
        type: String,
    },
})
</script>


<template>
    <h2>{{ t('Reference') }}</h2>
    <p>{{ t('You can manage the ordered services') }} <a target="_blank" :href="props.products_url">{{ t('in your personal account in Vuspace') }}</a>.</p>
    <p>{{ t('Please pay on time for domain names and hosting. In case of non-payment of domain names, there is a possibility that after the expiration date someone can buy them. Keep in mind that if the main domain is not paid, then you will not be able to get to your site.') }}</p>
    <p>{{ t('If you have any questions, contact') }} <a target="_blank" :href="props.support_url">{{ t('the support on the Vuspace website') }}</a></p>

    <h2>{{ t('Note') }}</h2>
    <ol>
        <li>{{ t('The backup files are compressed (archived) so they will be smaller than shown in the Site Data Size section. The total size of all backups is displayed in the "Site data size \\ Backups" section.') }}</li>
        <li>{{ t('The site code archive is not created after a certain time interval, but is updated only after changing the site code. The site code archive is much smaller, since it does not contain a virtual environment and service files.') }}</li>
        <li>{{ t('You can download these archives, both for backing up data on your devices, and, if necessary, go to the maintenance and revision of the site to other specialists, since the archives contain everything you need to transfer the site.') }}</li>
    </ol>
</template>


<style lang="scss">
ol {
    line-height: 1.5;padding-left: 15px;
    li {font-size: inherit;line-height: inherit;}
}
</style>


<i18n>
ru:
    Reference: Справка
    You can manage the ordered services: Управлять заказанными услугами по сайту вы можете
    in your personal account in Vuspace: в личном кабинете Vuspace
    ? Please pay on time for domain names and hosting. In case of non-payment of domain
        names, there is a possibility that after the expiration date someone can buy them.
        Keep in mind that if the main domain is not paid, then you will not be able to
        get to your site.
    : Пожалуйста, своевременно оплачивайте доменные имена и хостинг. В случае отсутствия
        оплаты доменных имен есть вероятность, что после окончания срока действия их может
        кто-то купить. Имейте ввиду, если не будет оплачен основной домен, то вы не сможете
        попасть на свой сайт.
    If you have any questions, contact: По всем имеющимся вопросам обращаться
    the support on the Vuspace website: в единую поддержку на сайте Vuspace
    Note: Примечание
    ? The backup files are compressed (archived) so they will be smaller than shown
        in the Site Data Size section. The total size of all backups is displayed in the
        "Site data size \ Backups" section.
    : Файлы резервных копий сжаты (архивированы), поэтому будут меньше размером, чем
        показано в разделе "Размер данных сайта". Суммарный размер всех резервных копий
        отображается в разделе "Размер данных сайта \ Резервные копии".
    ? The site code archive is not created after a certain time interval, but is updated
        only after changing the site code. The site code archive is much smaller, since
        it does not contain a virtual environment and service files.
    : Архив кода сайта не создаётся через определённый временной интервал, а обновляется
        только после изменения кода сайта. Архив кода сайта имеет гораздо меньший размер,
        так как не содержит виртуального окружения и служебных файлов.
    ? You can download these archives, both for backing up data on your devices, and,
        if necessary, go to the maintenance and revision of the site to other specialists,
        since the archives contain everything you need to transfer the site.
    : Вы можете скачать данные архивы, как для резервного копирования данных на своих
        устройствах, так и при необходимости перейти на обслуживание и доработку сайта
        к другим специалистам, так как архивы содержат всё необходимое для переноса сайта.
</i18n>