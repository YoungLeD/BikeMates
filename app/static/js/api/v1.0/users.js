var api_users_url = api_url + '/users';
function get_users(fields) {
    var url = api_users_url + '?';
    if (fields) {
        url += '&fields=' + fields;
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}

function get_user_by_id(user_id, fields) {
    var url = api_users_url + '/' + user_id + '?';
    if (fields) {
        url += '&fields=' + fields;
    }
    return api_ajax(
        'GET',
        url
    ).responseJSON;
}

function update_user(user_id, params) {
    var url = api_users_url + '/' + user_id;
    return api_ajax(
        'PUT',
        url,
        params
    ).responseJSON;
}