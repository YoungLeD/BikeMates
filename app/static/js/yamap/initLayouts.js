function initLayouts() {
    // Стиль "балуна" для точки на карте (aka sourcePoint)
    // Стиль кнопок + / -
    ZoomLayout = ymaps.templateLayoutFactory.createClass("<div>" +
        "<div id='zoom-in' class='btn btn-default'><i class='glyphicon glyphicon-plus'></i></div><br>" + "<br>" +
        "<div id='zoom-out' class='btn btn-default'><i class='glyphicon glyphicon-minus'></i></div>" +
        "</div>", {
        build: function () {
            // Вызываем родительский метод build.
            ZoomLayout.superclass.build.call(this);
            // Привязываем функции-обработчики к контексту и сохраняем ссылки
            // на них, чтобы потом отписаться от событий.
            this.zoomInCallback = ymaps.util.bind(this.zoomIn, this);
            this.zoomOutCallback = ymaps.util.bind(this.zoomOut, this);
            // Начинаем слушать клики на кнопках макета.
            $('#zoom-in').bind('click', this.zoomInCallback);
            $('#zoom-out').bind('click', this.zoomOutCallback);
        },
        clear: function () {
            // Снимаем обработчики кликов.
            $('#zoom-in').unbind('click', this.zoomInCallback);
            $('#zoom-out').unbind('click', this.zoomOutCallback);
            // Вызываем родительский метод clear.
            ZoomLayout.superclass.clear.call(this);
        },
        zoomIn: function () {
            var map = this.getData().control.getMap();
            map.setZoom(map.getZoom() + 1, {
                checkZoomRange: true
            });
        },
        zoomOut: function () {
            var map = this.getData().control.getMap();
            map.setZoom(map.getZoom() - 1, {
                checkZoomRange: true
            });
        }
    });

    SrcPointBallonContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="row" style="margin: 10px;">' +
        '<input class="form-control" id="inputName" placeholder="Название события"><br>' +
        '<textarea type="text" class="form-control" placeholder="Описание события" id="description"></textarea><br>' +
        '<center> ' +
        '<button class="btn btn-success" style="margin-top:10px" id="createSrcPoint"> <i class="glyphicon glyphicon-pencil"></i> Создать событие</button> <br>' +
        '<button class="btn btn-danger" style="margin-top:10px" id="closeSrcPoint"><i class="glyphicon glyphicon-remove"></i> Закрыть</button>' +
        '</center' +
        '</div>', {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                // Сначала вызываем метод build родительского класса.
                SrcPointBallonContentLayout.superclass.build.call(this);
                // А затем выполняем дополнительные действия.
                $('#closeSrcPoint').bind('click', this.onCloseClickSrcPoint);
                $('#createSrcPoint').bind('click', this.createSrcPoint);
            },
            // Аналогично переопределяем функцию clear, чтобы снять
            // прослушивание клика при удалении макета с карты.
            clear: function () {
                // Выполняем действия в обратном порядке - сначала снимаем слушателя,
                // а потом вызываем метод clear родительского класса.
                $('#closeSrcPoint').unbind('click', this.onCloseClickSrcPoint);
                $('#createSrcPoint').unbind('click', this.createSrcPoint);
                SrcPointBallonContentLayout.superclass.clear.call(this);
                // $('#close').unbind('click', this.onCloseClick)
            },
            onCloseClickSrcPoint: function () {
                myMap.geoObjects.remove(sourcePoint); //Убирает placemark
            },
            createSrcPoint: function () {
                var event_id = create_event({
                    name: document.getElementById('inputName').value,
                    desc: document.getElementById('description').value,
                    coords: sourcePointCoords,
                    date_time: (Date.now() - Date.now() % 1000) / 1000
                });
                myPoints += {
                    coords: sourcePointCoords,
                    description: document.getElementById('description').value,
                    id: event_id,
                    name: document.getElementById('inputName').value,
                };
                post_init();
                myMap.geoObjects.remove(sourcePoint); //Убирает placemark
            }
        });

    PointCreatedBallonContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="row" style="margin: 10px;"><input type="hidden" id="id" value="{{ properties.balloonContent }}">' +
        '<strong>Название события: </strong><div class="text-justify" id="name"></div>' +
        '<strong>Описание события: </strong><div class="text-justify" id="desc"></div>' +
        '<strong>Создано: </strong><div class="text-justify" id="date_time"></div>' +
        '<strong>Создатель события: </strong><div class="text-justify" id="creator"></div>' +
        '<button class="btn btn-danger" id="delete_event">Удалить событие</button>' +
        '<button class="btn btn-primary" id="join_event">Участвовать</button>',
        {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                // Сначала вызываем метод build родительского класса.
                PointCreatedBallonContentLayout.superclass.build.call(this);
                var point_id = $('#id').val();
                var inform = get_event_by_id(point_id, ["name", "description", "date_time", "creator_id"]);
                if (user_id != inform.creator_id) {
                    document.getElementById("delete_event").style.display = 'none';
                    $('#join_event').bind('click', this.onClickPart);
                }
                else {
                    $('#delete_event').bind('click', this.onClickDelete);
                    document.getElementById("join_event").style.display = 'none';
                }
                $('#name').html(inform.name);
                $('#desc').html(inform.description);
                var time = new Date(inform.date_time * 1000);
                $('#date_time').html(time);
                // $('#date_time').html(time.getHours() + ":" + time.getMinutes() +
                //     " " + time.getDate() + "." + time.getMonth() + "." + time.getFullYear());
                $('#creator').html('<a href="/profile/' + inform.creator_id + '">' + get_user_by_id(inform.creator_id, ["name"]).name + '</a>');
            },
            clear: function () {
                // Выполняем действия в обратном порядке - сначала снимаем слушателя,
                // а потом вызываем метод clear родительского класса.
                $('#delete_event').unbind('click', this.onClickDelete);
                $('#join_event').unbind('click', this.onClickPart);
                PointCreatedBallonContentLayout.superclass.clear.call(this);
            },
            onClickDelete: function () {
                delete_event($('#id').val());
                var new_objects = get_events(myMap.getBounds(), ['coords', 'name', 'description', 'creator_id']);
                update_map_objects(new_objects);
            },
            onClickPart: function () {
                part_in_event($('#id').val());
                var new_objects = get_events(myMap.getBounds(), ['coords', 'name', 'description', 'creator_id']);
                update_map_objects(new_objects);
            }
        });

    PathCreatedBallonContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="row" style="margin: 10px;"><input type="hidden" id="id" value="{{ properties.balloonContent }}">' +
        '<strong>Название маршурта: </strong><div class="text-justify" id="name"></div>' +
        '<strong>Описание маршурта: </strong><div class="text-justify" id="desc"></div>' +
        '<strong>Создано: </strong><div class="text-justify" id="date_time"></div>' +
        '<strong>Создатель маршрута: </strong><div class="text-justify" id="creator"></div>',
        {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                // Сначала вызываем метод build родительского класса.
                PathCreatedBallonContentLayout.superclass.build.call(this);
                var point_id = $('#id').val();
                var inform = get_route_by_id(point_id, ["name", "desc", "creator_id"])
                $('#name').html(inform.name);
                $('#desc').html(inform.desc);
                // var time = new Date(inform.date_time * 1000);
                $('#date_time').html("пока не ясно");
                // $('#creator').html(get_user_by_id(inform.creator_id, ["name"]).name);
                $('#creator').html('<a href="/profile/' + inform.creator_id + '">' + get_user_by_id(inform.creator_id, ["name"]).name + '</a>');
            },
            clear: function () {
                // Выполняем действия в обратном порядке - сначала снимаем слушателя,
                // а потом вызываем метод clear родительского класса.
                PathCreatedBallonContentLayout.superclass.clear.call(this);
                // $('#close').unbind('click', this.onCloseClick)
            }
        });

    myCircleContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="container-fluid" style="background: rgb(255, 255, 255); padding: 18px;">' +
        '<h4 id="RadVal"></h4>' +
        '<input type="text" id="RadIn"><br><br>' +
        '<button type="confirm" class="btn btn-success" id="confirmCircle">Применить</button> <button class="btn btn-danger" id="closeCircle">Закрыть</button>' +
        '</div>', {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                // Сначала вызываем метод build родительского класса.
                myCircleContentLayout.superclass.build.call(this);
                // А затем выполняем дополнительные действия.
                $('#confirmCircle').bind('click', this.onConfirmClickCircle);
                $('#closeCircle').bind('click', this.onCloseClickCircle); // Функция закрывающая текущее окошко(ну или можно его просто закрывать ака controls.remove)
                $('#RadVal').html("Радиус: " + radius + " км");
                RadIn.value = radius;
            },
            // Аналогично переопределяем функцию clear, чтобы снять
            // прослушивание клика при удалении макета с карты.
            clear: function () {
                // Выполняем действия в обратном порядке - сначала снимаем слушателя,
                // а потом вызываем метод clear родительского класса.
                $('#confirmCircle').unbind('click', this.onConfirmClickCircle);
                $('#closeCircle').unbind('click', this.onCloseClickCircle);
                myCircleContentLayout.superclass.clear.call(this);
            },
            onConfirmClickCircle: function () {
                if (!isNaN(RadIn.value)) { //Проверка что введено число
                    CircleUpd(myCircleCoords, RadIn.value * 1000);
                    $('#RadVal').html("Радиус: " + radius + " км");
                    openNav();
                } else {
                    alert("Введите корректные данные");
                }
            },
            onCloseClickCircle: function () {
                myMap.controls.remove(myCircleButton);
            }
        });

    SearchNearButtonLayout = ymaps.templateLayoutFactory.createClass(
        '<button class="btn btn-success" id="search"> <i class="glyphicon glyphicon-search"></i> Найти события рядом</button>',
        {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                SearchNearButtonLayout.superclass.build.call(this);
                if (RouteCreating) {
                    myMap.controls.remove(SearchNear);
                }
                $('#search').bind('click', this.SearchClick);
            },
            clear: function () {
                $('#search').unbind('click', this.SearchClick);
                SearchNearButtonLayout.superclass.clear.call(this);
            },
            SearchClick: function () {
                myMap.setCenter(geoloc_coords, 12);
                if (myCircle.geometry._map == null) //Если круга не существует...
                {
                    myMap.geoObjects.add(myCircle); //...то создаем его.
                }
                myCircleCoords = geoloc_coords;
                radius = 2;
                CircleUpd(myCircleCoords, radius * 1000);
                openNav();
            }
        });

    RoutesModeButtonLayout = ymaps.templateLayoutFactory.createClass(
        '<button class="btn btn-primary" id="routesMode"> <i class="glyphicon glyphicon-road"></i> Режим создания маршрута</button>',
        {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                RoutesModeButtonLayout.superclass.build.call(this);
                $('#routesMode').bind('click', this.routesMode);
            },
            clear: function () {
                $('#routesMode').unbind('click', this.routesMode);
                RoutesModeButtonLayout.superclass.clear.call(this);
            },
            routesMode: function () {
                myMap.geoObjects.remove(myRoute);
                myMap.setCenter(geoloc_coords, 15);
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

                // Добавляем линию на карту.
                myMap.geoObjects.add(myRoute);

                // Включаем режим редактирования.
                myRoute.editor.startDrawing();
                myMap.controls.remove(RoutesMode);
                myMap.controls.add(RoutesCreator);
                clearMap();
            }
        });


    RoutesCreatorLayout = ymaps.templateLayoutFactory.createClass(
        '<div class="container-fluid" style="background: rgb(255, 255, 255); padding: 18px;">' +
        '<input class="form-control" id="inputName" placeholder="Название маршрута"><br>' +
        '<textarea type="text" class="form-control" placeholder="Описание маршрута" id="description"></textarea><br>' +
        '<button class="btn btn-success" id="createRoute"> <i class="glyphicon glyphicon-pencil"></i> Создать маршрут</button> ' +
        '<button class="btn btn-danger" id="cancelRoute"><i class="glyphicon glyphicon-remove"></i> Закрыть</button>' +
        '</div>',
        {
            // Переопределяем функцию build, чтобы при создании макета начинать
            // слушать событие click на кнопке-счетчике.
            build: function () {
                RoutesCreatorLayout.superclass.build.call(this);
                $('#createRoute').bind('click', this.createRoute);
                $('#cancelRoute').bind('click', this.closeRoute);
                RouteCreating = true;
                myMap.controls.remove(SearchNear);
                myMap.geoObjects.remove(sourcePoint);
            },
            clear: function () {
                RouteCreating = false;
                myMap.geoObjects.remove(myRoute);
                myMap.controls.add(RoutesMode);
                myMap.controls.add(SearchNear);
                post_init();
                show_routes(get_routes(['name', 'points', 'desc']));
                $('#createRoute').unbind('click', this.createRoute);
                $('#cancelRoute').unbind('click', this.closeRoute);
                RoutesCreatorLayout.superclass.clear.call(this);
            },
            createRoute: function () {
                var params = {
                    name: document.getElementById('inputName').value,
                    desc: document.getElementById('description').value,
                    points: myRoute.geometry._coordPath._coordinates
                };
                console.log(params);
                create_route(params);
                RouteCreating = false;
                myMap.controls.remove(RoutesCreator);
            },
            closeRoute: function () {
                RouteCreating = false;
                myMap.controls.remove(RoutesCreator);
            }
        });


    // ------------
}
