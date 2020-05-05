
function TagChoice(){
var taginput=document.getElementById('tagsInput');
var tags=document.getElementById('tags');
if(taginput.value.length>0){
    if(tags.value.length>0){
    tags.value=tags.value+" "+taginput.value;
    }else{
        tags.value=taginput.value;
    }
}
taginput.value="";
}