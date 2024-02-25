// THEME SCRIPTS
let listUsers = []
let themeNum
let themeMode
let escAllowed = false

const pages = ["home", "gallery", "upload", "process", "about"]

// LOGIN

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
				document.getElementById("login").classList.add("pointer-events-none")
				document.getElementById("login").classList.replace("opacity-100", "opacity-0")
				document.getElementById("signup").classList.add("pointer-events-none")
				document.getElementById("signup").classList.replace("opacity-100", "opacity-0")
				escAllowed = true
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
				document.getElementById("login").classList.add("pointer-events-none")
				document.getElementById("login").classList.replace("opacity-100", "opacity-0")
				document.getElementById("signup").classList.add("pointer-events-none")
				document.getElementById("signup").classList.replace("opacity-100", "opacity-0")
				escAllowed = true
                return true
			} else {
                alert(response["user"]);
                return false
			}
		});
    }
}

document.onkeydown = function(event) {
	if (((event.key === "Escape") || (event.key == "Esc")) && (escAllowed == true)) {
		goTo(localStorage.page)
	}
}

function themeOnLoad() {
	if (!('theme' in localStorage)) {
		themeNum = 0
	} else if (localStorage.theme == 1) {
		themeNum = 1
	} else {
		themeNum = 2
	}
	switchTheme()
	setTimeout(() => {
		let splash = document.getElementById('splash')
		splash.classList.add('opacity-0')
	}, 1000);
}

function incrementThemeNum() {
	if (themeNum === 2) {
		themeNum = 0
		localStorage.removeItem('theme')
	} else {
		themeNum = themeNum + 1
		localStorage.theme = themeNum
	}
	switchTheme()
}

function switchTheme() {
	const icon = document.querySelector('#settings').querySelector('path')
	switch (themeNum) {
		case 0:
			if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
				document.documentElement.classList.add('dark')
				themeMode = "dark"
			} else {
				document.documentElement.classList.remove('dark')
				themeMode = "light"
			}
			icon.setAttribute('d', 'M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25')
			break
		case 1:
			document.documentElement.classList.add('dark')
			themeMode = "dark"
			icon.setAttribute('d', 'M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z')
			break
		case 2:
			document.documentElement.classList.remove('dark')
			themeMode = "light"
			icon.setAttribute('d', 'M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z')
			break
	} pageOnLoad()
}

// PAGE SCRIPTS

function pageOnLoad() {
	if ('page' in localStorage) {
		goTo(localStorage.page);
	} else {
        localStorage.page = "home";
        goTo("home");
	}
}

function goTo(page) {
	if(typeof(page)==='undefined') page = localStorage.page;

	let defaultClass = themeMode === "dark" ? "regular-button-dark" : "regular-button";
	let newClass = themeMode === "dark" ? "regular-button" : "regular-button-dark";

	if (page == "upload") {
		if (hidePopups()) {
			upload()
		}
	} else {
		pages.forEach((otherPage) => {
			document.getElementById(otherPage + "-sidebar").classList.replace(newClass, defaultClass)
			if (otherPage != "upload") {document.getElementById(otherPage).classList.add("hidden")}
		})
		hidePopups()
		document.getElementById(page + "-sidebar").classList.replace(defaultClass, newClass);
		document.getElementById(page).classList.remove("hidden");
		localStorage.page = page;
	}
}

function login(stage) {
	if(typeof(stage)==='undefined') stage = 0;
	let login = document.getElementById("login");
	let signup = document.getElementById("signup");

	document.getElementById("password-login").value = "";
	document.getElementById("username-login").value = "";
	document.getElementById("new-password-login").value = "";
	document.getElementById("new-username-login").value = "";

	clearImage()

	switch (stage) {
		case 0:
			// Display login
			login.classList.remove("pointer-events-none")
			login.classList.replace("opacity-0", "opacity-100")
			signup.classList.add("pointer-events-none")
			signup.classList.replace("opacity-100", "opacity-0")
			break
		case 1:
			// Display register
			signup.classList.remove("pointer-events-none")
			signup.classList.replace("opacity-0", "opacity-100")
			login.classList.add("pointer-events-none")
			login.classList.replace("opacity-100", "opacity-0")
			break
	}
}

function signup() {
	let userlogin = document.getElementById("new-username-login").value;
	let passwordlogin = document.getElementById("new-password-login").value;
	let userPass = {
		user : userlogin,
		password : passwordlogin
	};

	let userExists = false;

	for(i = 0; i < listUsers.length; i++){
		if(listUsers[i].hasOwnProperty("user") && listUsers[i].user === userlogin){
			userExists = true;
			break;
		}
	}
	if(!userExists){
		listUsers.push(userPass);
	}

	document.forms[0].reset();
}

function logout() {
	localStorage.username = ""
	localStorage.password = ""
	login(0)
}

function upload() {
	document.getElementById("pages").classList.add("overflow-hidden");
	document.getElementById("upload").classList.remove("pointer-events-none");
	document.getElementById("upload").classList.replace("opacity-0", "opacity-100");
}

function hidePopups() {
	if (loginAction(localStorage.username, localStorage.password) == false) {
		login(0)
		return false
	} else {
		let upload = document.getElementById("upload");
	
		document.getElementById("nameImg").value = "";
		document.getElementById("authorImg").value = "";
	
		document.getElementById("pages").classList.remove("overflow-hidden");
	
		upload.classList.add("pointer-events-none");
		upload.classList.replace("opacity-100", "opacity-0");
	
		clearImage();
		return true
	}

}

// Image Upload functions

var file

function updatePhoto(event) {
    document.getElementById("image_display_area").classList.remove("hidden");
    var reader = new FileReader();
	reader.onload = function(event) {
		var img = new Image();
		img.onload = function() {
			const canvas = document.getElementById("photo");

			let aspectRatio = (img.width / img.height).toFixed(1);
			let maxSize = 32;

			if (aspectRatio > 2) {
				width = maxSize * 2
				height = maxSize / (aspectRatio/2)
			} else if (aspectRatio == 2) {
				width = maxSize * 2;
				height = maxSize;
			} else if ((aspectRatio < 2) && (aspectRatio > 1)) {
				width = maxSize * 2 / aspectRatio;
				height = maxSize;
			} else if (aspectRatio == 1) {
				width = maxSize;
				height = maxSize;
			} else if (aspectRatio < 1) {
				width = maxSize * aspectRatio;
				height = maxSize;
			}

			clearImage()
			canvas.classList.add(`h-[${Math.round(height)}rem]`);
			canvas.classList.add(`w-[${Math.round(width)}rem]`);
			canvas.src = img.src;
		}
		img.src = event.target.result;
	}
	file = event.target.files[0];
	reader.readAsDataURL(file);
}

function clearImage() {
	const canvas = document.getElementById("photo")
	let hClasses = [...canvas.classList].filter(className => className.startsWith('h-'));
	hClasses.forEach(className => canvas.classList.remove(className));
	let wClasses = [...canvas.classList].filter(className => className.startsWith('w-'));
	wClasses.forEach(className => canvas.classList.remove(className));
	canvas.src = ""
}

function uploadImage() {
	if (file != null) {
		sendFile(file);
	} else {
		fileMissing();
		failed_upload();
	}
}

function sendFile(file) {
    var data = new FormData();
    var name = document.getElementById('nameImg').value;
    var author = document.getElementById('authorImg').value;
    data.append("myFile", file);
	data.append("myName", name);
	data.append("myAuthor", author);
	
	if (name == "" && author == "") { 
		missing_image_name();
		missing_author_name();
		failed_upload();
	} else if (name == "") {
		missing_image_name();
		failed_upload();
	} else if (author == "") {
		missing_author_name();
		failed_upload();
	} else {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload");
        xhr.upload.addEventListener("progress", updateProgress(this), false);
        xhr.send(data);
	}
	window.location.reload();
}

function updateProgress(evt){
    if (evt.loaded == evt.total) {
        var upload_btn = document.getElementById("uploadbutton");
        upload_btn.classList.remove("btn-outline");
		upload_btn.classList.replace("btn-accent", "btn-success");
        setTimeout(function () { upload_btn.classList.replace("btn-success", "btn-accent"); upload_btn.classList.add("btn-outline"); hidePopups() }, 1000);
	}
}

function failed_upload() {
    var upload_btn = document.getElementById("uploadbutton");
	upload_btn.classList.remove("btn-outline");
    upload_btn.classList.replace("btn-accent", "btn-error");
    setTimeout(function () { upload_btn.classList.replace("btn-error", "btn-accent"); upload_btn.classList.add("btn-outline"); }, 2500);
}

function fileMissing() { 
    var element = document.getElementById("add_file_button");
	element.classList.remove("btn-outline");
    element.classList.replace("btn-primary", "btn-error");
    setTimeout(function () { element.classList.replace("btn-error", "btn-primary"); element.classList.add("btn-outline") }, 2500);
}

function missing_image_name() {
    let label = document.getElementById("image-label")
    label.classList.add("text-red-400")
    setTimeout(function () { label.classList.remove("text-red-400") }, 5000);
}

function missing_author_name() {
	let label = document.getElementById("author-label")
    label.classList.add("text-red-400")
    setTimeout(function () { label.classList.remove("text-red-400") }, 5000);
}