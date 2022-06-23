$(document).on('click', '#navbarDropdown-genres', function(){
  console.log('asdas')
    var aria_expanded = $(this).attr('aria-expanded')
    if (aria_expanded == 'true'){
      console.log('paskdasd')
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
          $('#genres-menu').html(html)
        },
        error: function(error){
          console.log(error)
        }
      })
    }
  })
