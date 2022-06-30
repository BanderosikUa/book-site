const SpinnerBox = document.getElementById('spinner-box')
const UserCommentsBox = document.getElementById('user-comments-box')
const LoadBtn = document.getElementById('load-btn')
const EndBox = document.getElementById('end-box')
const UserPk = $('#user-username').attr('username')

var visible = 10

const GetCommentData = () =>{
    $.ajax({
        type: "GET",
        url: `/get-user-comments/${UserPk}/${visible}`,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        success: function(response){
            const data = response.data
            setTimeout(()=>{
                SpinnerBox.classList.add('not-visible')
                LoadBtn.classList.remove('not-visible')
                data.forEach(el => {
                        UserCommentsBox.innerHTML += `<div id='comment-${el.pk}' style='padding-top:20px'><div class="row border">
                        <div class="col-2 border-right text-center">
                            <a href="${el.book_url}"><img class='owl-lazy' src="${el.book_photo}" style='object-fit: cover;' height='180' width="120"></a>
                        </div>
                        <div class="col-10">
                            <div class="row">
                                <div class="col-1"><a href="${el.user_url}}" style='href-unstyle'><img class="border rounded-circle"
                                    src="${el.avatar}" style="width: 80px;height: 60px;"></a></div>
                                <div class="col-11" style="padding-left:38px;">
                                    <span>${el.username}</span>
                                    <p style="padding-top:10px">${el.time_created}</p>
                                </div>
                                <div class="comment">
                                    ${el.comment}
                                    <ul class="list-inline"
                                        style="padding-top: 20px">
                                        <li class="list-inline-item"><div>
                                                    <i
                                                    class="fa fa-thumbs-up"></i>
                                                    <span id="span-like-${el.pk}"
                                                    class=""
                                                    style="">${el.likes}</span></div>
                                        </li>
                                        <li class="list-inline-item">
                                                <div style='padding-left:10px'>
                                                    <i
                                                    class="fa fa-thumbs-down"></i>
                                                    <span id="span-dislike-${el.pk}"
                                                    class=""
                                                    style="">${el.dislikes}</span><div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>`
                });
            }, 100)
            if (response.size === 0){
                EndBox.textContent = "Users not make comments yet"
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
    visible += 10
    GetCommentData()
})

GetCommentData();
