<template>
  <div class="base-layout">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Navbar from "@/components/common/Navbar.vue";
</script>

<style scoped>
.base-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f5f8fc;
}

.main-content {
  flex: 1;
  padding: 2rem;
}
</style>
