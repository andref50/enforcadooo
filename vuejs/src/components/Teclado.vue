<script setup>

  import { defineEmits } from 'vue';
  const emit = defineEmits(['keyPressed']);

  function kbTrigger(t) {
    const kp = t.target.innerHTML.toUpperCase();
    emit("keyPressed", kp);
  }
const props = defineProps({
    items: {
      type: Array,
      default: () => []
    }
  });
</script>

<template>
<!-- TECLADO -->

  <div class="keyboard-div">
    <!-- LINHA 1 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha">
      <!-- <button @click="kbTrigger" class="keyboard kb_q"> Q </button> -->
      <button @click="kbTrigger" :class="props.items.includes('Q') ? 'keyboard-disabled' : 'keyboard'">Q</button>
      <button @click="kbTrigger" :class="props.items.includes('W') ? 'keyboard-disabled' : 'keyboard'">W</button>
      <button @click="kbTrigger" :class="props.items.includes('E') ? 'keyboard-disabled' : 'keyboard'">E</button>
      <button @click="kbTrigger" :class="props.items.includes('R') ? 'keyboard-disabled' : 'keyboard'">R</button>
      <button @click="kbTrigger" :class="props.items.includes('T') ? 'keyboard-disabled' : 'keyboard'">T</button>
      <button @click="kbTrigger" :class="props.items.includes('Y') ? 'keyboard-disabled' : 'keyboard'">Y</button>
      <button @click="kbTrigger" :class="props.items.includes('U') ? 'keyboard-disabled' : 'keyboard'">U</button>
      <button @click="kbTrigger" :class="props.items.includes('I') ? 'keyboard-disabled' : 'keyboard'">I</button>
      <button @click="kbTrigger" :class="props.items.includes('O') ? 'keyboard-disabled' : 'keyboard'">O</button>
      <button @click="kbTrigger" :class="props.items.includes('P') ? 'keyboard-disabled' : 'keyboard'">P</button>
    </div>
    <!-- LINHA 2 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha2">
      <button @click="kbTrigger" :class="props.items.includes('A') ? 'keyboard-disabled' : 'keyboard'">A</button>
      <button @click="kbTrigger" :class="props.items.includes('S') ? 'keyboard-disabled' : 'keyboard'">S</button>
      <button @click="kbTrigger" :class="props.items.includes('D') ? 'keyboard-disabled' : 'keyboard'">D</button>
      <button @click="kbTrigger" :class="props.items.includes('F') ? 'keyboard-disabled' : 'keyboard'">F</button>
      <button @click="kbTrigger" :class="props.items.includes('G') ? 'keyboard-disabled' : 'keyboard'">G</button>
      <button @click="kbTrigger" :class="props.items.includes('H') ? 'keyboard-disabled' : 'keyboard'">H</button>
      <button @click="kbTrigger" :class="props.items.includes('J') ? 'keyboard-disabled' : 'keyboard'">J</button>
      <button @click="kbTrigger" :class="props.items.includes('K') ? 'keyboard-disabled' : 'keyboard'">K</button>
      <button @click="kbTrigger" :class="props.items.includes('L') ? 'keyboard-disabled' : 'keyboard'">L</button>
    </div>
    <!-- LINHA 3 -->
    <!-- <div class="grid grid-cols-10"> -->
    <div class="kb_linha3">
      <button @click="kbTrigger" :class="props.items.includes('Z') ? 'keyboard-disabled' : 'keyboard'">Z</button>
      <button @click="kbTrigger" :class="props.items.includes('X') ? 'keyboard-disabled' : 'keyboard'">X</button>
      <button @click="kbTrigger" :class="props.items.includes('C') ? 'keyboard-disabled' : 'keyboard'">C</button>
      <button @click="kbTrigger" :class="props.items.includes('V') ? 'keyboard-disabled' : 'keyboard'">V</button>
      <button @click="kbTrigger" :class="props.items.includes('B') ? 'keyboard-disabled' : 'keyboard'">B</button>
      <button @click="kbTrigger" :class="props.items.includes('N') ? 'keyboard-disabled' : 'keyboard'">N</button>
      <button @click="kbTrigger" :class="props.items.includes('M') ? 'keyboard-disabled' : 'keyboard'">M</button>
    </div>
  </div>
</template>
