$('.like-form').submit(function (e) {
    e.preventDefault()
    var post_id_not_slice =  $(this).attr('id')
    const post_id =  post_id_not_slice.slice(1)
    const url = $(this).attr('action')
    let res
    const like = $(`.like-btn${post_id}`).text()
    const intLike = like
    const trimCount = parseInt(intLike)
    const btnlike = document.querySelectorAll('#btnlike' + post_id)

    const like_img = document.getElementById('like-img' + post_id)
    $.ajax({
        method: 'POST',
        url: '/like/',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            'post_id': post_id,
        },
        success: function (response) {

            value = response.likes
            btnlike.forEach(button => {
                button.innerHTML = `
            <p class="like-img" id="like-img${post_id}">❤ ${value}</p>
            `
            })

            if (response.like_value == 'Like') {
                btnlike.forEach(button => {button.style.color = 'black'})


            } else {
                btnlike.forEach(button => {button.style.color = 'red'})


            }


        },
        error: function (xhr, errmsg, err) {
            console.log("error");
        }
    })

})