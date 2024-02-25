var id;

$(document).ready(
    function(){
        const params = new URLSearchParams(window.location.search);
        id = params.get("id");
        imagecomments ();
    });      

function imagecomments() {
	$.get("/comments",
		{ idimg : id },
		function(response){
			showimageandinfo(response);
		});
}

function showimageandinfo(response) {
	var full_path = "../" + response.image.path;
	
	// Create a new Image object
	var img = new Image();
	img.src = full_path;

	// Wait for the image to load
	img.onload = function() {
		let aspectRatio = (img.width / img.height).toFixed(1);
		let maxSize = 64;
		
		if (aspectRatio > 2) {
			width = maxSize * 2;
			height = maxSize / (aspectRatio / 2);
		} else if (aspectRatio === 2) {
			width = maxSize * 2;
			height = maxSize;
		} else if (aspectRatio < 2 && aspectRatio > 1) {
			width = maxSize;
			height = maxSize / aspectRatio;
		} else if (aspectRatio === 1) {
			width = maxSize;
			height = maxSize;
		} else if (aspectRatio < 1) {
			width = maxSize * aspectRatio;
			height = maxSize;
		}

		console.log(width, height, aspectRatio)

		// Display the image with the calculated aspect ratio
		$("#imageinfo").append("<img style='width: " + width + "rem; height: " + height + "rem; max-width: 128 rem; max-height: 64 rem;' src='" + full_path + "' alt='image'>");
	};

	// response.image is the image information
	// response.comments is the image list comments
	// response.votes is the image votes
	full_path = "../"+response.image.path;
	$("#imageinfo").html("");
	$("#imageinfo").append("<p>Author: "+ response.image.author +" </p>"+"<p>Name: "+response.image.name+"</p>"+"<p>Path: "+full_path+"</p>");
	// html code for showing the image
	// html code for showing the image comments
	$("#comments").html("");
	for (let i = 0; i < response.comments.length; i++) {
		$("#comments").append("<p>Username: "+response.comments[i].user+"</p>"+"<p>Comment: "+response.comments[i].comment+"</p>");
	}
	// html code for showing the image votes
	$("#thumbs_up").html("");
	$("#thumbs_up").append("<p>Thumbs up: "+response.votes.thumbs_up+"</p>");
	$("#thumbs_down").html("");
	$("#thumbs_down").append("<p>Thumbs down: "+response.votes.thumbs_down+"</p>");
}

function newcomment() {
	// obtain the user and comment from image page
	var user = document.getElementById("user").value;
	var comment = document.getElementById("comment").value;
	
	if (user == "" || comment == "") alert("Missing comment and/or username!");
	else {
		$.post("/newcomment",
			{ idimag: id, username: user, newcomment: comment },
			function() { imagecomments(); });
	}
}

function upvote() {
	$.post("/upvote",
		{ idimag: id },
		function() { imagecomments(); });
}

function downvote() {
	$.post("/downvote",
		{ idimag: id },
		function() { imagecomments(); });
}