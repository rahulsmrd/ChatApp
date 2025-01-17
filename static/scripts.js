document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        hideAllChats();
    }
});


var present_group = '';
var present_user = '';
const chatPanel = document.getElementById("chatPanel");

function scrollToBottom(chatContainerId) {
    const chatContainer = document.getElementById(chatContainerId);

    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

function openChat(id, user) {
    hideAllChats();
    var user_id = parseInt(user);
    var other_id = parseInt(id);
    if (user_id > other_id) {
        present_group = user_id + "-" + other_id;
    } else {
        present_group = other_id + "-" + user_id;
    }
    present_user = user
    var chat = document.querySelector(`#chat-${present_group}`);
    var chat_user = document.querySelector(`#chat-${present_group} .userinfo`);
    var newChat = document.querySelector('.newChat');
    if (!chat) {
        newChat.style.display = 'block';
        var conatiner = document.querySelector('.newChat div');
        var input = document.querySelector('.newChat input');
        conatiner.setAttribute('id', `chat_container_${present_group}`);
        input.setAttribute('id', `messageInput_${present_group}`);

    }
    else{
    chat.style.display = 'block'
    chat_user.style.display = 'block';
    }
    openSocket(id);
    scrollToBottom(`chat-${present_group}`);
}

function hideAllChats() {
    const divs = chatPanel.querySelectorAll("div");

    divs.forEach((div) => {
        div.style.display = "none";
    });
}





function openSocket(id) {
    const chatSocket = new WebSocket("ws://" + window.location.host + `/ws/chat/${id}/`);
    chatSocket.onopen = function (e) {
        console.log("The connection was setup successfully !");
    };
    chatSocket.onclose = function (e) {
        console.log("Something unexpected happened !");
    };
    document.querySelector(`#messageInput_${present_group}`).focus();
    document.querySelector(`#messageInput_${present_group}`).onkeyup = function (e) {
        if (e.keyCode == 13) {
            document.querySelector("#sendMessage").click();
        }
    };
    document.querySelector("#sendMessage").onclick = function (e) {
        var messageInput = document.querySelector(
            `#messageInput_${present_group}`
        ).value;
        chatSocket.send(JSON.stringify({ message: messageInput, username: "{{request.user.username}}" }));
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (!data.sender || !data.message) {
            return;
        }

        var p = document.createElement("p");
        var span = document.createElement("span");

        if (data.sender == `${present_user}`) {
            p.classList.add('toUser');
            span.classList.add('toUserTime');
        }
        else {
            p.classList.add('fromUser');
            span.classList.add('fromUserTime');
        }
        p.innerHTML = data.message;
        span.innerHTML = data.time;
        document.querySelector(`#messageInput_${present_group}`).value = "";
        var chat_container = document.querySelector(`#chat_container_${present_group}`);
        chat_container.style.display = 'block';
        chat_container.appendChild(p);
        chat_container.appendChild(span);
        scrollToBottom(`chat-${present_group}`);
    };
};