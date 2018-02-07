$(function() {

    getJsonFromServer = function(url_path, callback) {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', 'Basic ' + window.btoa(unescape(encodeURIComponent(window.localStorage.getItem("userToken") + ":"))))
            },
            url: url_path,
            // data: JSON.stringify(callback),
            contentType: 'application/json; charset=utf-8',
            type: 'GET',
            success: function(response, status, xhr) {
                console.log(response, status);
                callback(response);
            },
            error: function(xhr, status, error) {
              console.log(status, error);
            }
        });
    }
    
    sendToServer = function(url_path, data, callback) {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', 'Basic ' + window.btoa(unescape(encodeURIComponent(window.localStorage.getItem("userToken") + ":"))))
            },
            url: url_path,
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            type: 'POST',
            success: function(response, status, xhr) {
                console.log(response, status);
                callback(response);
            },
            error: function(xhr, status, error) {
              console.log(status, error);
            }
        });
    }

});

