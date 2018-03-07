<template>
    <div class='activate'>
        <logged-out-header></logged-out-header>
        <h4>{{ expired }}</h4>
    </div>
</template>

<script>
/* eslint-disable */
    import LoggedOutHeader from '@/components/LoggedOutHeader'
    import auth from '@/auth.js'
    export default {
        name: 'activate',
        props: ['activationtoken'],
        data: function() {
        	return {
                expired: ''
            }
        },
        created: function() {
            this.activateUser()
        },
        methods: {
        	activateUser: function() {
                auth.activateUser(
                    this.activationtoken, 
                    (response) => { this.$router.replace( '/login' ) },
                    (error) => { this.expired = 'Your activation url is invalid.' }
                );
            },

        },
        components: {
          LoggedOutHeader
        },
    }
</script>