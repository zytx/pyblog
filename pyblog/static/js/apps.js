var auth = (function ($) {
    $('body').on('submit', "#login-form,#register-form", function (e) {
        e.preventDefault();
        form = $(this);
        $.post(form.attr('action'), form.serialize(), function (re) {
            if (re['status'] == 1) {
                location.reload();
            } else {
                form.find(".invalid-feedback").text('');
                form.find(".form-control.is-invalid").removeClass('is-invalid');
                for (var k in re['errors']) {
                    form.find("input[name='" + k + "']").addClass('is-invalid').siblings('.invalid-feedback').hide().fadeIn(500).html(re['errors'][k]);
                }
            }
        }, 'json');
    });
})(jQuery);

var siteAJAX = (function ($) {
    var content = $('#content');
    var selector = 'a:not([rel*="nofollow"],[rel*="external"],[target="_blank"],[href^="#"],:has(img))';
    var progress_bar = $(".header-progress-bar");

    var setCookie = function (v) {
        document.cookie = "AJAX=" + v + ";path=/";
    };
    var ajaxSuccessCallback = function () {
    };
    var ajaxRegCallback = function () {
    };
    var ajaxOffCallback = function () {
    };
    var ajaxSuccess = function (result) {
        progress_bar.stop(true).animate({'width': '100%'}, 100, function () {
            content.animate({'right': '1.3em', 'opacity': '0'}, 10).html(result).animate({
                'right': '0em',
                'opacity': '1'
            }, 300, function () {
                ajaxSuccessCallback();
                $(".mask").hide();
            })
        }).animate({'opacity': 0}, 800, function () {
            $(this).css({'width': 0});
        });
    };
    var dataFilter = function (data) {
        $("title").html($(data).filter('title:first').html());
        var outline = $(data).filter('#data-outline');
        if (outline.find('ul li').length > 0) {
            $('#sidebar #outline').html(outline.html()).show();
        } else {
            $('#sidebar #outline').hide();
        }
        return $(data).not("title").not("#data-outline");
    };
    var ajaxReg = function () {
        $("body").off('click', selector).on('click', selector, function (e) {
            e.preventDefault();
            if ($(this)[0].host != window.location.host) {     //非本站链接跳转
                window.open($(this)[0].href);
                return;
            }
            progress_bar.stop(true).css({'width': 0, 'opacity': '.2'}).animate({"width": "20%"});
            $.ajax({
                url: this,
                context: content,
                dataFilter: function (data) {
                    progress_bar.stop(true).animate("width", "90%");
                    window.history.pushState(data, $(data).filter('title:first').html(), this.url);
                    return dataFilter(data);
                },
                beforeSend: function () {
                    $(".mask").show();
                    $('html,body').animate({scrollTop: 0}, 500);      //滚动到顶部
                    progress_bar.animate({'width': '70%'}, 1000);
                },
                success: ajaxSuccess
            });
        });
        ajaxRegCallback();
    };
    var outline = function () {
        /**
         * 侧边栏文章提纲
         * */
        var ol = $('#outline');
        threshold();
        // 跟随滚动
        if ($(document).scrollTop() > ol.prev().offset().top) ol.css({'top': 0, 'position': 'fixed'});
        $(window).scroll(function () {
            if ($('article').length != 0 && $(document).scrollTop() > ol.prev().offset().top + ol.prev().height() && $(document).scrollTop() < $('article').offset().top + $('article').height()) {
                ol.css({'top': 0, 'position': 'fixed'});
            } else {
                ol.css({'position': 'relative'});
            }
        });
        $(window).resize(threshold);

        function threshold() {
            if ($(document.body).width() < 1200) {
                // 小屏隐藏
                ol.hide();
                return
            } else {
                // 设置宽度
                ol.css('width', $('#sidebar').width()).show();
            }
        }

        // 二级标题自动折叠
        var timer = null;
        $(window).on('activate.bs.scrollspy', function (event) {
            if (timer) {
                window.clearTimeout(timer);
            }
            timer = window.setTimeout(function () {
                ol.find('ul ul').addClass('d-none');
                if (ol.find('.active:first-child').next().is('ul')) {
                    ol.find('.active:first-child').next().removeClass('d-none');
                }
            }, 50);
        })
    };
    var anchorScroll = function () {
        $('body').on('click', 'a[href^="#"]:not([data-toggle="collapse"],[data-toggle="modal"])', function (e) {        //本页锚点平滑滚动
            e.preventDefault();
            $("html,body").animate({scrollTop: $($(this).attr('href')).offset().top}, 300);
            $(this).blur();
        });
    };
    outline();
    anchorScroll();
    window.history.replaceState('<title>' + $(document).attr("title") + '</title>' + content.html() + '<div id="data-outline">' + $('#outline').html() + '</div>', null, window.location.href);
    var cookieAJAX = (function () {
        var name = "AJAX=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1);
            if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
        }
        return "";
    })();
    if (cookieAJAX == "") {
        setCookie(1);
        ajaxReg();
    } else if (cookieAJAX == "1") {
        ajaxReg();
    }
    $("#ajax-checkbox").on('change', function () {
        if (this.checked) {
            setCookie(1);
            ajaxReg();
        } else {              //关闭AJAX
            $("body").off('click', selector);
            ajaxOffCallback();
            setCookie(0);
        }
    });
    window.onpopstate = function () {          //浏览器前进后退
        ajaxSuccess(dataFilter(window.history.state));
    };
    return {
        'setCallback': function (op) {
            if (typeof op.ajaxSuccess !== 'undefined' && $.isFunction(op.ajaxSuccess)) ajaxSuccessCallback = op.ajaxSuccess;
            if (typeof op.ajaxReg !== 'undefined' && $.isFunction(op.ajaxReg)) {
                ajaxRegCallback = op.ajaxReg;
                $("#ajax-checkbox").change();
            }
            if (typeof op.ajaxOff !== 'undefined' && $.isFunction(op.ajaxOff)) {
                ajaxOffCallback = op.ajaxOff;
                $("#ajax-checkbox").change();
            }
        }
    }
})(jQuery);

function codeHighlight() {
    if ($('pre.prettyprint').length > 0) {
        if (typeof prettyPrint !== 'undefined' && $.isFunction(prettyPrint)) {
            prettyPrint();
        } else {
            $.getScript('//cdn.bootcss.com/prettify/r224/prettify.min.js', function () {
                prettyPrint();
            })
        }
    }
}

$.ajaxSetup({cache: true});

$(document).ready(function () {
    codeHighlight();
    comments.regAJAX();
    siteAJAX.setCallback({
        'ajaxSuccess': function () {
            codeHighlight();
            comments.initLazyLoad();
            comments.regAJAX();
        }
    });
    $('#reward-modal').on('show.bs.modal', function () {   //悬赏模态框显示时加载图片
        ali = $(this).find('#alipay');
        ali.attr('src', ali.attr('data-src'));
    });
    $('#header .nickname').html(function () {
        return emojione.unicodeToImage($(this).html());
    });
    $('.modal').keydown(function (e) {
        if (e.keyCode == 13) {
            $(this).find('form').submit();
        }
    });
});
