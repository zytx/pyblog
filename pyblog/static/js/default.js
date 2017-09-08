var comments=(function($) {
    var _count = 0;
    var m1 = function() {
        alert('m1');
    };
    var m2 = function() {
        // ...
    };

    return {
        m1 : m1,
        m2 : m2
    };
})(jQuery);

alert(comments._count);

var progress_bar = $(".header-progress-bar");
function getCookieAJAX(){
    var name = "AJAX=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}
function setCookieAJAX(v) {
    document.cookie="AJAX="+v+";path=/";
}
function ajaxFilter(data) {
    progress_bar.css("width","90%");
    $("title").html($(data).filter('title:first').html());
    window.history.pushState(data, null, this.url);
    return $(data).not("title");
}
function ajaxBefore() {
    $("#content").after('<div class="mask"></div>');
    $(".mask").css("opacity",".5");
    $('html,body').animate({scrollTop:0},500);      //滚动到顶部
    progress_bar.animate({'width':'50%'},function() {
        $(this).animate({'width':'80%'},1000);
    });
}
function ajaxSuccess(result) {
    progress_bar.animate({'width':'100%'});
    $("#content").animate({'right':'1.3em','opacity':'0'},10,function() {
        $(this).html(result);
        $(this).animate({'right':'0em','opacity':'1'},300,function() {
            prettyPrint();
            emoji();
            $(".mask").remove();
        });
    });

    progress_bar.animate({'opacity':0},100,function() {
        $(this).css({'width':0});
    });

}
function ajaxReg(){
    $("body").on('click','a:not([rel*="nofollow"],[target="_blank"],:has(img))',function(e){
        e.preventDefault();
        if( $(this).is("[href^='#']") ){
            $("html,body").animate({scrollTop: $($(this).attr('href')).offset().top}, 300);
            return 0;
        }
        progress_bar.stop(true);       //清除元素的所有动画，停止在当前状态
        progress_bar.css({'width':0,'opacity':'.2'});
        progress_bar.animate({"width":"30%"});
        
        $.ajax({url:this,
            dataFilter:ajaxFilter,
            beforeSend:ajaxBefore,
            success:ajaxSuccess,
            });
    });
    regCommentAJAX();
    setCookieAJAX(1);
}
function ajaxOff(){
    $("body").off('click','a:not([rel*="nofollow"],[target="_blank"],:has(img))');
    unCommentAJAX();
    setCookieAJAX(0);
}
function modelInit() {
    $('#content').on('click','#reward',function(){
        if($('#rewardmodal').length == 0){
            $("body").append('<div class="modal fade" id="rewardmodal" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><h5 class="modal-title">打赏</h5><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body text-center"><img src="/static/img/alipay.gif" height="200" %}"></img><br>支付宝</div></div></div></div>')
        }
        $('#rewardmodal').modal('show');
    });
}
function commentInit() {
    $("#content").on('click',".comment-reply",function(e){
        e.preventDefault();
        if ($(this).text()=='Reply'){
            $('#comment-form').prev().find('.comment-reply').text('Reply');
            $(this).text('Cancel');
            $('input[name="to"]').val($(this).attr('data-to'));
            $(this).parent().parent().parent().parent().after($('#comment-form'));
        }else{
            $('#comments').append($('#comment-form'));
            $(this).text('Reply');
            $('input[name="to"]').val('');
        }
    }).on('blur',"input[name='g_email']",function(e){
        e.preventDefault();
        if($(this).val().match(/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/ ))
        {
            $('#comment-form-avatar').attr('src','//cdn.v2ex.com/gravatar/'+ md5($(this).val()) +'?s=130&d=retro');
        }
    });
}
function regCommentAJAX() {
    $("#content").on('submit',"#comment-form",function(e){
        e.preventDefault();
        $("#comment-submit").attr("disabled",true);
        var data = $(this).serialize()+'&to='+$('input[name="to"]').val();
        $.post('',data,function(re) {
            $(".invalid-feedback").text('');                       //清空表单错误提示
            $(".is-invalid").removeClass(this);
            $("#comment-form .form-group input").removeClass('is-invalid');
            if(re['status']){                                           //评论成功
                $("#comment-success").html('评论成功');                  //插入新评论
                var comment = $('#comment-form').prev().clone();
                $(comment).children('img').attr('src','//cdn.v2ex.com/gravatar/'+ md5($("input[name='g_email']").val()) +'?s=50&d=retro');
                var ml = 0;
                if($('#comment-form input[name="to"]').val()!='')
                    ml = parseInt($('#comment-form').prev().css('margin-left'))+40;
                $(comment).css('margin-left',ml);
                $(comment).find('.comment-title').html('<a href="'+$("input[name='g_site']").val()+'">'+$("input[name='g_nikename']").val()+'</a>');
                $(comment).find('.comment-date').text('刚刚');
                $(comment).find('.comment-text').text($("[name='content']").val());
                $('#comment-form').before(comment);
            }else{
                for(var k in re['errors']){
                    if(k=='content') {
                        $(".emojionearea").addClass('is-invalid');
                    }
                    $("[name='"+k+"']").addClass('is-invalid').siblings('.invalid-feedback').html(re['errors'][k]);
                }
            }
            $("#comment-submit").attr("disabled",false);
        },'json');
    });
}
function unCommentAJAX() {
    $("#content").off('submit');
}
function emoji() {
    $('.comment-text').each(function(){
        $(this).html(emojione.unicodeToImage($(this).html()));
    });
    $("#comment-form textarea,#comment-form .comment-title").emojioneArea({
      template: "<filters/><tabs/><editor/>",
      tonesStyle: "radio",
      imageType: "svg",
    });
}
$(document).ready(function(){
    commentInit();
    prettyPrint();
    modelInit();
    emojione.imageType = 'svg';
    emoji();
    window.history.replaceState('<title>'+$('title:first').text()+'</title>'+$('#content').html(), null, this.url);
    cookieAJAX=getCookieAJAX();
    if(cookieAJAX==""){
        setCookieAJAX(1);
        ajaxReg();
    }else if(cookieAJAX=="1"){
        ajaxReg();
    }
    $("#ajax-checkbox").on('change',function(){
        if(this.checked) {
            ajaxReg();
        }else{
            ajaxOff();
        }
    });
    window.onpopstate=function() {
        $("title").html($(window.history.state).filter('title:first').html());
        ajaxSuccess(window.history.state);
    }
});