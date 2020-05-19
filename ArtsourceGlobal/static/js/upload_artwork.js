

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

var x;
var y;
var width;
var height;
var image = new Image();
var originalWidth;
var originalHeight;
function verificationPicFile3(file) {
    var filePath = file.value;
    if(filePath){
        //read image data
        var filePic = file.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            var data = e.target.result;
            //load the data
            image.src= data;
            var $preview = $('#demoImg');
            // Get the Cropper.js instance after initialized
            // var cropper = $preview.data('cropper');
            image.onload=function(){
                originalHeight=image.height;
                originalWidth=image.width;
                var canvas_thumbnail = AutoSize(image,400,300);
                //save as jpeg
                $('#thumbnail').val(canvas_thumbnail.toDataURL("image/jpeg"));
                document.getElementById('cropbtn').style.display="";
                $preview.cropper('destroy');
                $preview.attr('src', image.src);
                $preview.attr('height',image.height);
                $preview.attr('width',image.width);
                 $preview.cropper({
                  aspectRatio: 4/ 3,
                  crop: function(event) {
                    x=event.detail.x;
                    y=event.detail.y;
                    width=event.detail.width;
                    height=event.detail.height;
                  }
                });
            };

        };
        reader.readAsDataURL(filePic);

    }else{
        return false;
    }
}


function drawImage(){
    var canvas = document.createElement("canvas");
    canvas.width=originalWidth;
    canvas.height=originalHeight;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(image, 0,0);
    var imgData=ctx.getImageData(x,y,width,height);
    // var currentWidth;
    // currentWidth= width-x;
    // var currentHeight;
    // currentHeight= height-y;
    canvas.width=width;
    canvas.height=height;
    ctx.putImageData(imgData,0,0);
    var result =new Image();
    result.src= canvas.toDataURL("image/jpeg");
    result.onload=function () {
        var canvas2 = document.createElement("canvas");
        canvas2.width=400;
        canvas2.height=300;
        canvas2.getContext("2d").drawImage(result,0,0,width,height,0,0,400,300);
        $('#thumbnail').val(canvas2.toDataURL("image/jpeg"));
        $('#croppedImage').attr('src',canvas2.toDataURL("image/jpeg"));
    }
    //Mark the image as uploaded.
    document.getElementById("croppedImage").setAttribute("doesExist", "true");
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