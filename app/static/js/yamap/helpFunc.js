function createCircle() {
    return new ymaps.Circle([], {
        hintContent: "Нажать для изменения радиуса<br>Можно двигать"
    }, {
        draggable: true,
        // Цвет заливки.
        // Последний байт (77) определяет прозрачность.
        // Прозрачность заливки также можно задать используя опцию "fillOpacity".
        fillColor: "#2196f325",
        // Цвет обводки.
        strokeColor: "#2196f3",
        // Прозрачность обводки.
        strokeOpacity: 1.0,
        // Ширина обводки в пикселях.
        strokeWidth: 2,
        // наличие подсказки
        hasHint: false
    });
};

//Функция создания кастомного контролера. Передается сначала координаты типа {left: ?, top: ?, bottom: ?, right: ?}, после layout ymaps.templateLayoutFactory.createClass
function createCustomControl(pos, customlayout) {
    return new ymaps.control.Button({
        options: {
            layout: customlayout,
            position: pos
        }
    });
};


function sideUPD(Events_inside) {
    var html_events = '<br><br><br><center>';
    for (var i = 0, l = Events_inside.length; i < l; i++) {
        html_events += '<a href=' + Events_inside[i].url + '>' + Events_inside[i].name + '</a>' + '\n'
    }
    ;
    html_events += '<a href="javascript:void(0)" class="button btn-danger button-outlined closesidebar" onclick="closeNav()" style="margin:20px;">Закрыть</a></center>'
    $('#mySidenav').html(html_events);
};

function destroyCircle() {
    myMap.geoObjects.remove(myCircle); //Убирает круг
    myMap.controls.remove(myCircleButton); //Убирает панель изменения радиуса
    objects.setOptions('preset', 'islands#lightBlueCircleDotIcon');
};
