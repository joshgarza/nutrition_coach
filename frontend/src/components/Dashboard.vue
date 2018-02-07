<template>
    <div class="dashboard">
        <goals v-bind:goals="goals" v-bind:token="token"></goals>
        <goals-form v-on:updategoals='fetchGoals' v-bind:token="token"></goals-form>
        <macros v-bind:token="token"></macros>
    </div>
</template>

<script>
    import Goals from '@/components/Goals'
    import Macros from '@/components/Macros'
    import GoalsForm from '@/components/GoalsForm'
    import axios from 'axios'
    export default {
      props: ['token'],
      data () {
        return {
          goals: {}
        }
      },
      components: {
        GoalsForm,
        Goals,
        Macros
      },
      created: function () {
        this.fetchGoals()
      },
      methods: {
        fetchGoals: function () {
          axios({
            headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent(this.token) + ':'))
            },
            url: 'http://localhost:8081/goals',
            type: 'GET'
          }).then((response) => {
            this.goals = response.data
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      watch: {
        '$route': 'fetchGoals'
      }
    }
</script>