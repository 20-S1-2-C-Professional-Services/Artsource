
function TagChoice()
{
    var taginput = document.getElementById('tagsInput');
    var tags = document.getElementById('tags');
    if(taginput.value.length > 0)
    {
        cleanedInput = cleanInputValue(taginput.value);
        if(tags.value.length>0)
        {
            tags.value = tags.value + " "+ cleanedInput;
        }
        else
        {
            tags.value = cleanedInput;
        }
    }
    taginput.value = "";
}

//Make the input more robust, can be expanded on later
function cleanInputValue(startingValue)
{
    while(startingValue.includes("  ") || startingValue.includes(","))
    {
        startingValue = startingValue.replace(",", " ");
        startingValue = startingValue.replace("  ", " ")
    }
    return startingValue;
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