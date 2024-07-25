<script setup>
</script>

<template>
<!-- TOPO -->
    <div class="topo">
      <div class="grid grid-cols-3 m-2 items-center ">

        <!-- ESQUERDA -->
        <div class="grid justify-start">
          <button class="helpers">!</button>
        </div>

        <!-- TÍTULO -->
        <div class="grid justify-center">
          <h1 class="titulo">ENFORCADO</h1>
        </div>

        <!-- DIREITA -->
        <div class="flex-1 fex-row justify-self-end">
          <button class="helpers">S</button>
          <button @click="$emit('janelaDicaEvent')" class="helpers">?</button>
        </div>
      </div>
    </div>
</template>

