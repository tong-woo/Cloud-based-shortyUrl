function reloadUrls(){
    $('.urls-box').empty();
    $.ajax("/", {
        type: 'GET',
        beforeSend: function(request) {
            request.setRequestHeader("x-access-token", localStorage.getItem('access_token'));
        },
        statusCode: {
            200: (data) => {
                console.log(data);
                $('.urls-box').empty();
                if (Object.entries(data).length < 1){
                    $('.urls-box').append(`
                        You have not shorten any URL
                    `);
                    return;
                }
                $('.urls-box').append(`
                    <h4> Your Urls: </h4>
                    ${Object.entries(data).map((e) => {
                        const shortened = e[0];
                        const original = e[1]
                        return `
                            <div class="url-total-container">
                                <div class="url-container">
                                    <a class="my_url" target="_blank" href="${`/${shortened}`}">
                                        ${shortened}
                                    </a>
                                    <div class="original-url" id='original-url-${shortened}'>
                                        ${original}
                                    </div>
                                    <div class="delete-url" style="cursor: pointer">
                                        <span id="edit-${shortened}" class="material-icons" style="color: #aaa"> edit </span>
                                        <span id="delete-${shortened}" class="material-icons" style="color: #bc0031">close</span>
                                    </div>
                                </div>
                                <div class="url-edit" id="url-edit-${shortened}">
                                </div>
                            </div>
                        `;
                    }).join(' ')}
                `);
                $('span[id|="delete"]').click(function(){
                    const urlId = $(this).attr('id');
                    $.ajax(`/${urlId.split('-')[1]}`, {
                        type: 'DELETE',
                        beforeSend: function(request) {
                            request.setRequestHeader("x-access-token", localStorage.getItem('access_token'));
                        },
                        statusCode: {
                            204: (res) => {
                                reloadUrls();
                            },
                            403: () => {
                                $('#extra-message').append(`
                                   'Unauthenticated'
                                `);
                            },
                            404: () => {
                                reloadUrls();
                            },
                            500: () => {
                                $('#extra-message').append(`
                                   'Unknown error'
                                `);
                            }
                        }
                    });
                });
                $('span[id|="edit"]').click(function(){
                    const urlId = $(this).attr('id').split('-')[1];
                    const originalUrl = $(`#original-url-${urlId}`).text().trim();
                    $(`#url-edit-${urlId}`).append(`
                        <input type="url" class="edit-url" placeholder=${`${originalUrl}`} value=${`${originalUrl}`}>
                        <span id=${`fedit-ok-${urlId}`} class="material-icons" style="color: #bc0031; cursor: pointer">check_circle</span>
                    `);
                    console.log(urlId, originalUrl);
                    $('.delete-url').css('display', 'none');
                    $('span[id|="fedit-ok"]').click(function(){
                        let newUrl = $('.edit-url').val();
                        $('#extra-message').empty();
                        $.ajax(`/${urlId}`, {
                            beforeSend: function(request) {
                                request.setRequestHeader("x-access-token", localStorage.getItem('access_token'));
                            },
                            type: 'PUT',
                            data: { url: newUrl },
                            statusCode: {
                                200: (res) => {
                                    $(`#url-edit-${urlId}`).empty();
                                    $('#new-url').val('');
                                    $('#extra-message').empty();
                                    reloadUrls();
                                },
                                400: () => {
                                    $('#extra-message').append(`
                                       URL format is not correct
                                    `);
                                },
                                403: () => {
                                    $('#extra-message').append(`
                                       'Unauthenticated'
                                    `);
                                },
                                404: () => {
                                    $('#extra-message').append(`
                                       URL not found
                                    `);
                                },
                                500: () => {
                                    $('#extra-message').append(`
                                       'Unknown error'
                                    `);
                                }
                            }
                        });
                    });
                });
            },
            403: () => {
                $('#extra-message').append(`
                   'Unauthenticated'
                `);
            },
            500: (err) => {
                console.log(err);
                $('.url-container').append(`
                    An error has occurred
                `)
            }
        }
    });
}

$(document).ready(function(){

    reloadUrls();

    $('#create-url').click(() => {
        let newUrl = $('#new-url').val();
        $('#extra-message').empty();
        $.ajax('/', {
            beforeSend: function(request) {
                request.setRequestHeader("x-access-token", localStorage.getItem('access_token'));
            },
            type: 'POST',
            data: { url: newUrl },
            statusCode: {
                201: (res) => {
                    $('#new-url').val('');
                    $('#extra-message').empty();
                    reloadUrls();
                },
                400: () => {
                    $('#extra-message').append(`
                       URL format is not correct
                    `);
                },
                403: () => {
                    $('#extra-message').append(`
                       Unauthenticated
                    `);
                },
                500: () => {
                    $('#extra-message').append(`
                       Unknown error
                    `);
                }
            }
        });
    });

    $('#deleteAll').click(() => {
        $.ajax('/', {
            type: 'DELETE',
            beforeSend: function(request) {
                request.setRequestHeader("x-access-token", localStorage.getItem('access_token'));
            },
            statusCode: {
                200: (res) => {
                    reloadUrls();
                },
                404: () => {
                    reloadUrls();
                },
                403: () => {
                    $('#extra-message').append(`
                       'Unauthenticated'
                    `);
                },
                500: () => {
                    $('#extra-message').append(`
                       'Unknown error'
                    `);
                }
            }
        });
        reloadUrls();
    });
});