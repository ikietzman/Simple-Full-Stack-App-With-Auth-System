<template>
  <div>
    <NavigationComponent :user='user'/>
    <div>
      <h1>Find Courses</h1>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavigationComponent from '@/components/Navigation.vue'

// import axios from 'axios'
import router from '../router'

export default {
  name: 'FindCourses',
  data() {
    return {
      users: []
    }
  },
  props: ['user'],
  components: {
    NavigationComponent
  },
  watch: {
    user() {
      if (this.user == 0) {
        router.push('/login');
      }
    }
  },
  methods: {
    logout() {
      this.$emit('logout');
    }
  }
}
</script>
