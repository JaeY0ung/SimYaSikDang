const usernameInput = document.querySelector('#username');
const emailInput    = document.querySelector('#email');
const usernameCheckButton = document.querySelector('#username-check-button'); // 사용할 아이디 유효성 검사
const emailCheckButton    = document.querySelector('#email-check-button'); // 이메일 유효성 검사
let usernameUseButton = document.querySelector('#username-use-button');  // 아이디 사용 버튼
let emailUseButton    = document.querySelector('#email-use-button');  // 아이디 사용 버튼
let canUsernameChange = true;
let canEmailChange    = true;

const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
const passwordRegex = /^(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).*$/;

const rightComment = 'You can use!'     // '사용 가능한 아이디입니다' // TODO: (한글로 쓰면 수직으로 배열된다)
const wrongComment = 'Already used..'   // '사용중인 아이디입니다'
const emptyComment = 'Please fill it..' // '아이디를 입력해주세요'

document.addEventListener("DOMContentLoaded", function() {
  usernameCheckButton.addEventListener('click', (e) => {
    const username = usernameInput.value;
    const usernameComment = document.querySelector('#username-double-check-comment');
    if (username) { // 사용할 아이디 입력시에만 요청 보냄
      $.ajax({
        url: `/users?username=${username}`,
        method: 'GET',
        dataType: "json",
        success: function(response) {
          if (response.exist == 'true'){ // 사용중인 아이디일 떄
            usernameComment.textContent = wrongComment;
          }else {
            usernameComment.textContent = rightComment;
            usernameUseButton.style.display = 'block';
          }
        },
        error: function(error) {
          usernameComment.textContent = '';
          console.log('error', error);
        }
      });
    }else { // 사용할 아이디 값이 공백일 때
      usernameComment.textContent = emptyComment;
    }
  });

  emailCheckButton.addEventListener('click', (e) => {
    const email = emailInput.value;
    const emailComment = document.querySelector('#email-double-check-comment');
    if (email && emailRegex.test(email)) { // 사용할 이메일 입력시에만 요청 보냄
      $.ajax({
        url: `/users?email=${email}`,
        method: 'GET',
        dataType: "json",
        success: function(response) {
          if (response.exist == 'true'){ // 사용중인 이메일일 떄
            emailComment.textContent = wrongComment;
          }else { // 사용 가능한 이메일일 떄
            emailComment.textContent = rightComment;
            emailUseButton.style.display = 'block';
          }
        },
        error: function(error) {
          emailComment.textContent = '';
          console.log('error', error);
        }
      });
    }else if(email && !emailRegex.test(email)){ // 이메일 형식이 맞지 않을 때
      emailComment.textContent = '잘못된 이메일 형식입니다';
    }else { // 사용할 이메일 값이 공백일 때
      emailComment.textContent = emptyComment;
    }
  });


  usernameUseButton.addEventListener('click', (event) => {
    if (canUsernameChange) { // 사용하기 버튼 클릭시
      usernameInput.readOnly = true;
      usernameInput.style.backgroundColor = '#888888';
      canUsernameChange = false; // 못 바꾸게 하기
      usernameUseButton.textContent = '바꾸기';
    }else { // 바꾸기 버튼 클릭시
      usernameInput.readOnly = false;
      usernameInput.style.backgroundColor = '#FFFFFF';
      canUsernameChange = true; // 못 바꾸게 하기
      usernameUseButton.textContent = '사용하기';
  
    }
  })
  
  emailUseButton.addEventListener('click', (event) => {
    if (canEmailChange) { // 사용하기 버튼 클릭시
      emailInput.readOnly = true;
      emailInput.style.backgroundColor = '#888888';
      canEmailChange = false; // 못 바꾸게 하기
      emailUseButton.textContent = '바꾸기';
    }else { // 바꾸기 버튼 클릭시
      emailInput.readOnly = false;
      emailInput.style.backgroundColor = '#FFFFFF';
      canEmailChange = true; // 못 바꾸게 하기
      emailUseButton.textContent = '사용하기';
    }
  })
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

const registerForm = document.querySelector('#register-form');
registerForm.addEventListener("submit", (event) => {
  // 경고는 최신 한 개만 뜨게 하기 위해 if문이 아니라 else if 문 사용
  if (canUsernameChange){ // 둘 중 하나라도 바뀔 수 있다면
    event.preventDefault(); // 페이지 새로고침 막음
    document.querySelector('#submit-check-comment').textContent = "아이디 '사용하기' 버튼를 누르세요";
  }else if(canEmailChange){
    event.preventDefault(); // 페이지 새로고침 막음
    document.querySelector('#submit-check-comment').textContent = "이메일 '사용하기' 버튼를 누르세요";
  }
})