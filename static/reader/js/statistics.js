(function() {
    var articleId = $('meta[name="article_id"]').attr('content');
    var userId = $('meta[name="user_id"]').attr('content');
    var recordId = null;
    var isLiked = false;

    $.ajax({
        url: '/reader/query/read_records/create/' + articleId
    }).done(function(data) {
        recordId = data.record_id;
        isLiked = data.is_liked;

        $('.like-this').click(function() {
            if (isLiked) { unlike(); }
            else { like(); }
        });

        if (isLiked) { stateLiked(); }
        else { stateNotLiked(); }

    });

    function stateNotLiked() {
        $('.like-this span i').removeClass('yellow');
        $('.like-this span i').removeClass('fa-heart');
        $('.like-this span i').addClass('fa-heart-o');
        isLiked = false;
    }

    function stateLiking() {
        $('.like-this span i').addClass('yellow');
        $('.like-this span i').removeClass('fa-heart');
        $('.like-this span i').addClass('fa-heart-o');
    }

    function stateLiked() {
        $('.like-this span i').addClass('yellow');
        $('.like-this span i').addClass('fa-heart');
        $('.like-this span i').removeClass('fa-heart-o');
        isLiked = true;
    }

    function like() {
        stateLiking();
        $.ajax({
            url: '/reader/query/read_records/like/' + recordId
        }).done(function(data) {
            if(data.status == "ok") {
                stateLiked();
            } else {
                like();
            }
        });
    }

    function unlike() {
        stateLiking();
        $.ajax({
            url: '/reader/query/read_records/unlike/' + recordId
        }).done(function(data) {
            if(data.status == "ok") {
                stateNotLiked();
            } else {
                unlike();
            }
        });
    }

})();
