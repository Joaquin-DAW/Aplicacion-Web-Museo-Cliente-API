<template>
    <div>
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="iniciarSesion">
        <input v-model="username" placeholder="Usuario" required />
        <input v-model="password" type="password" placeholder="Contraseña" required />
        <button type="submit">Ingresar</button>
      </form>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import { loginUser } from "@/services/api.js";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        error: null
      };
    },
    methods: {
      async iniciarSesion() {
        try {
          const credentials = {
            grant_type: "password",
            username: this.username,
            password: this.password,
            client_id: "mi_aplicacion",
            client_secret: "mi_clave_secreta"
          };
  
          const data = await loginUser(credentials);
          sessionStorage.setItem("token", data.access_token);
          alert("¡Inicio de sesión exitoso!");
        } catch (error) {
          this.error = "Error al iniciar sesión. Verifica tus credenciales.";
        }
      }
    }
  };
  </script>  