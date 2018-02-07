/* eslint-disable */
import axios from 'axios'

export default {
    
    login (username, password, callback) {
        axios({
            headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent( username + ":" + password))),
            },
            url:"http://localhost:8081/token",
            type: 'GET'
        }).then(function(response) {
             callback(response.data.token);
        }).catch(function(error) {
            console.log(error);
        });
    },
    
    createUser (username, password, callback) {
        axios({
          method: 'post',
          url: 'http://localhost:8081/users',
          data: {'username': username, 'password': password},
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          type: 'POST'
        }).then(function(response) {
            console.log(response);
            axios({
                headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent( username + ":" + password))),
                },
                url:"http://localhost:8081/token",
                type: 'GET'
            }).then(function(response) {
                 callback(response.data.token);
            }).catch(function(error) {
                console.log(error);
            });
        }).catch(function(error){
            console.log(error);
        });
        
    }
}