( function( $ ) {
    btn_click("#topMenu", "menu_click", "menu_close"); //导航菜单
    btn_click("#Donate", "donate_click", "donate_close"); //捐赠
    btn_click("#mClick", "mobile_click", "mobile_close"); //二维码
    function btn_click(btn, on, off) {
        flag = true;
        $(btn).click(function () {
            $(btn).prop('class', (flag = !flag) ? on : off);
        });
    }
    //搜索
    $(".search_click").click(function () {
        $("body").addClass("search_bg");
        $(".search_key").focus();
        $(".search_close").click(function () {
            $("body").removeClass("search_bg");
        })
    })
    //评论
    $("#mobileComment").click(function () {
        $("body").addClass("comment_show");
        $("#comments").click(function () {
            $("body").removeClass("comment_show");
        })
    })
    //返回顶部
    $(".back2top").hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $(".back2top").fadeIn(200)
        } else {
            $(".back2top").fadeOut(200)
        }
        if ($(this).scrollTop() > 360) $("#header").addClass("fix");
        else $("#header").removeClass("fix");
    });
    $(".back2top").click(function () {
        return $("html,body").animate({scrollTop: 0}, 400);
    });


    //其它
    function other() {
        if (document.getElementsByClassName("navigation").length > 0) document.getElementsByClassName("navigation")[0].style.display = 'none';
        $("a[rel='external'],a[rel='external nofollow'],.post_article a").on('click', function () {
            window.open(this.href);
            return false
        });
    }
    other();
    $.fn.postLike = function () {
        if ($(this).hasClass('done')) {
            alert('点多了伤身体~');
            return false;
        } else {
            $(this).addClass('done');
            var id = $(this).data("id"),
                action = $(this).data('action'),
                rateHolder = $(this).children('.count');
            var ajax_data = {
                action: "dotGood",
                um_id: id,
                um_action: action
            };
            $.post("/wp-admin/admin-ajax.php", ajax_data,
                function (data) {
                    $(rateHolder).html(data);
                });
            return false;
        }
    };
    $(".dotGood").click(function () {
        $(this).postLike();
    });
    //Zepto.js版Ajax评论，兼容jQuery
    var i = 0, got = -1, len = document.getElementsByTagName('script').length;
    // while (i <= len && got == -1) {
    //     var js_url = document.getElementsByTagName('script')[i].src,
    //         got = js_url.indexOf('script.js');
    //     i++;
    // }
    // var ajax_php_url = themeAdminAjax.url,
    //     wp_url = js_url.substr(0, js_url.indexOf('wp-content')),
    //     txt1 = '<div id="loading">正在提交...</div>',
    //     txt2 = '<div id="error">#</div>',
    //     edit,
    //     num = 1,
    //     comm_array = [];
    // comm_array.push('');

    jQuery(document).ready(function ($) {
        $comments = $('#comments-title'); // 評論數的 ID
        $cancel = $('#cancel-comment-reply-link');
        cancel_text = $cancel.text();
        $submit = $('#commentform #submit');
        //$submit.attr('disabled', false);
        // $('#comment').after(txt1 + txt2);
        $('#loading').hide();
        $('#error').hide();
        $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');

        /** submit */
        $('#commentform').submit(function () {
            $('#loading').show();
            //$submit.attr('disabled', true);
            if (edit) $('#comment').after('<input type="text" name="edit_id" id="edit_id" value="' + edit + '" style="display:none;" />');

            /** ajax */
            $.ajax({
                url: ajax_php_url,
                data: $(this).serialize() + '&action=comment-submission',
                type: $(this).attr('method'),

                error: function (request) {
                    $('#loading').hide();
                    $('#error').show().html(request.responseText);
                    setTimeout(function () {
                        //$submit.attr('disabled', false);
                        $('#error').hide();
                    }, 3000);
                },
                success: function (data) {
                    $('#loading').hide();
                    comm_array.push($('#comment').val());
                    $('textarea').each(function () {
                        this.value = ''
                    });
                    var t = addComment, cancel = t.I('cancel-comment-reply-link'), temp = t.I('wp-temp-form-div'), respond = t.I(t.respondId), post = t.I('comment_post_ID').value, parent = t.I('comment_parent').value;

                    // comments
                    if (!edit && $comments.length) {
                        n = parseInt($comments.text().match(/\d+/));
                        $comments.text($comments.text().replace(n, n + 1));
                    }

                    // show comment
                    new_htm = '" id="new_comm_' + num + '"></';
                    new_htm = ( parent == '0' ) ? ('\n<ol style="clear:both;" class="commentlist' + new_htm + 'ol>') : ('\n<ul class="children' + new_htm + 'ul>');
                    $('#respond').before(new_htm);
                    $('#new_comm_' + num).hide().append(data);
                    $('#new_comm_' + num).show();
                    //$body.animate( { scrollTop: $('#new_comm_' + num).offset().top - 200},0);
                    scrollTop: $('#new_comm_' + num).offset().top;
                    countdown();
                    num++;
                    edit = ''; //$('*').remove('#edit_id');
                    cancel.style.display = 'none';
                    cancel.onclick = null;
                    t.I('comment_parent').value = '0';
                    if (temp && respond) {
                        temp.parentNode.insertBefore(respond, temp);
                        temp.parentNode.removeChild(temp)
                    }
                }
            }); // end Ajax
            return false;
        }); // end submit

        /** comment-reply.dev.js */
        addComment = {
            moveForm: function (commId, parentId, respondId, postId, num) {
                var t = this, div, comm = t.I(commId), respond = t.I(respondId), cancel = t.I('cancel-comment-reply-link'), parent = t.I('comment_parent'), post = t.I('comment_post_ID');
                if (edit) exit_prev_edit();
                num ? (
                    t.I('comment').value = comm_array[num],
                        edit = t.I('new_comm_' + num).innerHTML.match(/(comment-)(\d+)/)[2],
                        $new_sucs = $('#success_' + num), $new_sucs.hide(),
                        $new_comm = $('#new_comm_' + num), $new_comm.hide()
                ) : $cancel.text(cancel_text);

                t.respondId = respondId;
                postId = postId || false;

                if (!t.I('wp-temp-form-div')) {
                    div = document.createElement('div');
                    div.id = 'wp-temp-form-div';
                    div.style.display = 'none';
                    respond.parentNode.insertBefore(div, respond)
                }

                !comm ? (
                    temp = t.I('wp-temp-form-div'),
                        t.I('comment_parent').value = '0',
                        temp.parentNode.insertBefore(respond, temp),
                        temp.parentNode.removeChild(temp)
                ) : comm.parentNode.insertBefore(respond, comm.nextSibling);

                scrollTop: $('#respond').offset().top;

                if (post && postId) post.value = postId;
                parent.value = parentId;
                cancel.style.display = '';

                cancel.onclick = function () {
                    if (edit) exit_prev_edit();
                    var t = addComment, temp = t.I('wp-temp-form-div'), respond = t.I(t.respondId);

                    t.I('comment_parent').value = '0';
                    if (temp && respond) {
                        temp.parentNode.insertBefore(respond, temp);
                        temp.parentNode.removeChild(temp);
                    }
                    this.style.display = 'none';
                    this.onclick = null;
                    return false;
                };

                try {
                    t.I('comment').focus();
                }
                catch (e) {
                }

                return false;
            },

            I: function (e) {
                return document.getElementById(e);
            }
        }; // end addComment

        function exit_prev_edit() {
            $new_comm.show();
            $new_sucs.show();
            $('textarea').each(function () {
                this.value = ''
            });
            edit = '';
        }

        var wait = 15, submit_val = $submit.val();

        function countdown() {
            if (wait > 0) {
                $submit.val(wait);
                wait--;
                setTimeout(countdown, 1000);
            } else {
                $submit.val(submit_val);
                //$submit.val(submit_val).attr('disabled', false);
                wait = 15;
            }
        }
    });// end
} )( jQuery );