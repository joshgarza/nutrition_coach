<template>
    <div class='login'>
        <logged-out-header></logged-out-header>
        <h1>Login Form</h1>
        <form id="login" v-on:submit.prevent="loginUser" >
            <input v-model="email" type="text" placeholder="Enter Email" required>
            <input v-model="password" type="password" placeholder="Enter Password" required>
            <button type="submit">Submit</button>
            <button v-on:click="resetPassword">Reset Password</button>
        </form>

    </div>
</template>

<script>
/* eslint-disable */
    import auth from '@/auth.js'
    import LoggedOutHeader from '@/components/LoggedOutHeader'
    export default {
        name: 'login',
        data: function() {
            return {
                email: '',
                password: '',
            }
        },
        components: {
          LoggedOutHeader
        },
        methods: {
            loginUser: function(evt) {
                auth.login(this.email, this.password, (token) => {
                    this.$emit('loginsuccess', token);
                    this.$router.push('dashboard')
                });
            },
            resetPassword: function(evt) {
                // reset password logic
            }
        }
    }
</script>
