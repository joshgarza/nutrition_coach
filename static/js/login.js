$(function() {


	$("#login-form").submit(function(e){
	    e.preventDefault();
      login_info = {'username': $("input[name=username]").val(), 'password': $("input[name=password]").val()};
      $.ajax({
        url:"/users",
        data: JSON.stringify(login_info),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        type: 'POST',
        success: function(response, status) {
          getUserToken(login_info);
        },
        error: function(xhr, status, error) {
          console.log(status, error);
        }
      });
    });

    function getUserToken(login_info) {
      $.ajax({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('Authorization', 'Basic ' + window.btoa(unescape(encodeURIComponent( login_info.username + ":" + login_info.password))))
        },
        url:"/token",
        type: 'GET',
        success: function(tokendata) {
            window.localStorage.setItem('userToken', tokendata.token);
            console.log("Received user token!");
            window.location.href = "/static/html/user.html";
        },
        error: function(xhr, status, error) {
          console.log(status, error);
        }
      });

    }

});

