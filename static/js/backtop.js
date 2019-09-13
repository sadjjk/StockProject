if ($('#back-to-top').length) {
        var scrollTrigger = 100; // px

        // $(window).scrollTop()与 $(document).scrollTop()产生结果一样
        // 一般使用document注册事件，window使用情况如 scroll, scrollTop, resize
        $(window).on('scroll', function () {
            if ($(window).scrollTop() > scrollTrigger) {
                $('#back-to-top').addClass('show');
            } else {
                $('#back-to-top').removeClass('show');
            }
        });

        $('#back-to-top').on('click', function (e) {
            // html,body 都写是为了兼容浏览器
            $('html,body').animate({
                scrollTop: 0
            }, 700);

            return false;
        });
    }