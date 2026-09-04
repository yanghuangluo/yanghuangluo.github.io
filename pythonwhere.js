async function getAPI(){
  const apiURL "https://yanghuangluo.pythonwhere.com/api";
  try{
    const res = await fetch(apiURL);
    const rawTEXT = await res.text();
    console.log(rawTEXT);
    const data = JSON.parse(resTEXT);
    alert(data.msg);
  }catch(err){
    console.error(err);
  }
}
getAPI();
