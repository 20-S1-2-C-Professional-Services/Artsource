
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

function ArtistChoice(){
var artistinput=document.getElementById('artistsInput');
var artists=document.getElementById('artists');
if(artistinput.value.length>0){
    if(artists.value.length>0){
    artists.value=artists.value+" "+artistinput.value;
    }else{
        artists.value=artistinput.value;
    }
}
artistinput.value="";
}