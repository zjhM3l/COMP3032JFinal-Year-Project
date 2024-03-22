//check if the email has already been token
function checkEmail() {
    var req = new XMLHttpRequest();
    req.open('post', '/checkEmail', true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("email=" + email.value);
    req.onload = function () {
        var json = JSON.parse(req.responseText);
        if (json.returnvalue == 1) {
            //use javascript to change css
            msg.innerText = 'Sorry, email is already token';
            msg.style.color = "red";
        } else if (json.returnvalue == 0) {
            //use javascript to change css
            msg.innerText = 'Email is available';
            msg.style.color = "black";
        } else if (json.returnvalue == 2) {
            //use javascript to change css
            msg.innerText = 'Email format error';
            msg.style.color = "red";
        }
    };
}

//check the passward strength
function passwordStrength() {
    var req = new XMLHttpRequest();
    req.open('post', '/passwordStrength', true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("password=" + password.value);
    req.onload = function () {
        var json = JSON.parse(req.responseText);
        if (json.returnvalue == 1) {
            //use javascript to change css
            strength.innerText = 'low strength';
            strength.style.color = "red";
        } else if (json.returnvalue == 2) {
            //use javascript to change css
            strength.innerText = 'medium strength';
            strength.style.color = "orange";
        } else if (json.returnvalue == 3) {
            //use javascript to change css
            strength.innerText = 'strong strength';
            strength.style.color = "blue";
        } else if (json.returnvalue == 4) {
            strength.innerText = 'very strong strength';
            //use javascript to change css
            strength.style.color = "green";
        }
    };
}

//check if the passwords are the same
function checkPassword() {
    var password = $("input[name='password']").val();
    var password2 = $("input[name='password2']").val();
    if (password == password2 && password2.length !== 0) {
        updateMessage(pass, 'Correct', 'black');
    } else if (password != password2) {
        updateMessage(pass, 'Sorry, the password does not match', 'red');
    }
}

function updateMessage(element, text, color) {
    element.innerText = text;
    element.style.color = color;
}

$(document).ready(function () {
    $("#register-btn").click(function () {
        $.ajax({
            url: "/send_message",
            type: "POST",
            success: function (data) {
                alert(data.message);
            }
        });
    });
});

$(document).ready(function () {
    $("#login-btn").click(function () {
        $.ajax({
            url: "/send_message2",
            type: "POST",
            success: function (data) {
                alert(data.message);
            }
        });
    });
});

