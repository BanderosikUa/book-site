$(document).on('click', '#navbarDropdown-genres', function(){
  function FillNavbarGenres(){
      if ($("#genres-menu").has('li').length > 0){
        console.log('true')
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
            html += `<li><a class="dropdown-item" href="${response.all_genres_url}">All genres!</a></li>`
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
