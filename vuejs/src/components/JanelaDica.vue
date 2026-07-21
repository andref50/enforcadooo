<script setup>
    import { defineEmits } from 'vue';
    const emit = defineEmits(['fechaJanela'])

    function botaoFechaJanela() {
        emit('fechaJanela')
    }

    const props = defineProps({
        dica: String
    })
</script>

<template>
    <div class="janela dica">
        <button @click="botaoFechaJanela" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title">Dica: 👀</p>
        </div>
        <div class="janela-body-dica">
          <p class="dica-text-body" id="dica-text-body"> {{ dica }} </p>
        </div>
      </div>
</template>