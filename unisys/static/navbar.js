let formdata = new FormData();
formdata.append("receiver", "sonali42");

let xhr = new XMLHttpRequest();
xhr.open('GET', window.location.origin+"/getUsers", true);
xhr.onload = function () {
    if (this.status === 200) {
        let objects = JSON.parse(this.response);
        let usernames = objects.usernames;

        usernames.forEach(element => {
            let button = document.createElement("button");
            button.innerHTML = element;
            button.onclick = () => {
                console.log("clicked for user:"+element);
                //input to submit for post
                let input = document.createElement("input");
                input.type = "hidden";
                input.name = "receiver";
                input.value = element;
                //submit it
                $("#sidebar-form").append(input);
                $("#sidebar-form").submit();
            }

            //div for containing the button and other stuff
            let div = document.createElement("div");
            div.setAttribute("class", "usrBtnCon");
            div.onclick = () => button.click();
            if(typeof remoteUser !== undefined && remoteUser !== "404_ERR_NOT_FOUND")
            {
                if(element === remoteUser)
                    div.setAttribute("class", "usrBtnCon selected");
            }   
            div.appendChild(button);

            $(".user-list").append(div);
        });

        console.log(objects);
    }
    else {
        console.error(xhr);
    }
};
xhr.send();


// $(".usrBtnCon").each( (index, value) => {
//         console.log("lol");
//         if (this.children[0].innerHTML() === remoteUser)
//             div.addClass("selected");
//     });



// $("#left").append($('<form action="" method="POST" id = "lolForm">' + 
//     '<input type="hidden" name="receiver" value="sonali42">' +
//     '<input type="submit" style = "display:none">' +
//     '</form>'));

// $("#left").on("click", () => {
//     $("#lolForm").submit();
// });