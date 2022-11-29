(function($){
    // workaround for functionality "Add another" button in inline forms
    $(document).ready(function() {
        setTimeout(function() {  // workaround: "Add another" button does not have time to load on the page
            $('.add-row a').click(function () {
                let $add_row_a = $(this)
                setTimeout(function() {  // workaround: new ".form-row" does not have time to load on the page
                    // call color_picker in new .form-row for all color_picker_inputs
                    $add_row_a.parents('form').find('.form-row').not('.empty-form').last().find('.color_picker [type=text]').color_picker()
                }, 100);
            })
        }, 100);
    })

    $.fn.color_picker = function(method) {
        let opt = {
            'color': '#000'
        };

        function hex2rgb(hex, opacity) {
            let h=hex.replace('#', '');
            h =  h.match(new RegExp('(.{'+h.length/3+'})', 'g'));

            for(let i=0; i<h.length; i++)
                h[i] = parseInt(h[i].length===1 ? h[i]+h[i] : h[i], 16);

            if (typeof opacity != 'undefined')  h.push(opacity);

            return 'rgba('+h.join(',')+')';
        }

        function rgb2Hex(a){
            a=a.replace(/[^\d,]/g,"").split(",");
            return '#'+((1<<24)+(+a[0]<<16)+(+a[1]<<8)+ +a[2]).toString(16).slice(1)
        }

        function get_opacity(a){
            a=a.replace(/[^\d,]/g,"").split(",");

            let opacity = parseInt(a[3]);
            if (opacity > 100) opacity = parseInt(opacity.toString().substring(0, 2));

            return opacity
        }


        let methods = {
            init : function(options) {
                this.each(function() {
                    if (options) $.extend(true, opt, options);

                    function set_opacity_label(opacity){
                        $opacity.text(opacity);
                    }
                    function set_opacity_range(opacity){
                        $range.val(opacity);
                    }
                    function set_opacity(opacity){
                        set_opacity_label(opacity);
                        set_opacity_range(opacity);
                    }


                    function set_input_color(color){
                        if (opacity === 100) $input.val(color);
                        else $input.val(hex2rgb(color, opacity/100));
                    }
                    function set_picker_color(color){
                        $picker.val(color).css({'opacity': opacity/100});
                    }
                    function set_color(color){
                        set_input_color(color);
                        set_picker_color(color);
                    }

                    // --- containers ---
                    let $input = $(this);
                    let $color_picker = $input.parents('.color_picker');
                    let $picker = $color_picker.find('.picker');
                    let $range = $color_picker.find('.range');
                    let $opacity = $color_picker.find('.opacity_wr span');

                    let color = opt.color;
                    let opacity = 100;

                    function init(){
                        if (color[0] !== '#'){
                            opacity = get_opacity(color);
                            color = rgb2Hex(color);
                            set_opacity_range(opacity);
                        }

                        set_picker_color(color, opacity);
                        $input.trigger('input');
                        set_opacity(opacity)
                    }


                    // --- input ---
                    $input.on('input', function(){
                        let v = $(this).val().toUpperCase();
                        if (v){
                            v = v.trim();
                            if (v[0] === '#'){
                                opacity = 100;
                                if (v.length === 4) color = v[0] + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
                                else color = v
                            } else {
                                opacity = get_opacity(v);
                                color = rgb2Hex(v);
                            }
                        }

                        set_opacity(opacity);
                        $picker.val(color);
                    });


                    // --- picker ---
                    $picker.change(function(){
                        color = $(this).val();
                        set_color(color, opacity);
                    });


                    // --- range ---
                    let can_change = false;

                    $range.mousedown(function(){
                        can_change = true;
                    });

                    $range.mouseup(function(){
                        can_change = false;
                    });

                    $range.on('mousemove', function(){
                        if (can_change) {
                            opacity = parseInt($(this).val());
                            set_opacity_label(opacity);
                            set_color(color, opacity);
                        }
                    });

                    // --- old_color ---
                    $color_picker.find('.old_color').click(function(){
                        $picker.click();
                    });

                    init();
                });
            }
        };


        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method "' +  method + '" is not exists for color_picker');
        }
    };
})(django.jQuery);
