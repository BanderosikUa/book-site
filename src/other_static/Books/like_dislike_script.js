const SpinnerBox = document.getElementById('spinner-box')
const ReviewBox = document.getElementById('review-box')
const ToCommentBox = document.getElementById('to-comment-book')


const LikeComment = () =>{
    const LikeForm=[...document.getElementsByClassName('like-form-comment')];
    LikeForm.forEach(form => form.addEventListener('submit', e=>{
        e.preventDefault()
        const ClickedId = e.target.getAttribute('data-form-id')
        const ClickedBtn = document.getElementById(`like-${ClickedId}`)
        console.log(ClickedBtn)

        $.ajax({
            type: "POST",
            url: "/like-book-comment/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'comment_pk': ClickedId,
            },
            success: function(response){
                $(`#like-${ClickedId}`).find('span').text(response.likes)
                $(`#dislike-${ClickedId}`).find('span').text(response.dislikes)
                $(`#like-${ClickedId}`).find('i').css("color", "blue")
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
            },
            success: function(response){
                $(`#dislike-${ClickedId}`).find('span').text(response.dislikes)
                $(`#like-${ClickedId}`).find('span').text(response.likes)
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
                data.forEach(el => {
                    ReviewBox.innerHTML += `<div class="border rounded-0 review" style="margin-top: 18px;">
                    <div class="user-info"><a class="avatar" href="#"
                            style="padding-right: -18px;margin-right: 0px;">
                            <ul class="list-inline">
                                <li class="d-xxl-flex justify-content-xxl-start list-inline-item"
                                    style="margin-top: 0px;margin-left: 38px;"><img
                                        class="border rounded-circle d-xxl-flex align-items-xxl-start"
                                        src=""
                                        style="width: 80px;height: 60px;margin-right: 0px;">
                                    <ul class="list-unstyled">
                                        <li style="margin-top: -14px;margin-left: 9px;"><span
                                                class="d-xxl-flex justify-content-xxl-start">${el.username}</span><span
                                                class="d-xxl-flex align-items-xxl-end disabled"
                                                style="height: 30px; padding-down: 20px">${el.time_created}
                                                </span></li>
                                                <br>
                                    </ul>
                                </li>
                            </ul>
                        </a>
                        <div class="comment" style="margin-left: 90px;">
                            <div><span class="d-xxl-flex justify-content-xxl-start"
                                    style="margin-top: -20px;padding-left: 37px;">${el.comment}
                                </span>
                                <ul class="list-inline d-xxl-flex justify-content-xxl-start"
                                    style="margin-down: 10px;padding-left: 33px;">
                                    <li class="list-inline-item"><form action="" method="POST" class="like-form-comment" data-form-id="${el.pk}"><button
                                            class="btn d-inline d-xxl-flex justify-content-xxl-start" id="like-${el.pk}"
                                            type="submit"
                                            style="margin-top: -17px;margin-left: -9px;"><i
                                                class="fa fa-thumbs-up d-xxl-flex justify-content-xxl-end align-items-xxl-start"></i><span id="span-like-${el.pk}"
                                                class="border rounded-0 shadow-sm d-xxl-flex align-items-xxl-center"
                                                style="margin-left: 10px;margin-top: -3px;transform: scale(1.10);opacity: 0.86;filter: brightness(135%);--bs-body-bg: var(--bs-red);">${el.likes}</span></button></form>
                                    </li>
                                    <li class="list-inline-item"><form action="" method="POST" class="dislike-form-comment" data-form-id="${el.pk}"><button
                                            class="btn d-inline d-xxl-flex justify-content-xxl-start" id="dislike-${el.pk}"
                                            type="submit"
                                            style="margin-top: -17px;margin-left: -9px;"><i
                                                class="fa fa-thumbs-down d-xxl-flex justify-content-xxl-end align-items-xxl-start"></i><span id="span-dislike-${el.pk}"
                                                class="border rounded-0 shadow-sm d-xxl-flex align-items-xxl-center"
                                                style="margin-left: 10px;margin-top: -3px;transform: scale(1.10);opacity: 0.86;filter: brightness(135%);--bs-body-bg: var(--bs-red);">${el.dislikes}</span></button></form>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>`
                });
            LikeComment();
            DislikeComment();
            }, 100)
            if (response.size === 0){
                ReviewBox.textContent = "No comments under this book"
            }
            else if (response.size <= visible){
                ReviewBox.text = "No more comments"
            }
            ToCommentBox.innerHTML = `<div id="post-comment" class="post-comment" style="padding-top: 30px">
            <div class="card text-black bg- mb-1">
                <div class="card-header">
                    <span class='d-flex align-item-center user-name'>UserName</span>
                </div>
                <div class="card-body">
                    <div class=" card-text form-group">
                        <textarea placeholder="Message" rows="4"
                            class="form-control form-control-lg">
        </textarea>
                    </div>
                    <div class="d-flex justify-content-center">
                    <a class="float-right btn btn-dark"> <i class="fa fa-comment"></i>
                        Comment</a>
                    </div>
                </div>
            </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        </section>
        `
        }

    })
}

GetCommentData();
$(document).ready(function(){
    $('.like-form-comment').submit(function(e){
        e.preventDefault();
        const CommentId=$('.btn d-inline d-xxl-flex justify-content-xxl-start')
        console.log(CommentId)
    })
})