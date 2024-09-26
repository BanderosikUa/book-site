const SpinnerBox = document.getElementById('spinner-box')
const ReviewBox = document.getElementById('review-box')
const ToCommentBox = document.getElementById('to-comment-book')
const LoadBtn = document.getElementById('load-btn')
const EndBox = document.getElementById('end-box')


const LikeComment = () =>{
    const LikeForm=[...document.getElementsByClassName('like-form-comment')];
    LikeForm.forEach(form => form.addEventListener('submit', e=>{
        e.preventDefault()
        const ClickedId = e.target.getAttribute('data-form-id')
        const ClickedBtn = document.getElementById(`like-${ClickedId}`)

        $.ajax({
            type: "GET",
            url: `/comments/${ClickedId}/like/`,
            csrfmiddlewaretoken: csrftoken,
            success: function(response){
                $(`#like-${ClickedId}`).find('span').text(response.likes)
                $(`#dislike-${ClickedId}`).find('span').text(response.dislikes)
                if (response.liked){
                    $(`#like-${ClickedId}`).find('i').css("color", "blue")
                }
                else{
                    $(`#like-${ClickedId}`).find('i').css("color", "black")
                }
                if (response.disliked){
                    $(`#dislike-${ClickedId}`).find('i').css("color", "blue")
                }
                else{
                    $(`#dislike-${ClickedId}`).find('i').css("color", "black")
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

const DislikeComment = () =>{
    const LikeForm=[...document.getElementsByClassName('dislike-form-comment')];
    LikeForm.forEach(form => form.addEventListener('submit', e=>{
        e.preventDefault()
        const ClickedId = e.target.getAttribute('data-form-id')
        const ClickedBtn = document.getElementById(`dislike-${ClickedId}`)

        $.ajax({
            type: "GET",
            url: `/comments/${ClickedId}/dislike/`,
            csrfmiddlewaretoken: csrftoken,
            success: function(response){
                $(`#dislike-${ClickedId}`).find('span').text(response.dislikes)
                $(`#like-${ClickedId}`).find('span').text(response.likes)
                if (response.liked){
                    $(`#like-${ClickedId}`).find('i').css("color", "blue")
                }
                else{
                    $(`#like-${ClickedId}`).find('i').css("color", "black")
                }
                if (response.disliked){
                    $(`#dislike-${ClickedId}`).find('i').css("color", "blue")
                }
                else{
                    $(`#dislike-${ClickedId}`).find('i').css("color", "black")
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


var visible = 0

const GetCommentData = () =>{
    $.ajax({
        type: "GET",
        url: `/books/${BookPk}/comments/`,
        csrfmiddlewaretoken: csrftoken,
        dataType: 'json',
        data: {offset: visible},
        success: function(response){
            const data = response.results
            setTimeout(()=>{
                SpinnerBox.classList.add('not-visible')
                LoadBtn.classList.remove('not-visible')
                data.forEach(el => {
                    ReviewBox.innerHTML += comment_html(el)
                if (el.liked){
                    $(`#like-${el.id}`).find('i').css("color", "blue")
                }
                else{
                    $(`#like-${el.id}`).find('i').css("color", "black")
                }
                if (el.disliked){
                    $(`#dislike-${el.id}`).find('i').css("color", "blue")
                }
                else{
                    $(`#dislike-${el.id}`).find('i').css("color", "black")
                }
                });
            LikeComment();
            DislikeComment();
            }, 100)
            if (response.results.length === 0){
                EndBox.textContent = "No comments under this book"
            }
            else if (response.results.length <= visible){
                LoadBtn.classList.add('not-visible')
                EndBox.textContent = "No more comments"
            }
         
        }

    })
}

LoadBtn.addEventListener('click', ()=>{
    SpinnerBox.classList.remove('not-visible')
    LoadBtn.classList.add('not-visible')
    visible += 3
    GetCommentData()
})

$(document).ready(function(){
    GetCommentData();
    $('.like-form-comment').submit(function(e){
        e.preventDefault();
        const CommentId=$('.btn d-inline d-xxl-flex justify-content-xxl-start')
        console.log(CommentId)
    })
})

const CommentForm = document.getElementById('CommentForm')

$(document).on('click', '#delete-comment', function(e){
    e.preventDefault()
    console.log('clicked')
    var comment_pk = $(this).attr('delete_id')
    $.ajax({
      type: 'GET',
      url: `/comments/${comment_pk}/delete/`,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      success: function(response){
        if(response.deleted){
          $(`#comment-${comment_pk}`).remove()
        }
        else{
            console.log('else')
        }
      },
      error: function(error){
        console.log(error)
      }
    })
})


$(document).on('submit', '#CommentForm', function(e){
    e.preventDefault()
    $.ajax({
        type: "POST",
        url: "/comments/create/",
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data:{
              'book': BookPk,
              'body': $('#body-comment').val()
        },
        dataType: 'json',
        success: function(response){
            ReviewBox.insertAdjacentHTML('afterbegin', comment_html(response))
                LikeComment();
                DislikeComment();
        },
        error: function(xhr, status, error) {
            // Handle authentication error
            if (xhr.status === 401 || xhr.status === 403) {
                login_required();  // Redirect to login or handle auth error
            }
        }
        
    })
})

function comment_html(el){
    html = `<div id='comment-${el.id}' style='padding-top:20px'><div class="row border h-100 flex-row min-vh-50">
                <div class="col-sm-5 col-lg-1 col-md-3 flex-shrink-1"><a href="${el.user.url}" style='href-unstyle' class='d-flex justify-content-center'><img class="border rounded-circle pfp"
                    src="${el.user.avatar}"></a></div>
                <div class="col-sm-7 col-lg-11 col-md-9 flex-shrink-1">
                    <span>${el.user.username}</span>
                    <p style="padding-top:10px">${formatDateTimeShort(el.time_created)}</p>
                </div>
                <div class="comment h-100 flex-grow-1">
                    <span class="body">${el.body}</span>
                    <ul class="list-inline reactions">
                        <li class="list-inline-item">
                            <form action="" method="POST" class="like-form-comment" data-form-id="${el.id}"><button
                            class="" id="like-${el.id}" type="submit"
                            style="background-color: Transparent; background-repeat:no-repeat;border: none;">
                                <i class="fa fa-thumbs-up"></i>
                                <span id="span-like-${el.id}" class="" style="">${el.likes}</span>
                            </button></form>
                        </li>
                        <li class="list-inline-item">
                            <form action="" method="POST" class="dislike-form-comment" data-form-id="${el.id}">
                                <button class="" id="dislike-${el.id}" type="submit"
                                style="background-color: Transparent; background-repeat:no-repeat;border: none;">
                                    <i class="fa fa-thumbs-down"></i>
                                    <span id="span-dislike-${el.id}" class="" style="">${el.dislikes}</span>
                                </button></form>
                        </li>
    `
    if(el.is_creator){
        html += `<li class="list-inline-item"><a href="#" class='href-unstyle' id='delete-comment' style='color:red' delete_id=${el.id}>Delete</a></li>`
    }
    html += `</ul></div></div>`
    return html
}
