const detailsElement = document.getElementById('details');
const summaryElement = document.getElementById('summary');

detailsElement.addEventListener('toggle', function () {
    if (detailsElement.open) {
        summaryElement.textContent = '닫기';
    } else {
        summaryElement.textContent = '펼치기';
    }
});