<template>
  <div>
    <nav class="navbar loggedout-navbar has-text-centered" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="#">
          <img src="../assets/logo.png" width="112" height="28">
        </a>
      </div>
    </nav>
    <div><h1 class="is-size-3 has-text-centered">Login</h1></div>
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
        @click="login"> Login
      </button>
      <button
        class="button is-ghost"
      >
          <router-link to="/register">Register</router-link>
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

// Enable sending cookies with axios requests
axios.defaults.withCredentials = true;

export default {
  name: 'LoginView',
  props: ['user'],
  data() {
    return {
      username: '',
      password: '',
      loggedin: false,
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
    login() {
      if (this.validateLogin()) {
        axios.post('http://127.0.0.1:5000/auth/login', {
          username: this.username,
          password: this.password
        })
          .then((res) => {
            this.message = res.data.response;
            // Build cookies for id and session token
            let d = new Date();
              d.setTime(d.getTime() + 1 * 24 * 60 * 60 * 1000);
            let expires = "expires=" + d.toUTCString();
            document.cookie =
              "Token=" + res.data.token + ";" + expires + ";path=/";
            document.cookie = "Id=" + res.data.id + ";" + expires + ";path=/";
            return res;
          })
          .then((res) => {
            if (res.data.id) {
              // Emit login event with user id to update user on main Vue instance (App.vue)
              this.$emit('login', res.data.id);
              router.push('/account');
            }
          })
      }

    },
    validateLogin() {
      // Client-side form validation
      if (this.username.length == 0) {
        this.message = 'Username required';
        return false;
      }
      else if (this.password.length == 0) {
        this.message = 'Password required';
        return false;
      }
      return true;
    }
  }
}
</script>
