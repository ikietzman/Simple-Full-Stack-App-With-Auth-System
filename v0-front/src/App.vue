<template>
  <router-view @login="login" :user="user"/>
</template>

<script>

import axios from 'axios'

export default {
  name: 'MainApp',
  data() {
    return {
      // User's id is stored here and passed to components to determine logged in state and retrieve user-specific information
      user: {}
    }
  },
  created() {
    // Check if a user has a current session, response is user id or 0 if not found
    axios.get(`http://127.0.0.1:5000/auth/loggedin`)
      .then((res) => {
        this.user = Number(res.data.loggedIn);
      })
  },
  methods: {
    logout() {
      // This action also triggers the authentication gate on authentication-required app views
      this.user = 0;
    },
    login(id) {
      // id is emitted from LoginView 
      console.log(id);
      this.user = id;
    }
  }
}
</script>
