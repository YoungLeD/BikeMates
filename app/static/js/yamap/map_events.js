function update_map_objects(o) {
    myPoints = o;
    if (objects) {
        objects.removeFromMap(myMap);
    }
    post_init();
}
function bindEvents() {
    myMap.events.add('click', EventClick);
    myMap.events.add('contextmenu', EventContextmenu);
    myMap.events.add('actionend', function (e) {
        closeNav();
        var new_objects = get_events(myMap.getBounds(), ['coords', 'name', 'description', 'creator_id']);
        update_map_objects(new_objects);
    });

    myCircle.events.add('dragend', function (e) {
        myCircleCoords = myCircle.geometry.getCoordinates();
        CircleSearchInside();
    });
    myCircle.events.add('click', CircleClick);
    myCircle.events.add('drag', CircleSearchInside);
}
function EventClick(e) {
    e.preventDefault();
    sourcePointCoords = e.get('coords');
    // Если метка уже создана – просто передвигаем ее.
    myMap.geoObjects.remove(sourcePoint);
    if (sourcePoint) {
        sourcePoint.balloon.close();
        sourcePoint.geometry.setCoordinates(sourcePointCoords);
        myMap.geoObjects.add(sourcePoint);
    }
    // Если нет – создаем.
    else {
        sourcePoint = createPlacemark(sourcePointCoords);
        myMap.geoObjects.add(sourcePoint);
        // Слушаем событие окончания перетаскивания на метке.
        sourcePoint.events.add('dragend', function () {
            getAddress(sourcePoint.geometry.getCoordinates());
            sourcePointCoords = sourcePoint.geometry.getCoordinates();
        });
    }
    getAddress(sourcePointCoords);
}
// Даблклик (вызов меню как бы)
function EventContextmenu(e) {
    if (!myCircle.properties.get('id')) //Если круга не существует...
    {
        myMap.geoObjects.add(myCircle); //...то создаем его.
    }
    e.preventDefault();
    myCircleCoords = e.get('coords');
    CircleUpd(myCircleCoords, radius * 1000);
    openNav();
    // ------
}
// Функция клика на круг
function CircleClick(e) {
    e.preventDefault();
    myMap.controls.add(myCircleButton);
}
// Функция поиска внутри
function CircleSearchInside() {
    // Объекты, попадающие в круг, будут становиться красными.
    objects_inside = [];
    var InsideCircle = objects.searchInside(myCircle);
    for (var i = 0, l = InsideCircle.getLength(); i < l; i++) {
        var current_object = InsideCircle.get(i); //Возвращает объект по индексу, объект типа IGeoObject
        //alert(current_object.properties.get('name'));
        objects_inside.push({
            name: current_object.properties.get('name'),
            url: "#"
        }); //позже тут будер урла, но сейчас ее нет ><
    }
    //Красим объекты внутри
    InsideCircle.setOptions('preset', 'islands#redCircleDotIcon');
    // Оставшиеся объекты - синими.
    objects.remove(InsideCircle).setOptions('preset', 'islands#lightBlueCircleDotIcon');
    sideUPD(objects_inside);
}

// > Вспомогательные функции
// Выставление sourcePoint адресса
function getAddress(coords) {
    sourcePoint.properties.set('iconCaption', 'поиск...');
    ymaps.geocode(coords).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0);
        sourcePoint.properties.set('iconCaption', firstGeoObject.properties.get('name'));
    });
}
// Изменение круга под актуальные значения
function CircleUpd(coords, rad) {
    myCircle.geometry.setCoordinates(coords);
    myCircleCoords = coords;
    myCircle.geometry.setRadius(rad);
    radius = rad / 1000;
    CircleSearchInside();
}
// Функция изменения радиуса NOT YET
// > функции возвращающие ymaps объекты
//Метка
function createPlacemark(coords) {
    return new ymaps.Placemark(coords, {
        iconCaption: 'поиск...'
    }, {
        balloonContentLayout: SrcPointBallonContentLayout,
        preset: 'islands#blueDotIconWithCaption',
        draggable: true
    });
};
