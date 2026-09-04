let apiUrl = "https://yanghuangluo.pythonanywhere.com/api";

async function getApi(){
    try{
        let res = await fetch(apiUrl);
        let rawText = await res.text();
        console.log("原始返回：",rawText);
        let data = JSON.parse(rawText);
        alert("服务器数据："+data.msg);
    }catch(err){
        console.error("错误：",err);
    }
}
getApi();
