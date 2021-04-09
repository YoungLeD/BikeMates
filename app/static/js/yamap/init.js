// Общие переменные
var myMap; // Карта +
var center_coords = [55.753994, 37.622093]; // Центральные коорды

var myPoints = []; //

var objects; //Объект с точками geoQuery
var allroutes; //Объект с ломаными geoQuery
var objects_inside = []; // объекты внутри круга, по умолчанию - все объекты

var myCircle; // Круг поиска +
var myCircleCoords; // Координаты центра круга +
var myCircleButton; // Окошко при нажатии на круг
var Circle_pos = {
    bottom: '85px',
    right: '15px'
};
var myCircleContentLayout; // Стиль окна круга
var radius = 10; // Радиус круга

var sourcePoint; // Точка на карте, ставиться на 'click' +
var sourcePointCoords; // Координаты точки(метки) +

var SrcPointBallonContentLayout; // Стиль балуна точки

var PointCreatedBallonContentLayout; // Стиль балуна евентов
var PathCreatedBallonContentLayout; // Стиль балуна пути, который создан

var SearchNearButtonLayout;
var SearchNear;
var SearchNearPos = {
    top: '15px',
    left: '15px'
};

var RoutesCreatorLayout;
var RoutesCreator;

var RouteCreating = false;

var RoutesModeButtonLayout;
var RoutesMode;
var RoutesModePos = {
    top: '15px',
    right: '15px'
};

var myRoute;

var geoloc_coords = [55.75396, 37.620393];

var ZoomLayout; // Стиль кнопок зума
var Zoom_pos = {
    bottom: '82px',
    left: '15px'
};

function init() {
    myMap = new ymaps.Map('map', {
        center: center_coords,
        zoom: 10,
        controls: []
    }, {});
    // ------------
    initLayouts();
    var geolocation = ymaps.geolocation;
    myCircle = createCircle();
    myMap.controls.add(createCustomControl(Zoom_pos, ZoomLayout));

    SearchNear = createCustomControl(SearchNearPos, SearchNearButtonLayout);
    myMap.controls.add(SearchNear);

    RoutesMode = createCustomControl(RoutesModePos, RoutesModeButtonLayout);
    RoutesCreator = createCustomControl(RoutesModePos, RoutesCreatorLayout);
    myMap.controls.add(RoutesMode);

    myCircleButton = createCustomControl(Circle_pos, myCircleContentLayout);

    bindEvents();
    post_init();
    show_routes(get_routes(['name', 'points', 'id']));
    geolocation.get({
        provider: 'yandex',
        mapStateAutoApply: false
    }).then(function (result) {
        geoloc_coords = result.geoObjects.position;
    });

    geolocation.get({
        provider: 'browser',
        mapStateAutoApply: true
    }).then(function (result) {
        console.log(result);
        geoloc_coords = result.geoObjects.position;
    });
    /*
     myRoute = new ymaps.Polyline([
     // Указываем координаты вершин.
     geoloc_coords
     ], {}, {
     // Задаем опции геообъекта.
     // Цвет с прозрачностью.
     strokeColor: "#00000088",
     // Ширину линии.
     strokeWidth: 4
     });
     myMap.geoObjects.add(myRoute);
     myRoute.editor.startEditing();
     myRoute.editor.startDrawing();*/
}

function post_init() {
    if(RouteCreating){
        return 0;
    }
    var map_objects = [];
    myPoints = get_events(myMap.getBounds(), ["coords", "name", "id"]);
    for (var i = 0, l = myPoints.length; i < l; i++) {
        var current_point = myPoints[i];
        objects_inside.push({
            name: current_point["name"],
            url: '#'
        });
        map_objects.push({
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: current_point["coords"]
            },
            options: {
                preset: 'islands#lightBlueCircleDotIcon',
                balloonContentLayout: PointCreatedBallonContentLayout
            },
            properties: {
                name: current_point["name"],
                balloonContent: current_point["id"]
            }
        });
    }
    objects = ymaps.geoQuery({
        type: 'FeatureCollection',
        features: map_objects
    });
    objects.addToMap(myMap);
    if (myCircle.geometry._map == null) //Если круга не существует...
    {
        console.log("post_init");
    }
    else {
        console.log("WTF");
        CircleSearchInside();
    }
}
function show_routes(routes) {
    var map_objects = [];
    for (var i = 0; i < routes.length; i++) {
        var current_route = routes[i];
        map_objects.push({
            type: 'Feature',
            geometry: {
                type: 'LineString',
                coordinates: current_route.points
            },
            options: {
                // Задаем опции геообъекта.
                balloonCloseButton: true,
                // Цвет линии.
                strokeColor: "#2196f3",
                // Ширина линии.
                strokeWidth: 8,
                // Коэффициент прозрачности.
                strokeOpacity: 1,
                balloonContentLayout: PathCreatedBallonContentLayout

            },
            properties: {
                balloonContent: current_route.id
            }
        });
    }
    allroutes = ymaps.geoQuery({
        type: 'FeatureCollection',
        features: map_objects
    });
    allroutes.addToMap(myMap);
}
function clearMap() {
    if (objects) {
        objects.removeFromMap(myMap);
    }
    allroutes.removeFromMap(myMap);
}