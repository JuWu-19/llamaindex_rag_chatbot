<template>
    <div>
      <h1>Registration</h1>
      <form @submit.prevent="register">
        <div>
          <label for="username">User Name:</label>
          <input id="username" v-model="username" type="text" required>
        </div>
        <div>
          <label for="account_number">Account Number:</label>
          <input id="account_number" v-model="accountNumber" type="text" required>
        </div>
        <div>
          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" required>
        </div>
        <div>
          <label for="repeat_password">Repeat Password:</label>
          <input id="repeat_password" v-model="repeatPassword" type="password" required>
        </div>
        <button type="submit">Confirm</button>
        <button @click="goBack">Revoke</button>
        <p v-if="error">{{ error }}</p>
      </form>
    </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        accountNumber: '',
        password: '',
        repeatPassword: '',
        error: ''
      };
    },
    methods: {
      register() {
        if (this.password !== this.repeatPassword) {
          this.error = 'Passwords not identical';
          return;
        }
        axios.post('/api/register', {
          username: this.username,
          account_number: this.accountNumber,
          password: this.password,
          repeat_password: this.repeatPassword
        })
        .then(() => {
          localStorage.setItem('cur_num', this.accountNumber);
          localStorage.setItem('cur_pass', this.password);
          this.$router.push('/user'); // Redirect on successful login
        })
        .catch(error => {
          if (error.response && error.response.data.error) {
            this.error = error.response.data.error;
          } else {
            this.error = 'An unexpected error occurred.';
          }
        });
      },
      goBack() {
        this.$router.push('/');
      }
    }
  }
</script>
  