$(function () {
   $('#send_code').click(function () {
       $('form').attr('action', '');
       var $email = $('#id_email').val();
       if ($email==''){
           $('#tip').text('*邮箱不能为空')
       } else {
           // 发送验证码
           $.ajax({
               url: '/user/bind_email_send_code/?email=' + $email,
               type: 'GET',
               // date: {
               //     'email': $email
               // },
               cache: false,
               success: function (data) {
                   if (data['status'] == 'ERROR') {
                       alert(data['status']);
                   }
               }
           })
       }

       // 将获取验证码按钮变灰
       $(this).addClass('disabled');
       $(this).attr('disabled', true);
       var time = 30;
       $(this).text(time + 's');
       var interval = setInterval(() => {
           if (time <= 0) {
               clearInterval(interval);
               $(this).removeClass('disabled');
               $(this).attr('disabled', false);
               $(this).text('发送验证码');
               return false;
           }
           time --;
           $(this).text(time + 's');
       }, 1000);
   })
});