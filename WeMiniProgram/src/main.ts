import { createSSRApp } from "vue";
import App from "./App.vue";
import uviewPlus from 'uview-plus';
import * as Pinia from 'pinia';
// import { setupRouteGuard } from "./utils/routeGuard";


export function createApp() {
  const app = createSSRApp(App);
  app.use(Pinia.createPinia());
  app.use(uviewPlus)
  return {
    app,
    Pinia,
  };
}

// setupRouteGuard();

