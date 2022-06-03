const socket = io();
function ask_about_quiz(){
    socket.emit("quiz_started","123");
    console.log("test");
}
$("#firstbutton").on("click",()=>{
    $("#chosen_button").text("Вы выбрали первый ответ");
    socket.emit("player_answered","1");
});
$("#secondbutton").on("click",()=>{
    $("#chosen_button").text("Вы выбрали второй ответ");
    socket.emit("player_answered","2");
});
$("#thirdbutton").on("click",()=>{
    $("#chosen_button").text("Вы выбрали третий ответ");
    socket.emit("player_answered","3");
});
$("#fourthbutton").on("click",()=>{
    $("#chosen_button").text("Вы выбрали четвёртый ответ");
    socket.emit("player_answered","4");
});
setInterval(ask_about_quiz,1000);