var api_routes_url = api_url + '/routes';
function get_routes(fields) {
    var url = api_routes_url + '?';
    if (fields) {
        url += '&fields=' + fields;
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}
function create_route(params) {
    return api_ajax(
        'POST',
        api_routes_url,
        params
    ).responseJSON;
}
function get_route_by_id(route_id, fields) {
    var url = api_routes_url + '/' + route_id + '?';
    if (fields) {
        url += '&fields=' + fields
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}