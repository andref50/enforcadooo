<script setup>

  const imgURL = 'https://i.redd.it/za2kypsi7qq51.jpg'

</script>

<template>
  <div class="container h-screen w-screen mx-auto flex flex-col items-center justify-center border">

    <div class="flex flex-col bg-gray-700 shadow-lg shadow-gray-00  py-6 px-6 rounded-xl">
      <div class="flex flex-row items-center">
        <img class="w-24 rounded-full" :src=imgURL />
        <div class="ml-4">
          <h3 class="font-semibold text-xl">Andre</h3>
          <h4 class="text-indigo-300 pt-1">Editor de video</h4>
        </div>
      </div>
      <div class="mt-6">
        <h2 class="font-semibold text-2xl mb-2">Bio</h2>
        <p class="text-gray-300 font-regular mt-1 max-w-xs text-justify">Olaaaa, como vai você? A gente pode pensar juntos em coisas legais?</p>
      </div>
      <div class="mt-6"></div>
        <h2 class="font-semibold text-2xl mb-1">Carreira</h2>
        <div class="mt-1">
          <h3 class="text-yellow-500 font-medium text-xl">Suno</h3>
          <ul class="list-disc list-inside font-regular pl-4">
            <li class="list-item">Oieee</li>
            <li class="list-item">Alo</li>
            <li class="list-item">Como vai voie meu caro?</li>
          </ul>
      </div>
    </div>
  </div>
</template>

