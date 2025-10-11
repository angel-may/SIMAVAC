<template>
  <Navbar v-if="isAuth" />
  <router-view />
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from './stores/user'
import Navbar from './components/common/Navbar.vue'

const store = useUserStore()
const isAuth = computed(() => store.isAuth)
</script>
