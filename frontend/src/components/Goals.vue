<template>
    <div class='goals'>
        <h2>Goals</h2>
        <table>
            <tr>
                <th>Date</th>
                <th>Calories</th>
                <th>Protein</th>
                <th>Carbs</th>
                <th>Fat</th>
            </tr>
           
            <tr v-for="goal in goals">
                <td>{{ goal.date }}</td>
                <td>{{ goal.calories }}</td>
                <td>{{ goal.protein }}</td>
                <td>{{ goal.carbs }}</td>
                <td>{{ goal.fat }}</td>
            </tr>
        </table>
    </div> 
</template>

<script>
  // import axios from 'axios'
  export default {
    props: ['token', 'goals'],
    watch: {
      '$route': 'fetchGoals'
    }
  }
</script>