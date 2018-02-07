<template>
    <div class='goals_form'>
        <h2>Update Goals</h2>
        <form id="goals_form" v-on:submit.prevent="updateGoals" >
            <input v-model="protein" type="text" placeholder="Enter Protein" required>
            <input v-model="carbs" type="text" placeholder="Enter Carbs" required>
            <input v-model="fat" type="text" placeholder="Enter Fat" required>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>

<script>
  import axios from 'axios'
  export default {
    props: ['token'],
    data: function () {
      return {
        protein: '',
        carbs: '',
        fat: ''
      }
    },
    methods: {
      updateGoals: function () {
        axios({
          headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent(this.token) + ':'))
          },
          url: 'http://localhost:8081/goals',
          data: {'protein': this.protein, 'carbs': this.carbs, 'fat': this.fat},
          method: 'POST'
        }).then((response) => {
          console.log(response)
          this.$emit('updategoals')
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    watch: {
      '$route': 'updateGoals'
    }
  }
</script>
