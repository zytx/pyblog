var comments=(function($,emojione){
    var content = $("#content");
    var form = {
        self:'#comment-form',
        to:'input[name="to"]',
        nickname:'input[name="nickname"]',
        nickname2:'#comment-form .comment-nickname',
        email:'input[name="email"]',
        site:'input[name="url"]',
        avatar:'#comment-form-avatar',
        content:'textarea[name="content"]',
        submit:'#comment-submit'
    };
    var comment = {
        list:'#comment-list',
        reply:'.comment-reply'
    };
    var user_url = function () {
        $(form.site).val() || $(form.nickname2).attr('href');
    }();
    initLazyLoad();
    lazyLoadBrow();
    lazyLoadEmojiTextArea();
    content.on('click',comment.reply,function(){
        if ($(this).text()=='Reply'){
            $(form.self).prev().find(comment.reply).text('Reply');
            $(this).text('Cancel');
            $(form.to).val($(this).attr('data-to'));
            $(this).closest('.media').find('.comment-text').first().after($(form.self));
        }else{
            $(comment.list).after($(form.self));
            $(this).text('Reply');
            $(form.to).val('');
        }
    }).on('blur',form.email,function(){
        var avatar=function(){$(form.avatar).attr('src','//cdn.v2ex.com/gravatar/'+ md5($(form.email).val()) +'?s=130&d=retro')};
        if(typeof md5 !== 'undefined' && $.isFunction(md5)){
            avatar();
        }else{
            $.getScript('//cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.min.js',function(){avatar()});
        }
    });

    function regAJAX() {
        content.off('submit',form.self).on('submit',form.self,function(e){
            e.preventDefault();
            $(form.submit).attr("disabled",true);
            var data = $(this).serialize()+'&to='+$(form.to).val();
            $.post('',data,function(re) {
                $(form.self).find(".invalid-feedback").text('');                       //清空表单错误提示
                $(form.self).find(".form-control.is-invalid").removeClass('is-invalid');
                if(re['status']){                                           //评论成功
                    $("#comment-success").html('评论成功');                  //插入新评论
                    $(form.self).before('<div class="media my-2">\
                    <img class="avatar d-flex mt-1 mr-2" width="60px" src="'+ $(form.avatar).attr('src') +'">\
                    <div class="media-body"><a href="'+user_url+'">'+emojione.unicodeToImage($(form.nickname).val()||$(form.nickname2).text())+'</a>\
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
    function lazyLoadBrow() {
        if($(comment.list).length && $(document).scrollTop() + $(window).height() > $(comment.list).offset().top){
            $(window).off('scroll', lazyLoadBrow);
            $('.comment-text,.comment-nickname,#comment-form-nickname').each(function(){      //渲染评论表情
                $(this).html(emojione.unicodeToImage($(this).html()));
            });
        }
    }
    function lazyLoadEmojiTextArea() {
        if($(form.self).length && $(document).scrollTop() + $(window).height() > $(form.self).offset().top){
            $(window).off('scroll', lazyLoadEmojiTextArea);
            var t=function() {
                $("#comment-form textarea").emojioneArea({          //渲染评论文本框
                    tonesStyle: 'radio',
                    autocomplete: false,    //关闭自动补全
                    searchPlaceholder: '搜索',
                    buttonTitle: '表情[Tab]'
                });
            };
            if(typeof $().emojioneArea !== 'undefined' && $.isFunction($().emojioneArea)){
                t();
            }else if(!$('#css-emojionearea').length){
                $("<link>").attr({
                    id: "css-emojionearea",
                    rel: "stylesheet",
                    type: "text/css",
                    href: "//cdn.bootcss.com/emojionearea/3.4.1/emojionearea.min.css"
                }).prependTo("head");
                $.getScript('//cdn.bootcss.com/emojionearea/3.4.1/emojionearea.min.js',function() {
                    t();
                })
            }
        }
    }
    function initLazyLoad() {
        $(window).off('scroll',lazyLoadBrow).scroll(lazyLoadBrow);
        $(window).off('scroll',lazyLoadEmojiTextArea).scroll(lazyLoadEmojiTextArea);
    }
    return {
        'regAJAX': regAJAX,
        'offAJAX': function () {
            content.off('submit');
        },
        'initLazyLoad': initLazyLoad
    };
})(jQuery,emojione);