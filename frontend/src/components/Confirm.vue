<template>
    <div class='confirm'>
        <logged-out-header></logged-out-header>
        <h1>Please check your email for your confirmation link.</h1>
        <button v-on:click="sendEmail">Resend confirmation email</button>
    </div>
</template>

<script>
/* eslint-disable */
    import LoggedOutHeader from '@/components/LoggedOutHeader'
    import axios from 'axios'
    export default {
        name: 'confirm',
        props: ['email'],
        data: function() {
        	return {}
        },
        methods: {
        	sendEmail: function() {
        		axios({
        		  url: 'http://localhost:8081/user-activation',
        		  data: {'email': this.email},
        		  method: 'POST'
        		}).then((response) => {
        		  console.log(response)
        		  alert("Your email has been sent.")
        		}).catch((error) => {
        		  console.log(error)
        		})
        	}
        },
        components: {
          LoggedOutHeader
        },
    }
</script>