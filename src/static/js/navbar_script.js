$(document).ready(function(){
  $(this).on('click', '#navbarDropdown-genres', function(){
    function FillNavbarGenres(){
        if ($("#genres-menu").has('li').length > 0){
          return false
        }
        var aria_expanded = $('#navbarDropdown-genres').hasClass('show')
        if (aria_expanded){
          $.ajax({
            type: 'GET',
            url: '/get-genres/',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            success: function(response){
              var html = ''
              const data = response.data
              data.forEach(el => {
                html += `<li><a class="dropdown-item" href="${el.url}">${el.name}</a></li>`
              })
              html += `<li><a class="dropdown-item" href="${response.all_genres_url}?ordering=Popular">All genres!</a></li>`
              $('#genres-menu').html(html)
            },
            error: function(error){
              console.log(error)
            }
          })
        }
      }
    FillNavbarGenres();
    })
  $(this).on('click', '#navbarDropdown-notifications', function(event){
    function FillNavbarNotifications(){
        if ($("#notifications").has('li').length > 0){
          console.log('okkkk')
          return false
        }
        var aria_expanded = $('#navbarDropdown-notifications').hasClass('show')
        if (aria_expanded){
          $.ajax({
            type: 'GET',
            url: '/get-notifications/',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            success: function(response){
              var html_notification = ''
              var data = response.data
              if(response.size > 0){
                  data.forEach(el => {
                  html_notification += `<div id="notification-${el.pk}">
                                          <li>
                                            <div class="row">
                                              <a href="${el.url}" class='href-unstyle'>
                                                <div class="col-md">
                                                  <img src="${el.photo}" height='100' width='100'
                                                    class="d-block"/>
                                                </div>
                                                <div class="col-md">
                                                  ${el.message}
                                                </a>
                                                  <div class="row">
                                                    <div class='col-6'><a href="#" class='href-unstyle' id='delete-notification' style='color:red;' delete_id=${el.pk}>Delete</a></div>
                                                    <div class='col-6'>
                                                        <p class="h8 mb-1 text-right" style="font-size:11px;text-align:right">${el.time}</p>
                                                    </div>
                                                  </div>
                                                </div>
                                            </div>
                                          </li>
                                          <li>
                                            <hr class="dropdown-divider" />
                                          </li>
                                        </div>
                                        `
                    })
                  }
              else{
                html_notification = 'No notification yet!'
              }
              $('#notifications').html(html_notification)
            }
          })
        }
      }
    FillNavbarNotifications();
    $('#delete-notification').on("click", function(e){
      e.preventDefault()
      var notification_pk = $(this).attr('delete_id')
      $.ajax({
        type: 'GET',
        url: `/delete-notification/${notification_pk}/`,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        success: function(response){
          if(response.deleted){
            $(`#notification-${notification_pk}`).remove()
          }
        },
        error: function(error){
          console.log(error)
        }
      })
    })
    })

})
