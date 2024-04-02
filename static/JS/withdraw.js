const withdrawButton = document.querySelector('#withdraw-button');
const withdrawButtonModal = document.querySelector('#withdraw-button-modal');
const modal = document.querySelector("#modal");
const closeBtn = modal.querySelector(".btn-close");

withdrawButton.addEventListener("click", (e) => {
    modal.style.display = "flex";
})

closeBtn.addEventListener("click", (e) => {
    modal.style.display = "none";
})

modal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        modal.style.display = "none"
    }
})

withdrawButtonModal.addEventListener('click' , (e) => {
    fetch('/auth/withdraw', {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            title: "Delete User",
            body: "Delete User",
        })
    })
    .then((response) => {
        location.replace('/');
        console.log("response:", response);
    })
    .catch((error) => console.log("error:", error))
});