<template>
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">
          <router-link :to="{ name: 'listar_museos' }">
            {{ museo.nombre }}
          </router-link>
        </h5>
        <h6 class="card-subtitle mb-2 text-muted">Ubicación: {{ museo.ubicacion }}</h6>
        <p class="card-text">Fecha de Fundación: {{ museo.fecha_fundacion }}</p>
        <p class="card-text">{{ museo.descripcion }}</p>
        
        <div>
          <p class="card-text">Exposiciones:</p>
          <ul>
            <li v-for="exposicion in museo.exposiciones" :key="exposicion.id">
              {{ exposicion.titulo }}
            </li>
          </ul>
        </div>
  
        <div class="row btn-group">
          <div class="mb-2">
            <router-link :to="{ name: 'museo_editar', params: { id: museo.id } }" class="btn btn-outline-primary">
              ✏️ Editar
            </router-link>
          </div>
          <div>
            <router-link :to="{ name: 'museo_editar_nombre', params: { id: museo.id } }" class="btn btn-outline-primary">
              ✏️ Editar Nombre
            </router-link>
          </div>
          <div class="mb-2">
            <button class="btn btn-danger" @click="confirmarEliminar(museo.id)">
              🗑️ Eliminar
            </button>
          </div>
        </div>
  
        <!-- Modal de Confirmación -->
        <div v-if="mostrarConfirmacion" class="modal fade show" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Confirmar eliminación</h5>
                <button type="button" class="btn-close" @click="cerrarModal"></button>
              </div>
              <div class="modal-body">
                ¿Estás seguro de que deseas eliminar este museo: {{ museo.nombre }}?
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
                <button class="btn btn-danger" @click="eliminarMuseo">Eliminar</button>
              </div>
            </div>
          </div>
        </div>
  
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      museo: Object
    },
    data() {
      return {
        mostrarConfirmacion: false
      };
    },
    methods: {
      confirmarEliminar() {
        this.mostrarConfirmacion = true;
      },
      cerrarModal() {
        this.mostrarConfirmacion = false;
      },
      eliminarMuseo() {
        // Aquí harías una petición DELETE a la API
        console.log(`Eliminando museo ID: ${this.museo.id}`);
        this.cerrarModal();
      }
    }
  };
  </script>
  
  <style scoped>
  .card {
    border: 1px solid #ddd;
    padding: 10px;
  }
  </style>
  