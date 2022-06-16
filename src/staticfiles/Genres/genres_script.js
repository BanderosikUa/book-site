const GenreName = document.getElementById("Genre name")
const url = $('#tabs-content').attr('data-url')

const getCookie=(name)=> {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



function InitRatings(){
    const ratings = document.querySelectorAll('.rating')    
    let ratingActive, ratingValue;

    for (let index=0; index < ratings.length; index++){
        const rating = ratings[index];
        initRating(rating);
    }

    function initRating(rating){
        InitRatingVars(rating);

        SetAverageRating();
    }

    function InitRatingVars(rating){
        ratingActive = rating.querySelector('.rating__active')
        ratingValue = rating.querySelector('.rating__value')
    }

    function SetAverageRating(index = ratingValue.innerHTML){
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`
    }
}

InitRatings()



// const TabsContent = document.getElementById('tabs-content')

// var genres

// function get_genres(book_pk){
//     $.ajax({
//         type: "GET",
//         async: false,
//         url: `/books/get-genres-of-book/${book_pk}`,
//         success: function(response){
//             genres = response
//         },
//         error: function(error){
//             return
//         }
//     })
// }


// send_ajax('Novelties')

$(document).ready(function(){
    const page_url = window.location.href
    const ordering = page_url.split(/\/?ordering=(\w*)/)[1]
    console.log(ordering)
    if(ordering==undefined){
        window.location.href = `${url}?ordering=Popular`
    }
    const buttons = [...document.getElementsByClassName('nav-link bookmark')]
    buttons.forEach(but => {
        if(but.classList.contains('active') && but.textContent != ordering){
            but.classList.remove('active');
        }
        else if(but.textContent == ordering){
            but.classList.add('active')
        }
    })
})


$(".nav-link.bookmark").click(function(e){
    e.preventDefault()
    const ClickedButton = e.target
    const OrderTarget = ClickedButton.textContent
    window.location.href = `${url}?ordering=${OrderTarget}`

})

// async function send_ajax(OrderTarget){
//     $.ajax({
//         type: "POST",
//         url: url,
//         csrfmiddlewaretoken: csrftoken,
//         data: {
//             'csrfmiddlewaretoken': csrftoken,
//             'ordering_by': OrderTarget
//         },
//         success: function(response){
//             console.log(response)
//             TabsContent.innerHTML = ''
//             response['books'].forEach(el => {
//                 var html = `
//                 <div id="book" style="border-bottom: 1px solid rgb(159,159,159) ;">
//                 <div class="row no-gutters" style="padding-top: 17px;padding-bottom: 30px;">
//                     <div class="col-12 col-sm-auto"><a class="image-link d-block" href="/book/${el.slug}"><img class="rounded-sm ls-is-cached lazyloaded" src = "/media/${el.photo}" widht="160" height="240"></a></div>
//                     <div class="col-12 col-sm ml-sm-5" style="padding-top: -1px;">
//                 `
//                 get_genres(el.pk)
//                 console.log(genres)
//                 genres.forEach(e => {
//                     html += `
//                         <li class="list-inline-item rounded" style="padding: 0px 1px;padding-right: 0px;padding-left: 1px;"><a class="text-center link d-block font-size-sm" href="/genres/${e.genre__slug}">${ e.genre__name }</a></li>
//                     `
//                 })
                
//                 html += `
//                     <div style="padding-top:10px"><a href="/book/${el.slug}" style="text-decoration: none; color: inherit;"><h4>${el.name}</h4></a></div>
//                     <div class="author-name" style="padding-top: 2px;padding-left: 0px;"><span style="opacity: 0.77;">Author:&nbsp;</span><a href="#"><span class="title-name" style="opacity: 0.77;color: rgb(192,220,25);">${el.author__name || "None"}</span></a></div>
//                     <div id="rating" style="margin-left:-12px"><div class="rating rating_set col-xs-12">
//                         <div class="rating__body">
//                             <div class="rating__active"></div>
//                             <div class="rating__items">
//                                 <span class="rating__item" name="rating">
//                                 <span class="rating__item" name="rating">
//                                 <span class="rating__item" name="rating">
//                                 <span class="rating__item" name="rating">
//                                 <span class="rating__item" name="rating">
//                             </div>
//                         </div>
//                                 <div class="rating__value" style="padding-bottom:2px">${ el.avg_rating }</div>
//                             </div>
//                         </div>
//                         <div id="bookmarks" style="">
//                             <ul class="list-inline">
//                                 <li class="d-inline-flex justify-content-xxl-center list-inline-item"><i class="fa fa-clock-o d-xxl-flex align-items-xxl-center"></i><span class="d-inline-block" href="#" style="margin-left: 5px; margin-bottom:-2px">${el.plan_to_read}</span></li>
//                                 <li class="d-inline-flex justify-content-xxl-center list-inline-item"><i class="fa fa-book d-xxl-flex align-items-xxl-center"></i><span class="d-inline-block" href="#" style="margin-left: 5px; margin-bottom:-2px">${el.reading}</span></li>
//                                 <li class="d-inline-flex justify-content-xxl-center list-inline-item"><i class="fa fa-check-circle d-xxl-flex align-items-xxl-center"></i><span class="d-inline-block" href="#" style="margin-left: 5px; margin-bottom:-2px">${el.read}</span></li>
//                                 <li class="d-inline-flex justify-content-xxl-center list-inline-item"><i class="fa fa-remove d-xxl-flex align-items-xxl-center"></i><span class="d-inline-block" href="#" style="margin-left: 5px; margin-bottom:-2px">${el.abandonded}</span></li>
//                             </ul>
//                         </div>
//                         <div class="" style="margin-top:-7px">
//                             <span style="padding-top: 9px;"></a>${el.about.substring(0, 200)}... <a href="books/${el.slug}">More</a></span>
//                         </div>
//                     </div>
//                     </div>
//                 </div>
//                     ` 
//                 TabsContent.innerHTML += html
//             });
//             InitRatings()
//         },
//         error: function(error){
//             console.log(error)
//         }
//     })
// }
