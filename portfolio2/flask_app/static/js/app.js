const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const colors = document.getElementsByClassName("color");
const saveBtn = document.getElementById("save");

CANVAS_SIZE = 500;

canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

ctx.fillStyle = "white";
ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

ctx.strokeStyle = "#000000";
ctx.lineWidth = 8;

let painting = false;

function stopPainting() {
    painting = false;
}

function startPainting() {
    painting = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if(!painting) {
        ctx.beginPath();
        ctx.moveTo(x, y);
    }else{
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

function onMouseDown(event) {
    painting = true;
}

function onMouseUp(event) {
    stopPainting();
}

if(canvas){
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("mouseup", stopPainting);
    canvas.addEventListener("mouseleave", stopPainting);
}

function handleColorClick(event) {
    const color = event.target.style.backgroundColor;
    ctx.strokeStyle = color;
    if(color === "black"){
        ctx.lineWidth = 8;
    }else{
        ctx.lineWidth = 30;
    }
}

Array.from(colors).forEach(color =>
    color.addEventListener("click", handleColorClick));

if(saveBtn){
    saveBtn.addEventListener("click", handleSaveClick);
}

function handleSaveClick(){
    var dataURL = canvas.toDataURL();
    $.ajax({
        type: 'POST',
        url: '/result',
        data:{
            'imageBase64': dataURL
        }
        // processData : false,	// data 파라미터 강제 string 변환 방지!!
        // contentType : false	// application/x-www-form-urlencoded; 방지!!
    }).done(function() {
        window.location.href = '/result2';
        console.log('sent');
    });
    // window.location.href = '/result2';
    // var dataURL = canvas.toDataURL("image/png");
    
    // var imgURL = canvas.toDataURL();
    // $.ajax({
    //     type: "POST",
    //     url: "/result", //I have doubt about this url, not sure if something specific must come before "/take_pic"
    //     data: {data: dataURL},
    //     success: function(data) {
    //       if (data.success) {
    //         alert('Your file was successfully uploaded!');
    //       } else {
    //         alert('There was an error uploading your file!');
    //       }
    //     },
    //     error: function(data) {
    //       alert('There was an error uploading your file!');
    //     }
    //   }).done(function() {
    //     console.log("Sent");
    //   });
}