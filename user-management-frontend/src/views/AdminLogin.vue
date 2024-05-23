<template>
  <div>
    <h1>Admin Login</h1>
    <form @submit.prevent="checkPassword">
      <input type="password" v-model="password" placeholder="Enter admin password">
      <button type="submit">Confirm</button>
      <button @click="goBack">Revoke</button>
    </form>
    <p v-if="loginError">{{ loginError }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      password: '',
      loginError: ''
    };
  },
  methods: {
    checkPassword() {
      axios.post('/api/admin/login', { password: this.password })
        .then(response => {
          if (response.data.message === "Admin login successful") {
            this.$router.push('/admin');
          } else {
            this.loginError = 'Incorrect password';
          }
        })
        .catch(error => {
          console.error('Login error:', error);
          this.loginError = 'Login failed, please try again.';
        });
      this.password = '';  // Clear the password field after submission
    },
    goBack() {
      this.$router.push('/');
    }
  }
}
</script>
