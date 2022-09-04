var handler = function (captchaObj) {
    captchaObj.appendTo('#captcha');
    captchaObj.onReady(function () {
        $("#wait").hide();
    });
    $("#done").click(function(){
        var result = captchaObj.getValidate();
        if (!result) {
            alert("请完成验证");
        }
        else {
            var validate = result.geetest_validate;
            var seccode = result.geetest_seccode;
            window.location.href = window.location.href + "result/validate=" + validate + "&seccode=" + seccode;
        }
    });
    // 更多前端接口说明请参见：http://docs.geetest.com/install/client/web-front/
};
$('#wait').show();
// 调用 initGeetest 进行初始化
// 参数1：配置参数
// 参数2：回调，回调的第一个参数验证码对象，之后可以使用它调用相应的接口
initGeetest({
    // 以下 4 个配置参数为必须，不能缺少
    gt: {Python_Interface: GT}, // 这里需要替换成 python 获取的 gt
    challenge: {Python_Interface: CHALLENGE}, // 这里需要替换成 python 获取的 challenge
    offline: false, // 表示用户后台检测极验服务器是否宕机
    new_captcha: true, // 用于宕机时表示是新验证码的宕机

    product: "popup", // 产品形式，包括：float，popup
    width: "300px",
    https: true

    // 更多前端配置参数说明请参见：http://docs.geetest.com/install/client/web-front/
}, handler);
