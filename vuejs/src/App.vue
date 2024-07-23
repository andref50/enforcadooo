<script setup>
  import { ref, onMounted } from 'vue'
  import Topo from './components/Topo.vue';
  import Teclado from './components/Teclado.vue';

  onMounted(async () => {});

  const palavra = "ABACAXI"



</script>

<template>

  <!-- CONTAINER -->
  <div class="container h-screen w-screen flex flex-col">

    <!-- TOPO -->
    <Topo />


    <!-- PRINCIPAL -->
    <div class="flex flex-1 flex-col justify-center">
      
  
      <!-- FORCA -->
      <div class="flex flex-1 flex-col">

        <!-- BONECO -->
        <div class="flex flex-1 justify-center">
        </div>

        <!-- LETRAS -->
        <div class="flex flex-col mb-5">
        <p class="ml-16">Tentativas</p>

        <div class="tentativas-box ">
          <div class="banco-erro"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
        </div>
        </div>
      </div>
        

        <!-- LETRAS -->
        <div class="flex justify-center items-end mb-5">
          <div class="letras-div">
            <p class="texto-input">   A </p>
            <p class="texto-input">   A </p>
            <p class="texto-correct"> A </p>
            <p class="texto-input">   A </p>
            <p class="texto-input">   A </p>
            <p class="texto-correct"> A </p>
            <p class="texto-input">   A </p>
            <p class="texto-input">   A </p>
            <p class="texto-correct"> A </p>
            <p class="texto-input">   A </p>
            <p class="texto-input">   A </p>
            <p class="texto-input">   A </p>
            <p class="texto-correct"> A </p>
          </div>
      </div>

    </div>


    <!-- TECLADO -->
    <div class="flex justify-center">
      <Teclado />
    </div>

  </div>
</template>
