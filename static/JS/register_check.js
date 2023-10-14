//! 사용할 아이디 유효성 검사
let usernameCheckButton = document.querySelector('#username-check-button');

document.addEventListener("DOMContentLoaded", function() {
  usernameCheckButton.addEventListener('click', (e) => {
    const userName = document.querySelector('#username').value;
    if (userName) {
      $.ajax({
        url: `/users?username=${userName}`,
        method: 'GET',
        dataType: "json",
        success: function(response) {
            if (response.exist == 'true'){ // 사용중인 아이디입니다
              document.querySelector('#username-invalid-feedback').textContent = '사용중인 아이디입니다';
              document.querySelector('#username-valid-feedback').textContent = '사용중인 아이디입니다';
            }else {
              $('#username-invalid-feedback').text('사용 가능한 아이디입니다');
              document.querySelector('#username-invalid-feedback').textContent = '사용 가능한 아이디입니다';
              document.querySelector('#username-valid-feedback').textContent = '사용 가능한 아이디입니다';
            }
        },
        error: function(error) {
          console.log('error', error);
        }
      });
    }else {
      document.querySelector('#username-invalid-feedback').textContent = '입력해주세요';
      document.querySelector('#username-valid-feedback').textContent = '입력해주세요';
    }
  });
});


//! 이메일 유효성 검사
let emailCheckButton = document.querySelector('#email-check-button');

document.addEventListener("DOMContentLoaded", function() {
  emailCheckButton.addEventListener('click', (e) => {
    const email = document.querySelector('#email').value;
    $.ajax({
      url: `/users?email=${email}`,
      method: 'GET',
      dataType: "json",
      success: function(response) {
          if (response.exist == 'true'){
            document.querySelector('#email-invalid-feedback').textContent = '사용중인 이매일입니다';
            document.querySelector('#email-valid-feedback').textContent = '사용중인 이매일입니다';
          }else {
            $('#email-invalid-feedback').text('사용 가능한 아이디입니다');
            document.querySelector('#email-invalid-feedback').textContent = '사용 가능한 이매일입니다';
            document.querySelector('#email-valid-feedback').textContent = '사용 가능한 이매일입니다';
          }
      },
      error: function(error) {
        console.log('error', error);
      }
    });
  });
});

//! 연락처(전화번호) 유효성 검사
const autoHyphen = (target) => {
    target.value = target.value
    .replace(/[^0-9]/g, '')
    .replace(/^(\d{0,3})(\d{0,4})(\d{0,4})$/g, "$1-$2-$3").replace(/(\-{1,2})$/g, "");
}


//! 부트 스트랩 Validation 코드
(() => {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
  
        form.classList.add('was-validated')
      }, false)
    })
})()