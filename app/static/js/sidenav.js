/* Set the width of the side navigation to 250px */
function openNav() {
	sideUPD(objects_inside);
    document.getElementById("mySidenav").style.width = "20%";
    myMap.controls.remove(SearchNear);
    //alert("OPENED");
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    destroyCircle();
    myMap.controls.add(SearchNear);
    //alert("CLOSED");
}