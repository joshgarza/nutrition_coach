<template>
    <div class='login'>
        <h1>Login Form</h1>
        <form id="login" v-on:submit.prevent="loginUser" >
            <input v-model="username" type="text" placeholder="Enter Username" required>
            <input v-model="password" type="password" placeholder="Enter Password" required>
            <button type="submit">Submit</button>
        </form>
    </div> 
</template>

<script>
/* eslint-disable */
    import auth from '@/auth.js'
    export default {
        name: 'login',
        data: function() {
            return {
                username: '',
                password: '',
            }
        },
        methods: {
            loginUser: function(evt) {
                auth.login(this.username, this.password, (token) => {
                    this.$emit('loginsuccess', token);
                    this.$router.push('dashboard')
                });
            }
        }
    }
</script>
