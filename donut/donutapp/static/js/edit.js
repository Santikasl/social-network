$(document).on('click', '.edit-button', function (e) {
    let id = e.target.id;
    const ge = document.getElementById(id)
    let idPosts = ge.value
    const desc = document.getElementById('edit-desc' + idPosts)
    let description = desc.value
    const descriptionpost2 = document.getElementById('open' + idPosts)
    const description2 = document.getElementById("description" + idPosts)
    const textarea = document.getElementById("edit-desc" + idPosts)
    const btnlike = document.getElementById('btnlike' + idPosts)


    $.ajax({
        type: 'POST',
        url: '/edit/',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            'id': idPosts,
            'description': description,
        },
        success: function (res_post2) {
            const dataPost2 = res_post2.data

            description2.style.display = 'flex'
            console.log(dataPost2)
            description2.innerHTML = ""
            descriptionpost2.innerHTML = ""
            textarea.style.display = 'none'
            description2.innerHTML += `
            <p>${dataPost2.split('\n').join('<br>')}</p>
`
            descriptionpost2.innerHTML += `
            ${dataPost2.split('\n').join('<br>')}
            `
            btnlike.style.opacity = '1'
        },

        error: function (xhr, errmsg, err) {
            console.log("error"); // provide a bit more info about the error to the console
        }
    });
});