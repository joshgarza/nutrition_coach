<template>
    <div class='generator'>
        <form id="generator_button" v-on:submit.prevent="generateMacros" >
            <button  type="submit">Generate Macros</button>
        </form>
        
    </div>
</template>

<script>
  import axios from 'axios'
  export default {
    props: ['token', 'goals'],
    methods: {
      generateMacros: function () {
        axios({
          headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent(this.token) + ':'))
          },
          url: 'http://localhost:8081/generator',
          data: {'protein': this.protein, 'carbs': this.carbs, 'fat': this.fat},
          method: 'POST'
        }).then((response) => {
          console.log(response)
          this.$emit('generateMacros')
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    watch: {
      '$route': 'fetchGoals'
    },
  }
</script>
