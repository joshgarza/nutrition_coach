/* eslint-disable */
import axios from 'axios'

export default {
    
    login (email, password, callback) {
        axios({
            headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent( email + ":" + password))),
            },
            url:"http://localhost:8081/token",
            type: 'GET'
        }).then(function(response) {
             callback(response.data.token);
        }).catch(function(error) {
            console.log(error);
        });
    },
    
    createUser (email, password, callback) {
        axios({
          method: 'post',
          url: 'http://localhost:8081/users',
          data: {'email': email, 'password': password},
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          type: 'POST'
        }).then(function(response) {
            console.log(response)
            callback(response)
        }).catch(function(error){
            console.log(error);
        });
        
    },

    activateUser (token, callback, error_callback) {
        axios({
          type: 'GET',
          url: 'http://localhost:8081/user-activation/' + token,
        }).then(function(response) {
            console.log(response)
            callback(response)
        }).catch(function(error){
            console.log(error)
            error_callback(error);
        });
    }
}