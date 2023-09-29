const copyAddressBtns = document.querySelectorAll(".copy_address_btn");
copyAddressBtns.forEach((btn) => {
    btn.onclick = () => {
        const address = btn.dataset.address;
        window.navigator.clipboard.writeText(address).then(() => {
            alert("주소를 복사했습니다");
        });
    };
})

const copyContactBtns = document.querySelectorAll(".copy_contact_btn");
copyContactBtns.forEach((btn) => {
    btn.onclick = () => {
        const contact = btn.dataset.contact;
        window.navigator.clipboard.writeText(contact).then(() => {
            alert("연락처를 복사했습니다");
        });
    };
})