<template>
  <div id="logged-out-header">
    <ul>
      <li><router-link to="/login">Log In</router-link></li>
      <li><router-link to="/signup">Signup</router-link></li>
      <h4 id="title">Nutrition Coach</h4>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'logged-out-header'
  }
</script>
