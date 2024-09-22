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


// const getAvgRate = () =>{
//     $.ajax({
//         async: false,
//         type: 'GET',
//         url: `/books/${BookPk}/rating`,
//         success: function(response){
//             ratingValue.textContent = response.avg_rating
//             avarage_rating = response.avg_rating
//             UpdateRate(avarage_rating)
//         },
//     });
// }

var AvgRate;
function UpdateRate(data){
    AvgRate = data
}

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
                RateBook(ratingItem.value)
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
            url: '/rating/create/',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'book': BookPk,
                'rate': rate_value,
            },
            success: function(response){
                ratingValue.textContent = response.avg_rating
                UpdateRate(response.avg_rating)
                setRatingActiveWidth(response.avg_rating)

            },
            error: function(xhr, status, error) {
                // Handle authentication error
                if (xhr.status === 401 || xhr.status === 403) {
                    login_required();  // Redirect to login or handle auth error
                }
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
            url: "/bookmarks/create/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data:{
                'book': BookPk,
                'bookmarks': ClickedBookmark
            },
            success: function(response){
                for(let index=0; index < BookmarkButtons.length; index++){
                    $(BookmarkButtons[index]).css('background-color', 'white')
                }
                if (response.bookmarks){
                    $(ClickedBookmarkBtn).css('background-color', 'orange')
                    const html = ClickedBookmarkBtn.innerHTML
                    $('.btn.btn-secondary.dropdown-toggle.border.rounded-pill').html(html)
                }
                else{
                    const AddTheBookHtml = `<i class="fa fa-bookmark"></i><span style="margin-left: 7px;">Add this book</span>`
                    $(ClickedBookmarkBtn).css('background-color', 'white')
                    $('.btn.btn-secondary.dropdown-toggle.border.rounded-pill').html(AddTheBookHtml)
                }
            },
            error: function(xhr, status, error) {
                // Handle authentication error
                if (xhr.status === 401 || xhr.status === 403) {
                    login_required();  // Redirect to login or handle auth error
                }
            }
        })
    }))
}

const SetUserBookmark = () => {
    const BookmarkButtons = [...document.getElementsByClassName('dropdown-item bookmark')]

    $.ajax({
        type: "GET",
        url: `/books/${BookPk}/bookmarks/`,
        success: function(response){
            if(response.bookmarks){
                const UserBookmark = BookmarkButtons[response.bookmarks-1]
                $(UserBookmark).css('background-color', 'orange')
                const html = UserBookmark.innerHTML
                $('.btn.btn-secondary.dropdown-toggle.border.rounded-pill').html(html)
            }
        },
        error: function(xhr, status, error) {
            // Handle authentication error
            if (xhr.status === 401 || xhr.status === 403) {
                login_required();  // Redirect to login or handle auth error
            }
        }
    })
}


main();

function main(){
    getUserValue()
    setRatingActiveWidth(ratingValue.textContent);
    SetRating();
    UserBookmarking();
}
