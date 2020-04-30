
function verificationPicFile(file) {
    var fileSize = 0;
    var fileMaxSize = 2048;//2M
    var filePath = file.value;
    if(filePath){
        fileSize =file.files[0].size;
        var size = fileSize / 1024;
        if (size > fileMaxSize) {
            alert("size of image should less than 2 MB!");
            file.value = "";
            return false;
        }else if (size <= 0) {
            alert("The size of image should be greater than 0 MB!");
            file.value = "";
            return false;
        }else{
            verificationPicFile3(file);
        }
    }else{
        return false;
    }
}

function verificationPicFile3(file) {
    var filePath = file.value;
    if(filePath){
        //read image data
        var filePic = file.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            var data = e.target.result;
            //load the data
            var image = new Image();
            image.onload=function(){
                document.getElementById("image").appendChild(image);
                canvas_thumbnail = AutoSize(image,600,400);
                //save as jpeg
                $('#thumbnail').val(canvas_thumbnail.toDataURL("image/jpeg"));
            };
            image.src= data;
        };
        reader.readAsDataURL(filePic);
    }else{
        return false;
    }

}

function AutoSize(Img, maxWidth, maxHeight) {

var expectratio = maxWidth/maxHeight
var canvas = document.createElement("canvas");
canvas.width = maxWidth;
canvas.height = maxHeight;

if(Img.width>Img.height*expectratio){
    var expectwidth = Img.height*expectratio;
    canvas.getContext("2d").drawImage(Img, 0, 0,expectwidth,Img.height,0,0,maxWidth,maxHeight);
}else if(Img.height>Img.width/expectratio){
    var expectheight = Img.width/expectratio;
    canvas.getContext("2d").drawImage(Img, 0, 0,Img.width,expectheight,0,0,maxWidth,maxHeight);
}else{
    if(Img.width>Img.height){
        canvas.getContext("2d").drawImage(Img, 0, 0,Img.width,Img.width/expectratio,0,0,maxWidth,maxHeight);
    }else{
        canvas.getContext("2d").drawImage(Img, 0, 0,Img.height*expectratio,Img.height,0,0,maxWidth,maxHeight);
    }
}


return canvas;

}