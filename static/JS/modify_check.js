const registerForm       = document.querySelector('#register-form');
const usernameInput      = document.querySelector('#username');
const passwordInput      = document.querySelector('#password');
const passwordNewInput   = document.querySelector('#password-new');
const nameInput          = document.querySelector('#name');
const nicknameInput      = document.querySelector('#nickname');
const emailInput         = document.querySelector('#email');
const contactInput       = document.querySelector('#contact');
const submitButton       = document.querySelector('#submit');

const usernameComment      = document.querySelector('#username-comment');
const passwordComment      = document.querySelector('#password-comment');
const passwordNewComment   = document.querySelector('#password-new-comment');
const nameComment          = document.querySelector('#name-comment');
const nicknameComment      = document.querySelector('#nickname-comment');
const emailComment         = document.querySelector('#email-comment');
const contactComment       = document.querySelector('#contact-comment');
const submitComment        = document.querySelector('#submit-comment');

const usernameRegex    = /^[a-zA-Z0-9]{3,20}$/;
const passwordRegex    = /^(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
const koreanNameRegex  = /^[가-힣\s]{2,5}$/;
const englishNameRegex = /^[A-Za-z]{2,50}$/;
const nicknameRegex    = /^[A-Za-z0-9_\-가-힣]{1,8}$/;
const emailRegex       = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
const contactRegex     = /^010-\d{4}-\d{4}$/; // /^\d{3}-\d{4}-\d{4}$/

const validationChecks = {
  name:true,
  username: true,
  nickname:true,
  contact:true, // 선택
  email:true,
  password: false,
  passwordNew:false,
};

document.addEventListener("DOMContentLoaded", function() {
  // usernameInput.addEventListener('input', (e) => {
  //   const username = usernameInput.value;
  //   if (username) { // 사용할 아이디 입력시에만 요청 보냄
  //     $.ajax({
  //       url: `/auth/check?username=${username}`,
  //       method: 'GET',
  //       dataType: "json",
  //       success: function(response) {
  //         if (response.exist == 'true'){
  //           usernameComment.style.color = 'red';
  //           usernameComment.textContent = '사용 중인 아이디입니다';
  //           validationChecks.username = false;
  //         }else if (usernameRegex.test(username)) {
  //           usernameComment.style.color = 'blue';
  //           usernameComment.textContent = '사용 가능한 아이디입니다';
  //           validationChecks.username = true;
  //         }else{
  //           usernameComment.style.color = 'red';
  //           usernameComment.textContent = '사용 불가한 아이디입니다';
  //           validationChecks.username = false;
  //         }
  //       },
  //       error: function(error) {
  //         usernameComment.style.color = 'red';
  //         usernameComment.textContent = 'error: ' + error;
  //         validationChecks.username = false;
  //       }
  //     });
  //   }else {
  //     usernameComment.style.color = 'red';
  //     usernameComment.textContent = '아이디를 입력헤주세요';
  //     validationChecks.username = false;
  //   }
  // });
  //!=========================================================
  passwordInput.addEventListener('input', (e) => {
    const password = passwordInput.value;
    if (password) { // 아이디 비밀번호가 맞는지 확인
      fetch('/auth/check', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            title: "POST User info",
            body: "POST User info",
            username: usernameInput.value,
            password: password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.exist == 'true'){
          passwordComment.style.color = 'blue';
          passwordComment.textContent = '비밀번호가 맞습니다';
          validationChecks.password   = true;
        }else{
          passwordComment.style.color = 'red';
          passwordComment.textContent = '비밀번호가 틀립니다';
          validationChecks.password   = false;
        }
      })
      .catch(error => {
        passwordComment.style.color = 'red';
        passwordComment.textContent = 'error: ' + error;
        validationChecks.password   = false;
      })
    }else {
      passwordComment.style.color = 'red';
      passwordComment.textContent = '비밀번호를 입력헤주세요';
      validationChecks.password   = false;
    }
  })
  //!=========================================================
  passwordNewInput.addEventListener('input', (e) => { // 새로운 비밀번호
    const passwordNew = passwordNewInput.value;
    if (passwordRegex.test(passwordNew)){
      passwordNewComment.style.color = 'blue';
      passwordNewComment.textContent = '사용 가능한 비밀번호입니다';
      validationChecks.passwordNew   = true;
    }else {
      passwordNewComment.style.color = 'red';
      passwordNewComment.textContent = '유효한 비밀번호가 아닙니다';
      validationChecks.passwordNew   = false;
    }
  })
  //!=========================================================
  nameInput.addEventListener('input', (e) => {
    const name = nameInput.value;
    if (koreanNameRegex.test(name) || englishNameRegex.test(name)){
      nameComment.style.color = 'blue';
      nameComment.textContent = '올바른 이름입니다';   
      validationChecks.name   = true;
    }else {
      nameComment.style.color = 'red';
      nameComment.textContent = '올바른 이름을 입력하세요';
      validationChecks.name   = false;
    }
  })
  //!=========================================================
  emailInput.addEventListener('input', (e) => {
    const email = emailInput.value;
    if (email && emailRegex.test(email)) { // 사용할 이메일 입력시에만 요청 보냄
      fetch('/auth/check', {
        method: 'PUT',
        headers: {
          'Content-Type': "application/json"
        },
        body: JSON.stringify({
          title:"Modify email",
          body: "Modify email",
          username:usernameInput.value,
          email:email
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.exist == 'true'){ 
          emailComment.style.color = 'red';
          emailComment.textContent = '사용 중인 이메일입니다';
          validationChecks.email   = false;
        }else {
          emailComment.style.color = 'blue';
          emailComment.textContent = '사용 가능한 이메일입니다';
          validationChecks.email   = true;
        }
      })
      .catch(error => {
        emailComment.style.color = 'red';
        emailComment.textContent = 'error: ' + error;
        validationChecks.email   = false;
      })
    }else if(email && !emailRegex.test(email)){
      emailComment.style.color = 'red';
      emailComment.textContent = '잘못된 이메일 형식입니다';
      validationChecks.email   = false;
    }else {
      emailComment.style.color = 'red';
      emailComment.textContent = '이메일을 입력해주세요';
      validationChecks.email   = false;
    }
  });
  //!=========================================================
  nicknameInput.addEventListener('input', (e) => {
    const nickname = nicknameInput.value;
    if (nickname) { // 닉네임 입력시에만 요청 보냄
      fetch('/auth/check', {
        method: 'PUT',
        headers: {
          'Content-Type': "application/json"
        },
        body: JSON.stringify({
          title: "Modify nickname",
          body: "Modify nickname",
          username: usernameInput.value,
          nickname: nickname
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.exist == 'true'){ 
          nicknameComment.style.color = 'red';
          nicknameComment.textContent = '사용 중인 닉네임입니다';
          validationChecks.nickname  = false;
        }else if (nicknameRegex.test(nickname)){
          nicknameComment.style.color = 'blue';
          nicknameComment.textContent = '사용 가능한 닉네임입니다';
          validationChecks.nickname   = true;
        }else { 
          nicknameComment.style.color = 'red';
          nicknameComment.textContent = '올바르지 않은 닉네임입니다';
          validationChecks.nickname   = false;
        }
      })
      .catch(error => {
        nicknameComment.style.color = 'red';
        nicknameComment.textContent = 'error: ' + error;
        validationChecks.nickname   = false;
      })
    }else {
      nicknameComment.style.color = 'red';
      nicknameComment.textContent = '닉네임을 입력해주세요';
      validationChecks.nickname   = false;
    }
  });
  //!=========================================================
  // 연락처(전화번호)에 하이픈(-) 넣기
  contactInput.addEventListener('input', (e) => {
    const contact = contactInput.value
    .replace(/[^0-9]/g, '')
    .replace(/^(\d{0,3})(\d{0,4})(\d{0,4})$/g, "$1-$2-$3").replace(/(\-{1,2})$/g, "");
    contactInput.value = contact;

    if (!contact || contactRegex.test(contact)) { // 공백이거나 정규식 (010-xxxx-xxxx)을 만족하면
      validationChecks.contact = true;
    }else {
      validationChecks.contact = false;
    }
  })
  //!=========================================================
  // Form 내 Enter 클릭 시 Form 제출 방지
  registerForm.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        return false;
    }
  });
  registerForm.addEventListener('submit', function(event) {
    event.preventDefault();
    // const formData = new FormData(registerForm);  //? 없당,,
    fetch('/auth/edit', {
      method: 'PUT',
      headers: {
        'Content-Type': "application/json"
      },
      body: JSON.stringify({
        title: "Modify nickname",
        body: "Modify nickname",
        name: nameInput.value,
        username: usernameInput.value,
        nickname: nicknameInput.value,
        contact: contactInput.value,
        email:emailInput.value,
        password: passwordInput.value,
        passwordNew: passwordNewInput.value,
        // formData: formData
      })
    }).then(request => request.json)
    .then(data => {
      location.replace('/');
    })
    .catch(error => console.log('error:', error))
  });
  //!=========================================================
  // 가입하기 클릭 시 조건 체크 후 제출
  submitButton.addEventListener('click', (event) => {
    if(!validationChecks.name){
      submitComment.textContent = '이름을 확인하세요';
      event.preventDefault();
    }else if (!validationChecks.username) {
      submitComment.textContent = '아이디를 확인하세요';
      event.preventDefault();
    }else if(!validationChecks.nickname){
      submitComment.textContent = '닉네임을 확인하세요';
      event.preventDefault();
    }else if(!validationChecks.contact){
      submitComment.textContent = '연락처를 확인하세요';
      event.preventDefault();
    }else if(!validationChecks.email){
      submitComment.textContent = '이메일을 확인하세요';
      event.preventDefault();
    }else if(!validationChecks.password){
      submitComment.textContent = '비밀번호를 확인하세요';
      event.preventDefault();
    }else if(!validationChecks.passwordNew){
      submitComment.textContent = '올바른 비밀번호가 아닙니다';
      event.preventDefault();
    }
  })
});

//! 부트 스트랩 Validation 코드
// (() => {
//     'use strict'
  
//     // Fetch all the forms we want to apply custom Bootstrap validation styles to
//     const forms = document.querySelectorAll('.needs-validation')
  
//     // Loop over them and prevent submission
//     Array.from(forms).forEach(form => {
//       form.addEventListener('submit', event => {
//         if (!form.checkValidity()) {
//           event.preventDefault()
//           event.stopPropagation()
//         }
  
//         form.classList.add('was-validated')
//       }, false)
//     })
// })()