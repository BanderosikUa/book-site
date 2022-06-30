function InputActive(){
  window.onclick = function(event) {
    if (event.target.id == "LoginModal") {
      $('#LoginModal').removeClass('show').css({'display': 'none'})
    }
  }
  $('.form-outline input').each(function(){
    if($(this).val()){
      $(this).parent().find('input').addClass('active')
    }
    else{
      $(this).parent().find('input').removeClass("active");
    }
  })
}


$(document).ready(function(){
    $('#LoginModal').on('hide.bs.modal', () => {
      console.log('need to hide')
      $('#login-alert').hide()
    })
    $('#signup-link').click(function(event){
        event.preventDefault()
        $('#LoginModal').modal('hide')
      })
    if(window.location.href.indexOf('#LoginModal') != -1) {
          $('#LoginModal').modal('show');
    }
  
    $('#login-form').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: '/validate-login-form/',
            data: $(this).serialize(),
            success: function(response){
                if (response.error){
                    $('#login-li').html(response.form)
                    $('#LoginModal').modal('show')
                    InputActive()
                }
                else{
                    window.location.reload()
                }
            }
            })
        })  
    })
