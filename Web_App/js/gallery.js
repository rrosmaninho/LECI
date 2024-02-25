$(document).ready(
	function(){
		imageslist("all");
    });

function imageslist(id) {
	var author;
	if (id == "all") author = "all";
	else {
			author = $("#authorImg").val();
			if (author == "") author = "all";
	}
	$.get("/list",
		{ id : author },
		function(response){
			showimages(response);
		});
}

function showimages(response) {
	$("#showimages").html("");
	for (let i = 0; i < response.images.length; i++) {
		let image = response.images[i];
		let full_path = "../" + image.path;

		// Create a new div element
		let div = $("<div>").addClass("flex-auto mt-10 card w-72 bg-gray-200 dark:bg-base-100 shadow-md").attr("onclick", "showimagecomments(" + image.id + ")");

		// Create the figure element with the image
		let figure = $("<figure>").append($("<img>").attr("src", full_path)).addClass("aspect-square object-cover");
		div.append(figure);

		// Create the card-body div with author and name
		let cardBody = $("<div>").addClass("card-body");
		cardBody.append($("<h2>").addClass("card-title").text(image.author));
		cardBody.append($("<p>").text(image.name));
		cardBody.append($("<p>").text("ID: "+image.id+""));
		div.append(cardBody);

		// Append the new div to the showimages div
		$("#showimages").append(div);
	}
}

function showimagecomments(id) {
	window.open("../html/image.html?id=" + id, '_blank');
}
