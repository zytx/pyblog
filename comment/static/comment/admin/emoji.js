$(document).ready(function(){
    $('#id_g_nickname, td.field-g_nickname, td.field-content, .breadcrumbs').each(function(){      //渲染评论表情
        $(this).html(emojione.unicodeToImage($(this).html()));
    });
    $("#id_content").emojioneArea({          //渲染评论文本框
      tonesStyle: "radio",
      autocomplete  : false    //关闭自动补全
    });
    $('.emojionearea').closest('.form-row').css('overflow','visible');
});
