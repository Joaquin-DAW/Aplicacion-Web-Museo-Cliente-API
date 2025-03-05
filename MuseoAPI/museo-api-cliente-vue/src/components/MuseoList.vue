<template>
    <div>
      <h2>Lista de Museos</h2>
      <button @click="cargarMuseos">Cargar Museos</button>
      <ul v-if="museos.length">
        <li v-for="museo in museos" :key="museo.id">{{ museo.nombre }}</li>
      </ul>
      <p v-else>No hay museos disponibles.</p>
    </div>
  </template>
  
  <script>
  import { getMuseos } from "@/services/api.js";
  
  export default {
    data() {
      return {
        museos: []
      };
    },
    methods: {
      async cargarMuseos() {
        try {
          const token = sessionStorage.getItem("token"); // Obtener el token del usuario
          if (!token) {
            alert("No hay token. Inicia sesión primero.");
            return;
          }
          this.museos = await getMuseos(token);
        } catch (error) {
          console.error("Error al obtener museos:", error);
        }
      }
    }
  };
  </script>  