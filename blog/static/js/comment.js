$(function () {
    function reply(reply_comment_id) {
        // 设置值
        $('#reply_comment_id').val(reply_comment_id);
        var html = $('#comment_' + reply_comment_id).html();
        $('#reply_content').html(html);
        $('#reply_content_container').show();
        $('html').animate({scrollTop: $('#comment').offset().top - 60}, 300, function () {
            CKEDITOR.instances['id_text'].focus();
        })
    }


   $('#comment').submit(function () {
       // 判断是否为空
       $('#comment-error').text('');
       if (CKEDITOR.instances['id_text'].document.getBody().getText().trim()=='') {
           $('#comment-error').text('评论内容不能为空');
           return false
       }

       // 更新数据到textarea
       CKEDITOR.instances['id_text'].updateElement();
       // 异步提交数据
       $.ajax({
           url: "/comment/update_comment/",
           type: 'POST',
           // 根据表单自动生成参数连接
           data: $(this).serialize(),
           // 是否使用缓存
           cache: true,
           // 回调函数
           success: function (data) {
               console.log(data);
               if (data['status']==='SUCCESS'){
                   if ($('#reply_comment_id').val() === '0') {
                        // 插入评论
                       var comment_html = '<div id="root_"' + data["id"] + ' class="comment">\
                                     <span>' + data["username"] + '</span>\
                                     <span>(' + data["comment_time"] + ')</span>\
                                     <div id="comment_' + data["id"] + '">' + data["text"] + '</div>\
                                     <a href="javascript:reply(' + data["id"] + ');">回复</a>\
                                   </div>';
                       $('#comment_list').prepend(comment_html);
                   } else {
                        // 插入回复
                       var reply_html = '<div class="reply">\
                                           <span>' + data["username"] + '</span>\
                                           <span>(' + data["comment_time"] + ')</span>\
                                           <span>回复</span>\
                                           <span>' + data["reply"] + '</span>\
                                           <div id="comment_' + data["id"] + '">'+ data["text"] +'</div>\
                                           <a href="javascript:reply(' + data["id"] + ');">回复</a>\
                                         </div>';
                       $('#root_' + data['root_id']).append(reply_html);
                   }
                   // 清空编辑器内容
                   CKEDITOR.instances['id_text'].setData('');
                   $('#reply_content_container').hide();
                   $('#reply_comment_id').val('0');
                   $('#no_comment').remove();



               } else {
                   $('#comment-error').text(data.message);
               }
           },
           // 请求失败的回调函数
           error: function (xhr) {
               console.log(xhr)
           }
       });
       return false
   });
});

