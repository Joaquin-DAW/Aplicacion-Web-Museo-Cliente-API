<template>
  <div id="app">
    <nav class="navbar">
      <ul>
        <li><router-link to="/">Inicio</router-link></li>
        <li><router-link to="/museos">Museos</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
      </ul>
    </nav>

    <router-view />
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
/* Estilos básicos */
nav {
  padding: 10px;
  background: #2c3e50;
  color: white;
}
nav a {
  color: white;
  text-decoration: none;
  margin: 0 10px;
}
</style>
