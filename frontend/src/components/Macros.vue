<template>
    <div class='macros'>
        <h3>Nutrition Info</h3>
        <table>
            <tr>
                <th>Date</th>
                <th>Calories</th>
                <th>Protein</th>
                <th>Carbs</th>
                <th>Fat</th>
            </tr>
            <tr v-for="macro in macros">
                <td>{{ macro.date }}</td>
                <td>{{ macro.calories }}</td>
                <td>{{ macro.protein }}</td>
                <td>{{ macro.carbs }}</td>
                <td>{{ macro.fat }}</td>
            </tr>
        </table>
    </div> 
</template>

<script>
    import axios from 'axios'
    export default {
      props: ['token'],
      data: function () {
        return {
          macros: {}
        }
      },
      created: function () {
        this.fetchMacros()
      },
      methods: {
        fetchMacros: function () {
          axios({
            headers: {'Authorization': 'Basic ' + window.btoa(unescape(encodeURIComponent(this.token) + ':'))
            },
            url: 'http://localhost:8081/macros',
            type: 'GET'
          }).then((response) => {
            this.macros = response.data
            console.log(this.macros)
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      watch: {
        '$route': 'fetchmacros'
      }
    }
    </script>