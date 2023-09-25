const copyAddressBtns = document.querySelectorAll(".copy_address_btn");
copyAddressBtns.forEach((btn) => {
    btn.onclick = () => {
        const address = btn.dataset.address;
        console.log(address);
        window.navigator.clipboard.writeText(address).then(() => {
            alert("주소 복사 완료!");
        });
    };
})