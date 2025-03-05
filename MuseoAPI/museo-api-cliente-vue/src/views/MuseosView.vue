<template>
  <div>
    <h1 class="mb-4">Lista de Museos</h1>
    <ul v-if="museos.length > 0" class="list-group">
      <li v-for="museo in museos" :key="museo.id">
        {{ museo.nombre }} - {{ museo.ubicacion }}
      </li>
    </ul>
    <p v-else class="text-center">No hay museos disponibles en este momento.</p>
  </div>
</template>

<script>
import { getMuseos } from "../services/api";

export default {
  data() {
    return {
      museos: []
    };
  },
  async mounted() {
    try {
      this.museos = await getMuseos();
    } catch (error) {
      console.error("Error al cargar los museos:", error);
    }
  }
};
</script>