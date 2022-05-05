
$(document).ready(function(){

    $('#login-btn').click(() => {
        let username = $('#username').val();
        let password = $('#password').val();
        $('#extra-message-login').empty();
        $.ajax('http://127.0.0.1:8081/users/login', {
            type: 'POST',
            data: { username, password },
            statusCode: {
                200: (res) => {
                    $('#username').val('');
                    $('#password').val('');
                    $('#extra-message-login').empty();
                    localStorage.setItem('access_token', res);
                    window.location.href = "/home";
                },
                403: () => {
                    $('#extra-message-login').append(`
                       Username or password are wrong
                    `);
                },
                500: () => {
                    $('#extra-message-login').append(`
                       'Unknown error'
                    `);
                }
            }
        });

    });

    $('#create-account').click(() => {
        let username = $('#new-username').val();
        let password = $('#new-password').val();
        $('#extra-message-register').empty();
        $.ajax('http://127.0.0.1:8081/users', {
            type: 'POST',
            data: { username, password },
            statusCode: {
                200: (res) => {
                    $('#new-username').val('');
                    $('#new-password').val('');
                    $('#extra-message-register').append(`
                       Account created successfully!
                    `);
                },
                400: () => {
                    $('#extra-message-register').append(`
                       You did not send one of the parameters
                    `);
                },
                409: () => {
                    $('#extra-message-register').append(`
                       An user already exists
                    `);
                },
                500: () => {
                    $('#extra-message-register').append(`
                       'Unknown error'
                    `);
                }
            }
        });
    });
});