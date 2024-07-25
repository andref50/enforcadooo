<script setup>
</script>

<template>
<!-- TOPO -->
    <div class="topo">
      <div class="grid grid-cols-3 m-2 items-center ">

        <!-- ESQUERDA -->
        <div class="flex justify-start items-center">
          <button @click="$emit('janelaDicaEvent')" class="helpers">!</button>
        </div>

        <!-- TÍTULO -->
        <div class="grid justify-center">
          <h1 class="logo">ENFORCADO</h1>
        </div>

        <!-- DIREITA -->
        <div class="flex-1 fex-row justify-self-end">
          <button @click="$emit('janelaStatsEvent')" class="helpers">III</button>
          <button @click="$emit('janelaAjudaEvent')" class="helpers">?</button>
        </div>
      </div>
    </div>
</template>

