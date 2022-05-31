const rating = document.querySelectorAll('.rating')[0]
const BookPicture = document.getElementById('book')
const BookPk = BookPicture.getAttribute('book-id')
const ratingActive = rating.querySelector('.rating__active');
const ratingValue = rating.querySelector('.rating__value');
const userValue = document.getElementById('user_checked_value')


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
    var avarage_rating = 0;
    $.ajax({
        async: false,
        type: 'GET',
        url: `/get-avarage-rating/${BookPk}`,
        success: function(response){
            ratingValue.textContent = response.avg_rating
            avarage_rating = response.avg_rating
        },
    });
    return avarage_rating
}

var AvgRate = getAvgRate();


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
                getAvgRate();
                AvgRate = getAvgRate();
                setRatingActiveWidth(AvgRate);
                getUserValue();
            })                
        }

    } 
}

const getUserValue = () =>{
    const ratingItems = rating.querySelectorAll('.rating__item');
    for(let index=0;index < ratingItems.length; index++){
        const ratingItem = ratingItems[index]
        if(ratingItem.checked){
            userValue.textContent = `Your rate: ${ratingItem.value}`
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

const UserBookmarking = () =>{
    const BookmarkButtons = [...document.getElementsByClassName('dropdown-item bookmark')]
    BookmarkButtons.forEach(button => button.addEventListener('click', e=>{
        e.preventDefault()
        const ClickedBookmarkBtn = e.target
        const ClickedBookmark = ClickedBookmarkBtn.value

        $.ajax({
            type: "POST",
            url: "/bookmark-book/",
            data:{
                'csrfmiddlewaretoken': csrftoken,
                'book_pk': BookPk,
                'bookmarked': ClickedBookmark
            },
            success: function(response){
                if (response.clicked){
                    $(ClickedBookmarkBtn).css('background-color', 'orange')
                    const html = ClickedBookmarkBtn.innerHTML
                    $('.btn.btn-secondary.dropdown-toggle.border.rounded-pill').html(html)
                }
                else{
                    const AddTheBookHtml = `<i class="fa fa-bookmark"></i><span style="margin-left: 7px;">Add this book</span>`
                    $(ClickedBookmarkBtn).css('background-color', 'white')
                    $('.btn.btn-secondary.dropdown-toggle.border.rounded-pill').html(AddTheBookHtml)
                }
                if (response.previous_bookmark){
                    for(let index=0; index < BookmarkButtons.length; index++){
                        if (BookmarkButtons[index].value == response.previous_bookmark){
                            $(BookmarkButtons[index]).css('background-color', 'white')
                      }
                    }
                }
            },
            error: function(error){
                console.log(error)
            }
        })
    }))
}



main();

function main(){
    setRatingActiveWidth(getAvgRate());
    SetRating();
    getUserValue();
    UserBookmarking();
}
