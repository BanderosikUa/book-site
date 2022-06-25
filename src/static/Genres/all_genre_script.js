$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
        nav: true,
        loop: true,
        lazyLoad: true,
        margin: 5,
        padding: 5,
        stagePadding: 5,
        responsive:{
            0 : {
                items: 1,
                dots: false
            },
            485 : {
                items: 2,
                dots: false
            },
            728: {
                items: 3,
                dots: false
            },
            960: {
                items: 4,
                dots: false
            },
            1200: {
                items: 6,
                dots: true
            }
        }
    })
})

const url = $('#all-genres').attr('data-url')


$(document).ready(function(){
    const page_url = window.location.href
    const ordering = page_url.split(/\/?ordering=(\w*)/)[1]
    if(ordering==undefined){
        window.location.href = `${url}?ordering=Popular`
    }
    const buttons = [...document.getElementsByClassName('nav-link genres')]
    buttons.forEach(but => {
        if(but.classList.contains('active') && but.textContent != ordering){
            but.classList.remove('active');
        }
        else if(but.textContent == ordering){
            but.classList.add('active')
        }
    })
    $(".nav-link.genres").click(function(e){
        e.preventDefault()
        const ClickedButton = e.target
        const OrderTarget = ClickedButton.textContent
        window.location.href = `${url}?ordering=${OrderTarget}`
    
    })
})
