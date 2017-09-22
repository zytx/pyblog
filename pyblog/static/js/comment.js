var comments=(function($,emojione){
    var content = $("#content");
    var form = {
        self:'#comment-form',
        to:'input[name="to"]',
        nikename:'input[name="nikename"]',
        email:'input[name="email"]',
        site:'input[name="url"]',
        avatar:'#comment-form-avatar',
        content:'textarea[name="content"]',
        submit:'#comment-submit'
    };
    function regAJAX() {
        content.on('submit',form.self,function(e){
            e.preventDefault();
            $(form.submit).attr("disabled",true);
            var data = $(this).serialize()+'&to='+$(form.to).val();
            $.post('',data,function(re) {
                $(form.self).find(".invalid-feedback").text('');                       //清空表单错误提示
                $(form.self).find(".form-control.is-invalid").removeClass('is-invalid');
                if(re['status']){                                           //评论成功
                    $("#comment-success").html('评论成功');                  //插入新评论
                    var ml = 0;
                    $(form.self).before('<div class="media my-2">\
                    <img class="avatar d-flex mt-1 mr-2" width="60px" src="'+ $(form.avatar).attr('src') +'">\
                    <div class="media-body">'+emojione.unicodeToImage($(form.nikename).val()||$('#comment-form .comment-nikename').text())+'\
                    <span class="small text-secondary float-right">刚刚</span>\
                    <div class="my-3">'+emojione.unicodeToImage($(form.content).val())+'</div></div></div>').prev().hide().fadeIn();
                }else{
                    for(var k in re['errors']){
                        if(k=='content') {
                            $(".emojionearea").addClass('is-invalid');
                        }
                        $(form.self).find("[name='"+k+"']").addClass('is-invalid').siblings('.invalid-feedback').hide().fadeIn(500).html(re['errors'][k]);
                    }
                }
                $(form.submit).attr("disabled",false);
            },'json');
        });
    }
    function offAJAX() {
        content.off('submit');
    }
    function init() {
        autoload();
        content.on('click',".comment-reply",function(){
            if ($(this).text()=='Reply'){
                $(form.self).prev().find('.comment-reply').text('Reply');
                $(this).text('Cancel');
                $(form.to).val($(this).attr('data-to'));
                $(this).closest('.media').find('.comment-text').first().after($(form.self));
            }else{
                $('#comment-list').after($(form.self));
                $(this).text('Reply');
                $(form.to).val('');
            }
        }).on('blur',form.email,function(){
            var avatar=function(){$(form.avatar).attr('src','//cdn.v2ex.com/gravatar/'+ md5($(form.email).val()) +'?s=130&d=retro')}
            if(typeof md5 !== 'undefined' && $.isFunction(md5)){
                avatar();
            }else{
                $.getScript('//cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.min.js',function(){avatar()});
            }
        });
    }
    function brow() {
        if(!$('#comment-list').hasClass('emojied')){
            $('.comment-text,.comment-nikename,#comment-form-nikename').each(function(){      //渲染评论表情
                $(this).html(emojione.unicodeToImage($(this).html()));
            });
            $('#comment-list').addClass('emojied');
        }
    }
    function textArea() {
        var t=function() {
            $("#comment-form textarea").emojioneArea({          //渲染评论文本框
              template        : "<filters/><tabs/><editor/>",
              tonesStyle      : "radio",
              imageType       : "svg",
              autocomplete    : false,    //关闭自动补全
              useInternalCDN  : false,      //关闭cloudflare CDN
              buttonTitle     : '表情[Tab]'
            });
        }
        if(typeof $().emojioneArea !== 'undefined' && $.isFunction($().emojioneArea)){
            t();
        }else{
            $("<link>").attr({
                rel: "stylesheet",
                type: "text/css",
                href: "/static/emojionearea/emojionearea.min.css"
            }).appendTo("head");
            $.getScript('//cdn.jsdelivr.net/gh/mervick/emojionearea@3.1.8/dist/emojionearea.min.js',function() {
                t();
            })
        }

    }
    function autoload() {
        if($(document).scrollTop()+$(window).height()>$('#comment-list').offset().top){
            brow();
        }
        if($(document).scrollTop()+$(window).height()>$('#comment-form').offset().top){
            textArea();
        }
    }
    return {
        regAJAX,
        offAJAX,
        autoload,
        init,
    };
})(jQuery,emojione);

$(window).scroll(function() {
    comments.autoload();
});