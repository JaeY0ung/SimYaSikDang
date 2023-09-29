var places = document.querySelectorAll('#address');

var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
    mapOption = { 
        center: new kakao.maps.LatLng(37.5657720, 126.9233857), // 지도의 중심좌표
        level: 8 // 지도의 확대 레벨
    };
var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 

var avgLat = 0;
var avgLng = 0;

places.forEach((place) => {
	var imageSize = new kakao.maps.Size(24, 35); 
	var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
	
	var marker = new kakao.maps.Marker({
		map: map, 
		position: new kakao.maps.LatLng(place.dataset.lng, place.dataset.lat),
		title : place.dataset.name, 
		image : markerImage,
		clickable: true
	});

	var infowindow = new kakao.maps.InfoWindow({
		position : new kakao.maps.LatLng(place.dataset.lng, place.dataset.lat), 
        content: `<div style="padding:0.2rem;">
					<a style="color:black;" href="${ place.dataset.placeurl }" style="color:blue" target="_blank">
						<b>${ place.dataset.name }</b>
					</a>
					<a style="color:green;" href="${ place.dataset.roadurl }" style="color:blue" target="_blank">
						<b>길찾기</b>
					</a>
				  </div>`,
		removable: true		
    });

	kakao.maps.event.addListener(marker, 'click', function() {
		infowindow.open(map, marker);  
  	});

	avgLat += parseFloat(place.dataset.lat);
	avgLng += parseFloat(place.dataset.lng);
	
});

avgLat /= places.length;
avgLng /= places.length;

// 지도 중심을 이동 시킵니다
// map.setCenter(new kakao.maps.LatLng(avgLng, avgLat));
// 지도 중심을 부드럽게 이동시킵니다
// 만약 이동할 거리가 지도 화면보다 크면 부드러운 효과 없이 이동합니다
map.panTo(new kakao.maps.LatLng(avgLng, avgLat));