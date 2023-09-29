function moveToLogin(error){
    if (error.responseText == 'No User login'){
        location.replace('/auth/login');
    }
}

document.addEventListener("DOMContentLoaded", function() {

    const stars = document.querySelectorAll('.fa-star')

    stars.forEach((star) => {
        star.addEventListener('click', (e)=>{
            place_uuid = star.dataset.uuid;
            //! 좋아요 선택
            if(star.classList.contains('fa-regular')){
                $.ajax({
                    url: `/place/${place_uuid}/like`, // 요청을 보낼 URL
                    method: 'POST',
                    dataType: "text",
                    success: function(response) {
                        // 요청이 성공적으로 처리되면 클래스를 변경합니다.
                        star.classList.remove('fa-regular');
                        star.classList.add('fa-solid');
                    },
                    error: function(error) {
                        moveToLogin(error);
                    }
                });
                
            //! 좋아요 해제
            }else{
                $.ajax({
                    url: `/place/${place_uuid}/like`, // 요청을 보낼 URL
                    method: 'DELETE',
                    dataType: "text",
                    success: function(response) {
                        // 요청이 성공적으로 처리되면 클래스를 변경합니다.
                        star.classList.remove('fa-solid');
                        star.classList.add('fa-regular');
                    },
                    error: function(error) {
                        moveToLogin(error);
                    }
                });                
            }
        });
    });             
});