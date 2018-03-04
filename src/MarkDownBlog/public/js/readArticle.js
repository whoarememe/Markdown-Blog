function readArticle(strPath) {
    $.ajax({
        type: "POST",
        url: "/getAnArticle/",
        data: {"path": strPath},
        dataType: "json",
        success: function(data) {
            if (data.success) {
                $("#sec").html("");
                $(".header-bg-mask").after('<div id="readarticle" class="well article"></div>');
                // $("#sec").attr("width", "1080px");
                console.log(data.article);
                content = markdown.toHTML(data.article.content);
                $("#readarticle").html(content);
            }
        },
        error: function(data) {
            console.log("error");
        }
    })
}

