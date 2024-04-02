// const sendUsernameEmail = document.querySelector('#send-username-email');
// const sendPasswordEmail = document.querySelector('#send-password-email');

// function sendEmail(button, title, type){
//     const name = button.previousSibling.previousSibling.querySelector('.form-label').value;
//     const email = button.previousSibling.querySelector('.form-label').value;
//     console.log(name, email);
//     button.addEventListener('click', (e) => {
//         fetch('/email', {
//             method: 'POST',
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body:JSON.stringify({
//                 title: title,
//                 body:  type,
//                 type:  type,
//                 name:  name,
//                 email: email
//             })
//         })
//         .then((response) => {
//             // location.replace('/login');
//             console.log("response:", response);
//         })
//         .then((error) => console.log("error:", error))
//     })
// }

// function onSubmit(event){
//     event.preventDefault();
//     console.log(event);
// }

// sendEmail(sendPasswordEmail, '아이디 찾기', 'username');
// sendEmail(sendUsernameEmail, '비밀번호 재설정하기', 'password');

// const forms = document.querySelectorAll('.needs-validation');
// forms.forEach((form) => {
//     form.addEventListener("submit", onSubmit);
// })
