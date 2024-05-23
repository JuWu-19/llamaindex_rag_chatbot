<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="account_number">Account Number:</label>
        <input id="account_number" v-model="accountNumber" type="text" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input id="password" v-model="password" type="password" required>
      </div>
      <button type="submit">Confirm</button>
      <button @click="goBack">Revoke</button>
      <p v-if="error">{{ error }}</p> <!-- Display error messages here -->
    </form>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = false;
export default {
  data() {
    return {
      accountNumber: '',
      password: '',
      loginError: ''
    };
  },
  methods: {
    login() {
      axios.post('http://127.0.0.1:5000/api/login', {
        account_number: this.accountNumber,
        password: this.password
      }, {
  withCredentials: false // This should be explicitly set to false
})
      .then(response => {
        if (response.data.message === "Logged in successfully") {
          console.log("success login and redirect to user page");
          localStorage.setItem('cur_num', this.accountNumber);
          localStorage.setItem('cur_pass', this.password);
          this.$router.push('/user'); // Redirect on successful login
        } else {
          this.loginError = response.data.error; // Display login error from server
        }
      })
      .catch(error => {
        console.error('Login error:', error);
        this.loginError = 'Failed to login. Please try again.'; // Generic error message
      });
  },
    goBack() {
      this.$router.push('/');
    }
  }
}
</script>
