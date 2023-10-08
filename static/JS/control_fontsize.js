function handleResize() {
    var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var newFontSize =  windowWidth / 85.375 + "px";
    console.log("창의 너비: " + windowWidth + "px" + ", 폰트 사이즈: " + newFontSize);
    document.documentElement.style.fontSize = newFontSize;
}

//! 초기 창 크기에 따른 폰트사이즈
var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var newFontSize =  windowWidth / 85.375 + "px";
document.documentElement.style.fontSize = newFontSize;

//! 창 크기 바뀔 때마다
window.addEventListener("resize", handleResize);