$(document).ready(function() {
    $("#cmt").on("click", function() {
        $.ajax({
                type: "POST",
                url: "http://localhost:8000/blog/comment/" + $("#post-id").val() + "/",
                data: JSON.stringify({
                    content: $("#content").val(),
                    author_id: $("#user-id").val()
                }),
            })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function(json) {
                alert("Thanh cong")
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function(xhr, status, errorThrown) {
                alert("that bai");
            })
    });
    $("#test").on("click", function() {
        alert("asdf")
    })
});