const url = window.location.href
const searchForm = document.getElementById("search-form")
const searchInput = document.getElementById("search-input")
const resultBlock = document.getElementById("results-block")
const blurSearch = document.getElementById("overlay-blur")
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
blurSearch.classList.remove('blur-search')
resultBlock.classList.remove('not-found-extend')
const sendSearchData = (dataName) => {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'dataName': dataName,

        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)) {
                resultBlock.classList.remove('not-found-extend')
                resultBlock.innerHTML = ""
                data.forEach(dataName => {
                    resultBlock.innerHTML += `

                       <div class="searchItems" style="">
                       <a href="/${dataName.pk}">
                       <div class="img-profile">
                       <img src="${dataName.img}" alt="" width="80px">
                       </div>
                       <h2 class="nameSearch">${dataName.name}</h2>
                        </a>
                       </div>
                  
                    `
                })
            } else {
                if (searchInput.value.length > 0) {
                    resultBlock.classList.add('not-found-extend')

                    resultBlock.innerHTML = ` 
 
   <img src="/static/img/not-found3.gif" alt="not-found" class="not-found-gif" >
   <h2 class="not-found"> ${data} </h2> `
                } else {
                    blurSearch.classList.remove('blur-search')
                    resultBlock.classList.add('not-visible')
                }
            }

        },
        error: (err) => {
            console.log(err)
        }
    })
}


searchInput.addEventListener('keyup', e => {


    if (resultBlock.classList.contains('not-visible')) {
        resultBlock.classList.remove('not-visible')
        resultBlock.classList.remove('not-found-extend')
        blurSearch.classList.add('blur-search')
    }

    sendSearchData(e.target.value)
})

