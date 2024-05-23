<template>
  <div>
    <h1>Welcome to the User Management System</h1>
    <button @click="goToAdminLogin">Admin</button>
    <button @click="goToLogin">User Login</button>
    <button @click="goToRegister">User Registration</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToAdminLogin() {
      this.$router.push('/admin-login');
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    }
  }
}
</script>

