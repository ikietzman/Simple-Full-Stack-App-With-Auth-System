<template>
  <div>
    <nav class="navbar loggedout-navbar has-text-centered" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="#">
          <img src="../assets/logo.png" width="112" height="28">
        </a>
      </div>
    </nav>
    <div><h1 class="is-size-3 has-text-centered">Register</h1></div>
    <div @click="this.message = ''" class="pt-6 pb-3">
      <label for="username">Username:</label>
      <input
        class="input level"
        name="username"
        v-model="username"
      />
      <label for="password">Password:</label>
      <input
        class="input level"
        name="password"
        type="password"
        v-model="password"
      />
    </div>
    <div class="pt-3 pb-2">
      <button
        class="button is-dark"
        @click="register"> Register
      </button>
      <button
        class="button is-ghost"
      >
        <router-link to="/login">Login</router-link>
      </button>
    </div>
    <div
      v-if="message"
      class="notification is-info is-light">
        {{ message }}
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import axios from 'axios'

import router from '../router'

export default {
  name: 'RegisterView',
  props: ['user'],
  data() {
    return {
      users: [],
      username: '',
      password: '',
      message: ''
    }
  },
  watch: {
    user() {
      if (this.user > 0) {
        router.push('/account');
      }
    }
  },
  methods: {
    register() {
      if (this.validateLogin()) {
        axios.post('http://127.0.0.1:5000/auth/register', {
          username: this.username,
          password: this.password
        })
          .then((res) => {
            if (res.data.response) {
              // Push registered user to login page
              router.push('/login')
            }
            else {
              // Display error message from server
              this.message = res.data.error;
            }
          })
      }
    },
    validateLogin() {
      // Client-side form validation
      if (this.username.length == 0) {
        this.message = 'Username required'
        return false
      }
      else if (this.password.length == 0) {
        this.message = 'Password required'
        return false
      }
      return true
    }
  }
}
</script>
