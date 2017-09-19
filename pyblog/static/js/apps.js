var siteAJAX=(function($,comments) {
    var content = $('#content');
    var selector = 'a:not([rel*="nofollow"],[rel*="external"],[target="_blank"],[href="#"],:has(img))';
    var progress_bar = $(".header-progress-bar");

    var setCookie = function (v) {
        document.cookie="AJAX="+v+";path=/";
    }
    var callback = function(){};
    var ajaxSuccess = function(result) {
        progress_bar.stop(true).animate({'width':'100%'},100,function() {
            content.animate({'right':'1.3em','opacity':'0'},10).html(result).animate({'right':'0em','opacity':'1'},300,function() {
                callback();
                $(".mask").hide();
            })
        }).animate({'opacity':0},800,function () {
            $(this).css({'width':0});
        });
    }
    var ajaxReg = function (){
        $("body").on('click',selector,function(e){
            e.preventDefault();
            if($(this)[0].host != document.domain){     //非本站链接跳转
                window.open($(this)[0].href);
                return;
            };
            if($(this).is('[href^="#"]')){        //本页锚点滚动
                $("html,body").animate({scrollTop: $($(this).attr('href')).offset().top}, 300);
                return;
            }
            progress_bar.stop(true).css({'width':0,'opacity':'.2'}).animate({"width":"20%"});
            $.ajax({
                url:this,
                context:content,
                dataFilter:function(data) {
                    progress_bar.stop(true).animate("width","90%");
                    $("title").html($(data).filter('title:first').html());
                    window.history.pushState(data, null, this.url);
                    return $(data).not("title");
                },
                beforeSend:function() {
                    $(".mask").show();
                    $('html,body').animate({scrollTop:0},500);      //滚动到顶部
                    progress_bar.animate({'width':'70%'},1000);
                },
                success:ajaxSuccess,
            });
        });
        comments.regAJAX();
        setCookie(1);
    }
    var init = function (ck) {
        callback=ck;
        window.history.replaceState('<title>'+$('title:first').text()+'</title>'+content.html(), null, this.url);
        var cookieAJAX = (function (){
            var name = "AJAX=";
            var ca = document.cookie.split(';');
            for(var i=0; i<ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1);
                if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
            }
            return "";
        })();
        if(cookieAJAX==""){
            setCookie(1);
            ajaxReg();
        }else if(cookieAJAX=="1"){
            ajaxReg();
        }
        $("#ajax-checkbox").on('change',function(){
            if(this.checked) {
                ajaxReg();
            }else{              //关闭AJAX
                $("body").off('click',selector);
                comments.offAJAX();
                setCookie(0);
            }
        });
        window.onpopstate=function() {          //浏览器前进后退
            $("title").html($(window.history.state).filter('title:first').html());
            ajaxSuccess(window.history.state);
        }
    }
    return {
        init
    }
})(jQuery,comments);


function modelInit() {
    $('#reward-modal').on('show.bs.modal',function(e){
        $(this).find('#alipay').attr('src','/static/img/alipay.gif');
    });
}

function emoji() {
    emojione.imageType = 'svg';
    emojione.imagePathSVG = '//cdn.bootcss.com/emojione/2.2.7/assets/svg/';
    //emojione.imagePathSVG = '//cdn.jsdelivr.net/emojione/assets/svg/';
    $('.comment-text,.comment-nikename,#comment-form-nikename').each(function(){      //渲染评论表情
        $(this).html(emojione.unicodeToImage($(this).html()));
    });
    $("#comment-form textarea").emojioneArea({          //渲染评论文本框
      template        : "<filters/><tabs/><editor/>",
      tonesStyle      : "radio",
      imageType       : "svg",
      autocomplete    : false,    //关闭自动补全
      useInternalCDN  : false,      //关闭cloudflare CDN
      buttonTitle     : '表情[Tab]'
    });
}

$(document).ready(function(){
    prettyPrint();
    comments.init();
    emoji();
    modelInit();

    siteAJAX.init(function(){
        prettyPrint();
        emoji();
    });
    
    $('.modal').keydown(function(e){
        if(e.keyCode==13){
            $(this).find('form').submit();
        }
    });
});
