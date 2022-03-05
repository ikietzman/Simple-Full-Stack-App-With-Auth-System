<template>
  <div>
    <NavigationComponent :user='user'/>
    <div>
      <h1 class="is-size-3 has-text-centered">Account</h1>
    </div>
    <div @click="this.message = ''" class="pt-4 pb-2">
      <h2 class="is-size-4 has-text-centered">My Info</h2>
      <label for="username">Username:</label>
      <input
        class="input level"
        name="username"
        disabled
        v-model="userInfo.username"
      />
      <label for="dob">Date of Birth:</label>
      <input
        class=" input level"
        name="dob"
        v-model="userInfo.dob"
      />
      <label for="street">Street Address:</label>
      <input
        class="input level"
        name="street"
        v-model="userInfo.street"
      />
      <label for="zip">Zip Code:</label>
      <input
        class="input level"
        name="zip"
        v-model="userInfo.zip"
      />
      <div class="level">
        <button
          class="button is-dark level-item"
          @click="save"> Save
        </button>
      </div>

    </div>
    <div
      v-if="message"
      class="notification is-info is-light">
        {{ message }}
    </div>
    <div @click="this.messagePassword = ''" class="pt-4 pb-2">
      <h2 class="is-size-4 has-text-centered">Change Password</h2>
      <label for="password">Password:</label>
      <input
        class="input level"
        name="password"
        type="password"
        v-model="passwords.current"
      />
      <label for="confirm">Confirm:</label>
      <input
        class="input level"
        name="confirm"
        type="password"
        v-model="passwords.currentConfirm"
      />
      <label for="new">New Password:</label>
      <input
        class="input level"
        name="new"
        type="password"
        v-model="passwords.new"
      />
    </div>
    <div>
      <div class="level">
        <button
          class="button is-dark level-item"
          @click="savePassword"> Save
        </button>
      </div>
    </div>
    <div
      v-if="messagePassword"
      class="notification is-info is-light">
        {{ messagePassword }}
  </div>
  </div>
</template>

<script>
// @ is an alias to /src

import axios from 'axios'

import NavigationComponent from '@/components/Navigation.vue'

import router from '../router'

export default {
  name: 'AccountView',
  data() {
    return {
      userInfo: {
        username: '',
        dob: '',
        street: '',
        zip: ''
      },
      passwords: {
        current: '',
        currentConfirm: '',
        new: '',
      },
      message: '',
      messagePassword: ''
    }
  },
  props: ['user'],
  components: {
    NavigationComponent
  },
  watch: {
    user() {
      if (this.user > 0) {
        // Retrieve user data
        axios.get(`http://127.0.0.1:5000/auth/getuser/${this.user}`)
          .then((res) => {
            this.userInfo = res.data[0];
          })
      }
      if (this.user == 0) {
        // Auth gate
        router.push('/login');
      }
    },
    messagePassword() {
      if (this.messagePassword == 'Password saved') {
        this.passwords = {
          current: '',
          currentConfirm: '',
          new: '',
        }
      }
    }
  },
  methods: {
    logout() {
      this.$emit('logout');
    },
    save() {
      axios.post(`http://127.0.0.1:5000/auth/update`, {
        dob: this.userInfo.dob,
        street: this.userInfo.street,
        zip: this.userInfo.zip,
        id: this.user
      })
        .then((res) => {
          this.message = res.data
        })
    },
    savePassword() {
      if (this.validatePasswords()) {
        axios.post(`http://127.0.0.1:5000/auth/updatepassword`, {
          current: this.passwords.current,
          confirm: this.passwords.currentConfirm,
          new: this.passwords.new,
          id: this.user
        })
          .then((res) => {
            this.messagePassword = res.data
          })
      }
    },
    validatePasswords() {
      // Client-side form validation
      if (this.passwords.current == 0) {
        this.messagePassword = 'Current password required';
        return false;
      }
      else if (this.passwords.current != this.passwords.currentConfirm) {
        this.messagePassword = 'Passwords do not match';
        return false;
      }
      return true;
    }
  },
  created() {
    // Retrieve user info if user exists
    if (typeof this.user == 'number') {
      axios.get(`http://127.0.0.1:5000/auth/getuser/${this.user}`)
        .then((res) => {
          this.userInfo = res.data[0];
        })
    }

  }
}
</script>
