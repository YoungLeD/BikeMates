var api_refresh_token_url = api_url + '/refresh_token';
function refresh_token() {
    var r = api_ajax(
        'POST',
        api_refresh_token_url,
        null,
        {'Authorization': 'Bearer ' + localStorage.refresh_token}
    ).responseJSON;
    var access_token = r['access_token'];
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('access_token_expires_at', r['expires_at']);
    console.log('access_token has been refreshed');
    var now = (new Date()).getTime();
    var expires_in = r['expires_at'] * 1000 - now;
    var update_before = 60000;
    if (expires_in > 300000) {
        update_before = 120000;
    } else if (expires_in < 120000) {
        update_before = expires_in / 2;
    }
    setTimeout(refresh_token, expires_in - update_before);
    return access_token
}

function api_ajax(method, url, json_data, headers, async) {
    if (!async) {
        async = false
    }
    if (!headers) {
        headers = {}
    }
    if (!headers['Authorization']) {
        headers['Authorization'] = 'Bearer ' + localStorage.access_token;
    }
    var ajax_params = {
        method: method ? method : 'GET',
        url: url,
        headers: headers,
        data: JSON.stringify(json_data),
        async: !!async,
        contentType: 'application/json; charset=utf-8'
    };
    return $.ajax(ajax_params);
}