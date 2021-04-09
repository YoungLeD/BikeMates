var auth_url = api_url + '/auth';
function auth(username, password) {
    var res = api_ajax(
        'POST',
        auth_url,
        {
            username: username,
            password: password
        }
    ).responseJSON;
    localStorage.setItem('access_token', res['access_token']);
    localStorage.setItem('access_token_expires_at', res['access_token_expires_at']);
    localStorage.setItem('refresh_token', res['refresh_token']);
    var now = (new Date()).getTime();
    var expires_in = res['access_token_expires_at'] * 1000 - now;
    var update_before = 60000;
    if (expires_in > 300000) {
        update_before = 120000;
    } else if (expires_in < 120000) {
        update_before = expires_in / 2;
    }
    setTimeout(refresh_token, expires_in - update_before);
    return res;
}