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
                let input = document.createElement("input");
                input.type = "hidden";
                input.name = "receiver";
                input.value = element;
                $("#navbarForm").append(input);
                $("#navbarForm").submit();
            }
            $("#left").append(button);
        });

        console.log(objects);
    }
    else {
        console.error(xhr);
    }
};
xhr.send();



// $("#left").append($('<form action="" method="POST" id = "lolForm">' + 
//     '<input type="hidden" name="receiver" value="sonali42">' +
//     '<input type="submit" style = "display:none">' +
//     '</form>'));

// $("#left").on("click", () => {
//     $("#lolForm").submit();
// });