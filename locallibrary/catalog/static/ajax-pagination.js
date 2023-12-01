function ajax_pagination(page, title) {
    $.ajax({
        url:'/ajax/paginate/',
        type: 'get',
        data: {
            'page': page,
            'title': title,
        },
        dataType: 'json',
        success: function(payload) {
            $('#id-of-your-choice').empty();
            for (i=0; i < payload.result.length; i++){
                $('#id-of-your-choice').append(i)
            }
        }
    })
}
