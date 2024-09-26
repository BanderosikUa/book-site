const SpinnerBox = document.getElementById('spinner-box')
const UserCommentsBox = document.getElementById('user-comments-box')
const LoadBtn = document.getElementById('load-btn')
const EndBox = document.getElementById('end-box')
const UserId = $('#user-id').attr('userId')

var visible = 0

const GetCommentData = () =>{
    $.ajax({
        type: "GET",
        url: `/users/${UserId}/comments`,
        data: {offset: visible, limit: 10},
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        success: function(response){
            const data = response.results
            setTimeout(()=>{
                SpinnerBox.classList.add('not-visible')
                LoadBtn.classList.remove('not-visible')
                data.forEach(el => {
                        UserCommentsBox.innerHTML += `<div id='comment-${el.id}' style='padding-top:20px'><div class="row border">
                        <div class="col-md-5 col-sm-6 col-lg-3 border-right text-center">
                            <a href="${el.book.url}">
                            <img class='owl-lazy pfp' src="${el.book.photo}" style='object-fit: cover;'>
                            </a>
                        </div>
                        <div class="col-md-7 col-sm-6 col-lg-9">
                            <div class="row flex-row h-80">
                                <div class="col-sm-6 col-lg-2 col-md-3 flex-shrink-1"><a href="${el.user.url}}" style='href-unstyle' class='d-flex justify-content-center'><img class="border rounded-circle pfp"
                                    src="${el.user.avatar}"></a></div>
                                <div class="col-sm-6 col-lg-10 col-md-9 flex-shrink-1">
                                    <span>${el.user.username}</span>
                                    <p style="padding-top:10px">${formatDateTimeShort(el.time_created)}</p>
                                </div>
                                <div class="comment h-100 flex-grow-1">
                                    <span class="body">${el.body}</span>
                                    <ul class="list-inline reactions">
                                        <li class="list-inline-item"><div>
                                            <i
                                            class="fa fa-thumbs-up"></i>
                                            <span id="span-like-${el.id}"
                                            class=""
                                            style="">${el.likes}</span></div>
                                        </li>
                                        <li class="list-inline-item">
                                                <div style='padding-left:10px'>
                                                    <i
                                                    class="fa fa-thumbs-down"></i>
                                                    <span id="span-dislike-${el.id}"
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
            if (response.results.length === 0){
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
