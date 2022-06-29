const GenreName = document.getElementById("Genre name")
const url = $('#tabs-content').attr('data-url')

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

$(document).ready(function(){
    const page_url = window.location.href
    const regex = /(?:\?|\&)(?<key>[\w]+)(?:\=?|)(?<value>[\w+]+)?/gm
    const regexted = page_url.matchAll(regex)
    for (const match of regexted) {
        if(match.groups.key === 'q'){
            var q = match.groups.value
        }
        if(match.groups.key === 'ordering'){
            var ordering = match.groups.value
        }
      }
    if(ordering==undefined){
        if(q){
            window.location.href = `${url}?q=${q}&ordering=Popular`
        }
        else{
            window.location.href = `${url}?ordering=Popular`
        }
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
    
    $(".nav-link.bookmark").click(function(e){
        e.preventDefault()
        const ClickedButton = e.target
        const OrderTarget = ClickedButton.textContent
        if(q){
            window.location.href = `${url}?q=${q}&ordering=${OrderTarget}`
        }
        else{
            window.location.href = `${url}?ordering=${OrderTarget}`
        }
    
    })
})
