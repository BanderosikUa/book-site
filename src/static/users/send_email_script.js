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
    
  //   window.onclick = function(event) {
  //     if (event.target.id == "RegistrationModal") {
  //       $('#RegistrationModal').removeClass('show').css({'display': 'none'})
  //     }
  //  }
  }

  $(document).ready(function(){
    $('#email-form').on('submit', function(event){
        event.preventDefault()
        $.ajax({
            type: "POST",
            url: '/auth/validate/email/',
            data: $(this).serialize()+`&url=${$('#email-form').attr('url')}`,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            success: function(response){
                if (response.error){
                    $('#send-email').html(response.form)
                    $('#SendEmailModal').modal('show')
                    InputActive()
                }
                else{
                    // $('#SendEmailModal').modal('')
                    $('#messages-email').html('<h2>Email was send!</h2>')
                    $('#email-form').remove()
                }
            }
            })
        })
        }
    )
