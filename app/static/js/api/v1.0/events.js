var api_events_url = api_url + '/events';
function get_events(area, fields) {
    var url = api_events_url + '?';
    if (area) {
        url += '&coords=' + area;
    }
    if (fields) {
        url += '&fields=' + fields;
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}

function get_events_by_search(search, fields) {
    var url = api_events_url + '?';
    url += '&search=' + search;
    if (fields) {
        url += '&fields=' + fields;
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}

function create_event(params) {
    return api_ajax(
        'POST',
        api_events_url,
        params
    ).responseJSON;
}

function get_event_by_id(event_id, fields) {
    var url = api_events_url + '/' + event_id + '?';
    if (fields) {
        url += '&fields=' + fields
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}

function update_event(event_id, params) {
    var url = api_events_url + '/' + event_id;
    return api_ajax(
        'PUT',
        url,
        params
    ).responseJSON;
}

function delete_event(event_id) {
    var url = api_events_url + '/' + event_id;
    return api_ajax(
        'DELETE',
        url
    ).responseJSON;
}
function part_in_event(event_id) {
    var url = api_events_url + '/' + event_id;
    return api_ajax(
        'POST',
        url
    ).responseJson;
}