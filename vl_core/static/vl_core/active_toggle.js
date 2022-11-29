function active_toggle(manager_el, toggle_elements, active_on_checked, use_slide, hor_filter_elements){
    function hide_toggle_elements(to_hide) {
        let el, selector, name;
        $.each(toggle_elements, function () {
            el = '';
            name = $(this).attr('name');

            // check on hor_filter_elements
            $.each(hor_filter_elements, function (index, value) {
                if (name === value + '_old') el = $('.field-'+value);
            });

            if (!el) el = $(this).parents('.field-'+name);

            if (to_hide) el.hide(); else el.slideToggle(500);
        });
    }

    function do_enable() {
        if (!use_slide) toggle_elements.removeAttr('disabled');
    }

    function do_disable(use_hide) {
        if (!use_slide) toggle_elements.attr('disabled','disabled');
        if (use_hide) hide_toggle_elements(true);
    }

    if (use_slide === undefined) use_slide = false;
    if (hor_filter_elements === undefined) hor_filter_elements = false;

    if (active_on_checked) {
        if (manager_el.attr('checked')) do_enable(); else do_disable(use_slide);
    } else {
        if (!manager_el.attr('checked')) do_enable(); else do_disable(use_slide);
    }

    manager_el.click(function(){
        if (toggle_elements.attr('disabled') === 'disabled') do_enable(); else do_disable(false);

        if (use_slide) hide_toggle_elements(false);
    });
}