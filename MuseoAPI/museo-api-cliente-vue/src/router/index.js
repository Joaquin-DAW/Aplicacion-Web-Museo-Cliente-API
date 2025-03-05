import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MuseosView from "../views/MuseosView.vue";
import LoginView from "../views/LoginView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/museos", component: MuseosView, name: "listar_museos" },
  { path: "/login", component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
