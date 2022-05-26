
const rating = document.querySelectorAll('.rating')[0]
const BookPicture = document.getElementById('book')
const BookPk = BookPicture.getAttribute('book-id')

function initRatingVars(rating){
    ratingActive = rating.querySelector('.rating__active');
    ratingValue = rating.querySelector('.rating__value');
}

function setRatingActiveWidth(index){
    const ratingActiveWidth = index / 0.05;
    ratingActive.style.width = `${ratingActiveWidth}%`
}   

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


const getAvgRate = () =>{
    $.ajax({
        type: 'GET',
        url: `/get-avarage-rating/${BookPk}`,
        success: function(response){
            ratingValue.textContent = response.avg_rating
            const avarage_rating = response.avg_rating
            return avarage_rating
        },
    })
}

const AvgRate = getAvgRate();


function SetRating(){
    if (rating.classList.contains('rating_set')){
        const ratingItems = rating.querySelectorAll('.rating__item');
        for (let index = 0; index < ratingItems.length; index++){
            const ratingItem = ratingItems[index];
            ratingItem.addEventListener("mouseenter", function(e){
                setRatingActiveWidth(ratingItem.value);
            })
            ratingItem.addEventListener('mouseleave', function(e){
                setRatingActiveWidth(AvgRate);
            })
            ratingItem.addEventListener('click', function(e){
                RateBook(rate_value=ratingItem.value);
            })                
        }

    } 
}

const RateBook = (rate_value) =>{
    if(!rating.classList.contains('rating_sending')){
        rating.classList.add('rating_sending');
        
        $.ajax({
            type: 'POST',
            url: '/rate-book/',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'pk': BookPk,
                'value': rate_value,
            },
            success: function(response){
                console.log(response)
                getAvgRate()
                setRatingActiveWidth(AvgRate)
                },
            error: function(error){
                console.log(error)
            }
        })

        rating.classList.remove('rating_sending');
    }
    }

main();

function main(){
    let ratingActive, ratingValue;
    initRatingVars(rating);
    getAvgRate();
    SetRating();
}
