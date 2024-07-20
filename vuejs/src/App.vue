<script setup>
import { ref, onMounted } from 'vue'

  const server = 'http://127.0.0.1:5000'
  const nome = ref('')

  const shownoshow = ref(false)
  const text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

 function changeStatus(){
  return shownoshow.value = !shownoshow.value;
 }
 
  onMounted(async () => {
    try {
      const response = await fetch(server);
      const data = await response.json();
      nome.value = data.title
      console.log(nome.value);
    } catch(error){
      console.log('Error fetching data')
    }
  });

</script>

<template>
  <div class="container h-screen w-screen flex flex-col border">
    <div class="flex-1 container bg-gray-800 border">
      <div class="m-4 border border-dashed">oie</div>
      <div class="absolute top-5 right-5">
        <button class="bg-indigo-800 px-4 py-2 rounded-full "@click="changeStatus">X</button>
      </div>
      <div class="bg-gray-100 absolute flex m-12 rounded-xl shadow-gray-600 shadow-lg">
        <Transition v-if="shownoshow" >
          <h1 class= "text-gray-800 p-6 px-8"> {{ text }} </h1>
        </Transition>
      </div>
    </div>
    <div class="flex-1 container w-full bg-yellow-600 border">
      <div class="flex flex-row h-full text-2xl items-center border">
        <Transition class="opacity-0 hover:opacity-100 duration-200 ease-in-out">
          <div class="bg-green-800 m-2 border">oi</div>
        </Transition>
        <div class="bg-red-800 m-2">oi</div>
        <Transition class="hover:flex-grow duration-500 ease-in-out">
          <div class="bg-gray-800 m-2 p-2">{{ nome }}</div>
        </Transition>
      </div>
    </div>
  </div>
</template>

