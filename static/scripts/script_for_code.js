const socket = io();
function ask_about_players(){
    let players = $("#players").val();
    let text1 = document.getElementById("game");
    let text = text1.textContent;
    d = {"players":players,
    "text":text
    };

    socket.emit("is_there_new_player",d);
}
// var test = document.getElementById( 'test' );

// // To get the text only, you can use "textContent"
// console.log( test.textContent ); // "1 2 3 4"
socket.on("new player",(d)=>{
    let players = $("#players").val();
    players = players + d["playername"];
    $("#players").val(players);
});
socket.on("players_list",(players_list)=>{
    console.log(players_list);
    const players_list_1 = new Array ();
    let players_str = "";
    for (let i = 0; i < players_list.length; i++){
        players_str += players_list[i];
        players_str += "\n";
    }
    $("#players").text(players_str);
});
setInterval(ask_about_players,1000);
// $(document).ready(() => {
//     socket.emit("checkuser");
// });

// function changePrices(){
//     socket.emit("changePrices");
// }

// const socket = io();

// function send_private(){             //это уже не send_private, а отправка private, если указан user
//     let user = $("#user").val();
//     console.log(user, 1);
//     //let private_message = $("#private_message").val();
//     let message = $("#input").val();
//     $("#user").val("");
//     $("#input").val("");
//     if (user == ""){
//         //socket.emit("message",{user:user,message:message});
//         socket.emit("message",{message:message});
//     }
//     else{
//         socket.emit("private_message",{user:user,private_message:message});
//     }
    
// }

// $("#send").on("click",()=>{
//     send_private()
//     // let text = $("#input").val();
//     // socket.emit("message",text);
//     // $("#input").val("");
// });
// $("#buy_button").on("click",()=>{
//     let name = $("#share_name").val();
//     let amount = $("#share_amount").val();
//     socket.emit("buying_shares",{name:name,amount:amount})
//     $("#share_name").val("");
//     $("#share_amount").val("");
// });
// // $("#send_private").on("click",)
// socket.on("server_message",(data)=>{
//     var ta = document.querySelector('textarea');
//     console.log(data.name,data.text);
//     ta.value += `${data.name}: ${data.text.message}\n`;    
//     ta.focus();
//     var block = document.getElementById("chat");
//     block.scrollTop = block.scrollHeight;
//     // $("#chat").append(`<p> ${text} </p>`);
// });
// socket.on("new_private_message",(data)=>{
//     var ta = document.querySelector('textarea');
//     ta.value += `${data}\n`;  
// });
// socket.on("updatePage",(d)=>{
//     $("#tinkoff").text("Tinkoff: "+d["Tinkoff"]);
//     $("#gasprom").text("Gasprom: "+d["Gasprom"]);
//     $("#gaspromoil").text("Gasprom oil: "+d["Gasprom oil"]);
//     $("#sber").text("Sber: "+d["Sber"]);
// });
// socket.on("update_user_things",(d)=>{
//     $("#balance span").text(d["balance"]);
//     d['shares'].forEach((elem, id) => {
//          $(`#share-${elem[0]} span`).text(elem[2]);
//          });
//      //РЕЗУЛЬТАТ [('sber', 'Sber', 16), ('gaspromoil', 'Gasprom oil', 5), ('gasprom', 'Gasprom', 11), ('tinkoff', 'Tinkoff', 6)]
//  });
// // setTimeout(changePrices,5000);
// setInterval(changePrices,5000);