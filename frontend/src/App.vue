<template>
  <div id="app">
    <ul>
      <li><router-link to="/login">Log In</router-link></li>
      <li><router-link to="/signup">Signup</router-link></li>
      <li id="dashboard"><router-link to="/dashboard">Dashboard</router-link></li>
      <h4 id="title">Nutrition Coach</h4>
    </ul>
    <router-view v-on:loginsuccess='storeToken' v-bind:token="token"/>
  </div>
</template>

<script>
export default {
  name: 'app',
  data: function () {
    return {
      'token': ''
    }
  },
  created: function () {
    this.token = localStorage.getItem('userToken')
    if (this.token) {
      this.$router.push('dashboard')
    }
  },
  methods: {
    storeToken: function (token) {
      this.token = token
      localStorage.setItem('userToken', token)
    }
  },
  watch: {
    token: function () { console.log(this.token) }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: -8px;

}
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

li {
    float: right;
    border-left: 1px solid #bbb;
}

#title{
  float: left;
  color: white;
  vertical-align: middle;
  padding: 0;
  margin: 10px;
  position: relative;
  top: 5px;
  /*left: 50%;*/
  /*transform: translate(-50%, -50%);*/
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

/* Change the link color to #111 (black) on hover */
li a:hover {
    background-color: #111;
}
</style>
