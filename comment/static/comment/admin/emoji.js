$(document).ready(function(){
    emojione.imageType = 'svg';
    emojione.imagePathSVG = '//cdn.bootcss.com/emojione/2.2.7/assets/svg/';
    $('#id_g_nikename, td.field-g_nikename, td.field-content, .breadcrumbs').each(function(){      //渲染评论表情
        $(this).html(emojione.unicodeToImage($(this).html()));
    });
    $("#id_content").emojioneArea({          //渲染评论文本框
      template: "<filters/><tabs/><editor/>",
      tonesStyle: "radio",
      imageType: "svg",
      autocomplete  : false,    //关闭自动补全
      useInternalCDN:false      //关闭cloudflare CDN
    });
    $('.emojionearea').closest('.form-row').css('overflow','visible');
});
