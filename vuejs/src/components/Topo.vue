<script setup>
</script>

<template>
<!-- TOPO -->
    <div class="topo">
      <!-- <div class="grid grid-cols-3 m-2 mt-0 items-center "> -->
      <div class="topo-subdiv">

        <!-- ESQUERDA -->
        <div class="flex justify-start items-center item1">
          <button @click="$emit('janelaDicaEvent')" class="helpers">!</button>
        </div>

        <!-- TÍTULO -->
        <div class="flex justify-center item2">
          <h1 class="logo">ENFORCADO</h1>
        </div>

        <!-- DIREITA -->
        <div class="flex-1 fex-row justify-self-end content-center item3">
          <button @click="$emit('janelaStatsEvent')" class="helpers">III</button>
          <button @click="$emit('janelaAjudaEvent')" class="helpers">?</button>
        </div>
      </div>
    </div>
</template>

