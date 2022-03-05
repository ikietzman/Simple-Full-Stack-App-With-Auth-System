<template>
  <!-- <nav>
    <router-link to="/my-courses">My Courses</router-link> |
    <router-link to="/find-courses">Find Courses</router-link> |
    <router-link to="/account">Account</router-link> |
    <a href="#" @click="logout">Logout</a>

  </nav> -->
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="#">
        <img src="../assets/logo.png" width="112" height="28">
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu is-active">
      <div class="navbar-start">
        <router-link class="navbar-item" to="/find-courses">
          Find Courses
        </router-link>
        <router-link class="navbar-item" to="/my-courses">
          My Courses
        </router-link>
        <router-link class="navbar-item" to="/account">
          Account
        </router-link>
      </div>

      <div class="navbar-end">
            <a @click="logout" class="navbar-item is-ghost">
              Log out
            </a>
      </div>
    </div>
  </nav>
</template>

<script>

import axios from 'axios'

import router from '../router'

export default {
  name: 'NavigationComponent',
  props: ['user'],
  methods: {
    logout() {
      axios.get(`http://127.0.0.1:5000/auth/logout/${this.user}`)
        .then(() => {
          this.$emit('logout');
          router.go();
        })
    }
  }
}
</script>
