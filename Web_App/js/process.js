function sendinfo2() {
    var id = document.getElementById("fname").value;
	var filter_option = document.getElementById("process_select").value;
	$.get("/imageproc",
		{ idimg : id , filter : filter_option},
		function(response){
			originalimage(response);
		});
}


function reload() {
	window.location.reload();
}

function originalimage(response) {
	// response.image is the image information
	full_path = "../"+response.image.path;
	full_path2 = "../"+response.image2.path2;
	$("#imageoriginal").html("");
	$("#imageoriginal").append("<p>Author: "+ response.image.author +" </p>"+"<p>Name: "+response.image.name+"</p>"+"<p>Date and Time: "+response.image.datetime+"</p>");
	// html code for showing the image
	$("#imageoriginal").append("<img width='550px' height='450px' src='"+full_path+"' alt='image'>");
	// html code for showing the filtered image
	$("#imagefilter").html("");
	$("#imagefilter").append("<button onclick='reload()' class='button btn btn-accent dark:btn-neutral' type = 'submit' style = 'margin-left: 155px; margin-bottom: 35px;'>Reload Page To Apply New Filter</button>");
	$("#imagefilter").append("<img width='550px' height='450px' src='"+full_path2+"' alt='image'>");
}
