//! 초기 창 크기에 따른 폰트사이즈 (맥북에어: 1444 * 732)
// function changeFontSize() {
//     var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
//     var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
//     var fontSizeByWidth = windowWidth / 93;
//     var fontSizeByHeight = windowHeight / 48;
//     console.log(fontSizeByWidth, fontSizeByHeight);
//     if (fontSizeByWidth >= fontSizeByHeight) {
//         var fontSize = fontSizeByHeight;
//     } else {
//         var fontSize = fontSizeByWidth;
//     }

//     document.documentElement.style.fontSize = fontSize + "px";
//     console.log("창: (" + windowWidth + "px x " + windowHeight + "px)"  + ", 폰트 사이즈: " + fontSize);
// }
// //! 초기 창 띄율 때/ 창 크기 바뀔 때마다 폰트사이즈 변경
// window.addEventListener("DOMContentLoaded", changeFontSize);
// window.addEventListener("resize", changeFontSize);
