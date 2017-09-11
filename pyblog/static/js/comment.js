
var auth=(function () {
    $('body').on('submit',"#login-form,#register-form",function(e){
        e.preventDefault();
        form = $(this);
        $.post(form.attr('action'),form.serialize(),function(re) {
            if(re['status']==1){
                location.reload();
            }else{
                form.find(".invalid-feedback").text('');
                form.find(".form-control.is-invalid").removeClass('is-invalid');
                for(var k in re['errors']){
                    form.find("input[name='"+k+"']").addClass('is-invalid').siblings('.invalid-feedback').hide().fadeIn(500).html(re['errors'][k]);
                }
            }
        },'json');
    });

    
    
})();

var comments=(function($){
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
        content.on('click',".comment-reply",function(e){
            e.preventDefault();
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
        }).on('blur',form.email,function(e){
            e.preventDefault();
            $(form.avatar).attr('src','//cdn.v2ex.com/gravatar/'+ md5($(this).val()) +'?s=130&d=retro');
        });
    }
    return {
        regAJAX,
        offAJAX,
        init
    };
})(jQuery);