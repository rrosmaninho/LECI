let login = document.getElementById("login");
let signup = document.getElementById("signup");

function loginAction(username, password) {
    if(typeof(username)==='undefined') username = $("#username-login").val();
    if(typeof(password)==='undefined') password = $("#password-login").val();
    if (username == "" | password == "") {
        // alert("Please check if username or password is missing!");
        return false
    } else {
        $.post("/users/login", { username: username, password: password },
		function(response) {
            if (response["user"] == "User found") {
                localStorage.username = username
                localStorage.password = password
				login.classList.add("pointer-events-none")
				login.classList.replace("opacity-100", "opacity-0")
				signup.classList.add("pointer-events-none")
				signup.classList.replace("opacity-100", "opacity-0")
                return true
            } else {
                alert(response["user"])
                return false
            }
		});
    }	
}

function registerAction() {
	var username = $("#new-username-login").val();
	var password = $("#new-password-login").val();
    if (username == "" | password == "") {
        // alert("Please check if username or password is missing!");
        return false
    } else { 
        $.post("/users/register", { username: username, password: password },
		function(response) {
			if(response["user"] == "User created") {
				localStorage.username = username
                localStorage.password = password
				login.classList.add("pointer-events-none")
				login.classList.replace("opacity-100", "opacity-0")
				signup.classList.add("pointer-events-none")
				signup.classList.replace("opacity-100", "opacity-0")
                return true
			} else {
                alert(response["user"]);
                return false
			}
		});
    }
}