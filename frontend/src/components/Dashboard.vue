<template>
    <div class="dashboard">
        <ul>
          <h4 id="title">Nutrition Coach</h4>
          <li><a v-on:click='logout'>Log Out</a></li>
        </ul>
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
        if (this.token === '') {
          alert('You need to log in first!')
          this.$router.push('login')
        } else {
          this.fetchGoals()
        }
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
        },
        logout: function () {
          this.$emit('logout')
        }
      },
      watch: {
        '$route': 'fetchGoals'
      }
    }
</script>
