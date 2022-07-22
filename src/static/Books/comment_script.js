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
            type: "POST",
            url: "/like-book-comment/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'comment_pk': ClickedId,
            },
            success: function(response){
                if(!response.user){
                    login_required()
                    return false
                }
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
            type: "POST",
            url: "/dislike-book-comment/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'comment_pk': ClickedId,
                'book_pk': BookPk,
            },
            success: function(response){
                if(!response.user){
                    login_required()
                    return false
                }
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
            }
        })

    }))
}


var visible = 3

const GetCommentData = () =>{
    $.ajax({
        type: "GET",
        url: `/book-comments/${BookPk}/${visible}`,
        csrfmiddlewaretoken: csrftoken,
        success: function(response){
            const data = response.data
            setTimeout(()=>{
                SpinnerBox.classList.add('not-visible')
                LoadBtn.classList.remove('not-visible')
                data.forEach(el => {
                    ReviewBox.innerHTML += comment_html(el)
                if (el.liked){
                    $(`#like-${el.pk}`).find('i').css("color", "blue")
                }
                else{
                    $(`#like-${el.pk}`).find('i').css("color", "black")
                }
                if (el.disliked){
                    $(`#dislike-${el.pk}`).find('i').css("color", "blue")
                }
                else{
                    $(`#dislike-${el.pk}`).find('i').css("color", "black")
                }
                });
            LikeComment();
            DislikeComment();
            }, 100)
            if (response.size === 0){
                EndBox.textContent = "No comments under this book"
            }
            else if (response.size <= visible){
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
    $('#delete-comment').on("click", function(e){
        e.preventDefault()
        console.log('clicked')
        var comment_pk = $(this).attr('delete_id')
        $.ajax({
          type: 'GET',
          url: `/delete-comment/${comment_pk}/`,
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
    
    
    
})

const CommentForm = document.getElementById('CommentForm')

$(document).on('click', '#delete-comment', function(e){
    e.preventDefault()
        console.log('clicked')
        var comment_pk = $(this).attr('delete_id')
        $.ajax({
          type: 'GET',
          url: `/delete-comment/${comment_pk}/`,
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
        url: "/api/v1/comment/",
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrftoken
        },
        contentType: 'application/json',
        data:JSON.stringify({
              'book': BookPk,
              'body': $('#body-comment').val()
        }),
        dataType: 'json',
        success: function(response){
            if(!response.user){
                login_required()
                return false
            }
            console.log(response)
            ReviewBox.insertAdjacentHTML('afterbegin', comment_html(response))
                LikeComment();
                DislikeComment();
            }
        
    })
})

function comment_html(el){
    html = `<div id='comment-${el.pk}' style='padding-top:20px'><div class="row border">
            <div class="col-1 border-right text-center">
                <a href="${el.user.url}}" style='href-unstyle'><img class="border rounded-circle"
                src="${el.user.avatar}" style="width: 80px;height: 60px;"></a>
            </div>
                <div class="col-11">
                <div class="row">
                        <span><a href="${el.user.url}}" class='href-unstyle'>${el.user.username}</a></span>
                        <span style="padding-top:10px">${new Date(el.time_created).toLocaleString("en-US")}</span>
                    <hr style='margin: 0em; border-width: 2px'>
                </div>
                <div class='row' style='padding-top:10px'>
                    <div class="comment">
                        ${el.comment}
                        <ul class="list-inline"
                            style="padding-top: 20px">
                            <li class="list-inline-item">
                                <form action="" method="POST" class="like-form-comment" data-form-id="${el.pk}"><button
                                class="" id="like-${el.pk}" type="submit"
                                style="background-color: Transparent; background-repeat:no-repeat;border: none;">
                                    <i class="fa fa-thumbs-up"></i>
                                    <span id="span-like-${el.pk}" class="" style="">${el.likes}</span>
                                </button></form>
                            </li>
                            <li class="list-inline-item">
                                <form action="" method="POST" class="dislike-form-comment" data-form-id="${el.pk}">
                                    <button class="" id="dislike-${el.pk}" type="submit"
                                    style="background-color: Transparent; background-repeat:no-repeat;border: none;">
                                        <i class="fa fa-thumbs-down"></i>
                                        <span id="span-dislike-${el.pk}" class="" style="">${el.dislikes}</span>
                                    </button></form>
                            </li>`
    if(el.is_creator){
        html += `<li class="list-inline-item"><a href="#" class='href-unstyle' id='delete-comment' style='color:red' delete_id=${el.pk}>Delete</a></li>`
    }
    html += `</ul></div></div></div></div></div></div>`
    return html
}
