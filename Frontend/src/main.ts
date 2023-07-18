import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import Login from './components/Login.vue'
import SignUp from './components/SignUp.vue'
import Contacts from './components/Contacts.vue'

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { path: '/', component: Login },
    {path: '/SignUp', component: SignUp},
    {path: '/Contacts', component: Contacts}
]
  

  // 3. Create the router instance and pass the `routes` option
  // You can pass in additional options here, but let's
  // keep it simple for now.
  const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHistory(),
    routes, 
  })

createApp(App).use(router).mount('#app')
