<template>
    <div class='confirm'>
        <logged-out-header></logged-out-header>
        <h1>Please check your email for your confirmation link.</h1>
        <button>Resend confirmation email</button>
    </div>
</template>

<script>
/* eslint-disable */
    import LoggedOutHeader from '@/components/LoggedOutHeader'
    export default {
        name: 'confirm',
        props: ['email'],
        data: function() {
        	return {}
        },
        components: {
          LoggedOutHeader
        },
    }
</script>