function InputActive(){
  $('.form-outline input').each(function(){
    if($(this).val()){
      $(this).parent().find('input').addClass('active')
    }
    else{
      $(this).parent().find('input').removeClass("active");
    }
  }
 )
  
  window.onclick = function(event) {
    if (event.target.id == "RegistrationModal") {
      $('#RegistrationModal').removeClass('show').css({'display': 'none'})
    }
 }
}
``
$(document).ready(function(){
    $('#registration-form').on('submit', function(event){
          event.preventDefault()
          $.ajax({
              type: "POST",
              url: '/auth/register/',
              data: $(this).serialize(),
              success: function(response){
                  if (response.error){
                      $('#registration-li').html(response.form)
                      $('#RegistrationModal').modal('show')
                      InputActive()
                  }
                  else{
                      $('#RegistrationModal').modal('hide')
                      $('#LoginModal').modal('show')

                  }
              }
              })
          })
        }
      )
