alert("Hello, World!");
a = prompt("注册或登录：");
my_name = prompt("请输入用户名：");
password = prompt("请输入密码：");
if (a == "注册"){
    alert("功能正在开发中");
    alert("注册成功！");
}else if (a == "登录"){
    alert("功能正在开发中");
    alert("登录成功！");
}else{
    alert("功能正在开发中");
}
alert("hello " + my_name);
const link = document.querySelector('#土耳其的首都');
link.onclick = function Ankara() {
    alert("土耳其的首都是什么城市");
    c = prompt("请输入答案：");
    if (c == "安卡拉") {
        alert("回答正确！");
        this.href = "b.html";
    }else if (c == "伊斯坦布尔" || c == "君士坦丁堡") {
        alert("回答错误！");
        alert("土耳其不是奥斯曼");
    }
    else{
        alert("回答错误！");
    }
}
Ankara()
