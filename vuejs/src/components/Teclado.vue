<script setup>

  import { defineEmits } from 'vue';
  const emit = defineEmits(['keyPressed']);

  
  function kbTrigger(t) {
    const kp = t.target.className.split("_")[1];

    if (kp != 'enter')  { t.target.classList = 'keyboard-disabled' } 
    else                { t.target.classList = 'keyboard-enter-disabled'}
    emit("keyPressed", kp);
    // return kp;
  }

</script>

<template>
<!-- TECLADO -->

  <div class="keyboard-div">
    <!-- LINHA 1 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha">
      <button @click="kbTrigger" class="keyboard kb_q"> Q </button>
      <button @click="kbTrigger" class="keyboard kb_w"> W </button>
      <button @click="kbTrigger" class="keyboard kb_e"> E </button>
      <button @click="kbTrigger" class="keyboard kb_r"> R </button>
      <button @click="kbTrigger" class="keyboard kb_t"> T </button>
      <button @click="kbTrigger" class="keyboard kb_y"> Y </button>
      <button @click="kbTrigger" class="keyboard kb_u"> U </button>
      <button @click="kbTrigger" class="keyboard kb_i"> I </button>
      <button @click="kbTrigger" class="keyboard kb_o"> O </button>
      <button @click="kbTrigger" class="keyboard kb_p"> P </button>
    </div>
    <!-- LINHA 2 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha2">
      <button @click="kbTrigger" class="keyboard kb_a"> A </button>
      <button @click="kbTrigger" class="keyboard kb_s"> S </button>
      <button @click="kbTrigger" class="keyboard kb_d"> D </button>
      <button @click="kbTrigger" class="keyboard kb_f"> F </button>
      <button @click="kbTrigger" class="keyboard kb_g"> G </button>
      <button @click="kbTrigger" class="keyboard kb_h"> H </button>
      <button @click="kbTrigger" class="keyboard kb_j"> J </button>
      <button @click="kbTrigger" class="keyboard kb_k"> K </button>
      <button @click="kbTrigger" class="keyboard kb_l"> L </button>
    </div>
    <!-- LINHA 3 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha3">
      <button @click="kbTrigger" class="keyboard kb_z"> Z </button>
      <button @click="kbTrigger" class="keyboard kb_x"> X </button>
      <button @click="kbTrigger" class="keyboard kb_c"> C </button>
      <button @click="kbTrigger" class="keyboard kb_v"> V </button>
      <button @click="kbTrigger" class="keyboard kb_b"> B </button>
      <button @click="kbTrigger" class="keyboard kb_n"> N </button>
      <button @click="kbTrigger" class="keyboard kb_m"> M </button>
      <!-- <button @click="kbTriggerEnter" class="keyboard-enter kb_enter"> ENTER </button> -->
    </div>
  </div>
</template>