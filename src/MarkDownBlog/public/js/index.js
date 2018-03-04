// {% csrf_token %}
pages = 1;
pageNum = 1;

function generateArticle(article) {
    author = article.author;
    content = markdown.toHTML(article.content);
    cDate = new Date(article.ctime*1000);
    mDate = new Date(article.mtime*1000);
    strPath = article.path;
    title = article.title;
    icon = article.icon;

    cY = cDate.getFullYear() + '-';
    cM = (cDate.getMonth()+1 < 10 ? '0'+(cDate.getMonth()+1) : cDate.getMonth()+1) + '-';
    cD = cDate.getDate() + ' ';
    ctime = cY + cM + cD;

    str = '<article class="post post-list" itemscope="" itemtype="http://schema.org/BlogPosting"><div class="thumbnail"><a href="/readArticle?path=' + strPath +'">' +
          '<img src="/' + icon + '"' + 'srcset="' + icon +'"/>' + '</a></div><div class="info"><h2 itemprop="name headline" class="title">' +
          '<a name="title" href="javascript:void(0);" onclick="readArticle(' + strPath + ')"' + 'strpath="' + strPath + '">' + title + '</a></h2><span class="time">' +
          '<i class="iconfont icon-rili"></i>' + ctime + '</span><span class="comment">' +
          '<i class="iconfont icon-user"></i>' + author +                          
          '</span><p itemprop="post">' + content + '......'+'</p></div></article><div class="clearer"></div>';
        //   href="/readArticle?path=' + strPath +'"' +
    return str;
}

//底部分页
function generatePage(left, pageNum, pages, right) {
    str = '<nav class="navigator"><a href="javascript:void(0);" onclick="pre_page()" ><i  id="left" class="iconfont icon-angleleft" pagenum="' + left + '"></i></a>' +
          '<a id="pageNum">' + '-->' + pageNum + '/' + pages + '<--' + '</a>' +
          '<a href="javascript:void(0);" onclick="next_page()" ><i  id="right" class="iconfont icon-angleright" pagenum="' + right + '"></i></a>' +
          '</nav><div class="clearer"></div>';

    return str;
}

function getArticles(strPath, paging, pageNum, level) {
    $.ajax({
        type: "POST",
        url: "/getArticles/",
        data:  {
            "paging": paging,
            "pageNum": parseInt(pageNum),
            "level": level,
            "path": strPath,
        },
        dataType: "json",
        success: function(data) {
            if (data.success) {
                pages = data.pages;
                pageNum = data.pageNum;
                $("#sec").html("");
                data.articles.forEach(function(article) {
                    $("#sec").append(generateArticle(article));
                });

                $("#sec").append(generatePage(parseInt(pageNum)-1, pageNum, pages, parseInt(pageNum)+1));
                console.log($("a[name='title']"));
                $("a[name='title']").click(function() {
                    strPath = $(this).attr("strpath");
                    readArticle(strPath);
                }); 
            } else {
                console.log(data.msg)
            }
        },
        error: function(data) {
            $("#sec").html("").append("<a>抱歉，可能出现了一点错误</a>");
        }
    })
}


function next_page() {
        nextPage = $("#right").attr('pagenum');
        if (parseInt(nextPage) > parseInt(pages)) {
            return;
        } else {
            getArticles("/", true, nextPage, "all");
        }

        $('body,html').animate({scrollTop:0},1000);
        return false;
}

function pre_page() {
        prePage = $("#left").attr('pagenum');
        if (parseInt(prePage) <= 0) {
            return;
        } else {
            getArticles("/", true, prePage, "all");
        }

        //回到顶部
        $('body,html').animate({scrollTop:0},1000);
        return false;
}

$(function() {
    getArticles("/", true, '1', "all");
});

function generateArticle2(article) {
    author = article.author;
    content = markdown.toHTML(article.content);
    cDate = new Date(article.ctime*1000);
    mDate = new Date(article.mtime*1000);
    strPath = article.path;
    title = article.title;
    icon = article.icon;

    cY = cDate.getFullYear() + '-';
    cM = (cDate.getMonth()+1 < 10 ? '0'+(cDate.getMonth()+1) : cDate.getMonth()+1) + '-';
    cD = cDate.getDate() + ' ';
    ctime = cY + cM + cD;

    str = '<article class="postShorten postShorten--thumbnailimg-left" itemscope="" itemtype="http://schema.org/BlogPosting"><div class="postShorten-wrap"><div class="postShorten-header"><h1 class="postShorten-title" itemprop="headline">' +
    '<a class="link-unstyled" href="/hexo-theme-tranquilpeak/2015/05/28/Elements-showcase/">' + title + '</a></h1><div class="postShorten-meta">' + 
    '<time itemprop="datePublished" datetime="' + ctime + '">' + ctime +
    '</time><span> author: </span>' + 
    '<a class="category-link" href="/hexo-theme-tranquilpeak/categories/tranquilpeak/features/">' +author+'</a>' +
    '</div></div><div class="postShorten-excerpt" itemprop="articleBody"><p>' + content + 
    '<br><a href="/readArticle/' + strPath + '" class="postShorten-excerpt_link link">Continue reading</a></p></div></div>' + 
    '<a href="/hexo-theme-tranquilpeak/2015/05/28/Elements-showcase/">' + 
    '<div class="postShorten-thumbnailimg"><img alt="" itemprop="image" src="' + icon + '></div></a></article>';

    return str;
}

