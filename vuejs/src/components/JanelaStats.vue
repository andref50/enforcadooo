<script setup>
    import { defineEmits, ref , computed} from 'vue';

    const emit = defineEmits(['fechaJanela'])

    function botaoFechaJanela(){
        emit('fechaJanela')
    }

    const props = defineProps({
        vitorias: Number,
        derrotas: Number,
        num_erros: Number,
        status: String
    })

    const isGameOver = computed(() => {
        return props.status == 'winner' || props.status == 'lost'
    })
    
    async function comparilhe(){
        const shareResultText = {
        0: '🔥 De primeira! \n🟩🟩🟩🟩🟩🟩 \nTente em enforcado.app',
        1: '🔥 Na segunda! \n🟥🟩🟩🟩🟩🟩 \nTente em enforcado.app',
        2: '🔥 Boooa! \n🟥🟥🟩🟩🟩🟩 \nTente em enforcado.app',
        3: '🔥 Boa! \n🟥🟥🟥🟩🟩🟩 \nTente em enforcado.app',
        4: '🔥 Boa! 🔥 \n🟥🟥🟥🟥🟩🟩 \nTente em enforcado.app',
        5: '🔥 Na trave! \n🟥🟥🟥🟥🟥🟩 \nTente em enforcado.app',
        6: '😔 Não foi dessa vez :/ \n🟥🟥🟥🟥🟥🟥\nTente em enforcado.app'
        }
        await navigator.share({text: shareResultText[props.num_erros]})
    }

    let countdown = ref('')

    // Set the date we're counting down to
    let countDownDate = new Date("Jan 5, 2030 23:59:59").getTime();

    // Update the count down every 1 second
    let x = setInterval(() =>  {

      // Get today's date and time
      let now = new Date().getTime();

      // Find the distance between now and the count down date
      let distance = countDownDate - now;

      // Time calculations for days, hours, minutes and seconds
      // let days = Math.floor(distance / (1000 * 60 * 60 * 24));
      let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      let seconds = Math.floor((distance % (1000 * 60)) / 1000);

      countdown.value = hours + "h " + ( minutes < 10 ? "0" + minutes : minutes) + "m " + ( seconds < 10 ? "0" + seconds : seconds) + "s ";

      if (distance < 0) {
        clearInterval(x);
        countdown.innerHTML = "EXPIRED";
      }
    }, 100);

</script>

<template>
    <div class="janela stats" :class="{gameover: isGameOver}">
        <button @click="botaoFechaJanela" class="close-button"> x </button>
        <div class="janela-title">
            <p class="title-stats">Sua evolução</p>
        </div>
        <div class="janela-body">
            <div class="flex flex-row flex-1 justify-center">
                <div class="flex flex-col items-center px-8">
                    <p class="placar-label">VITÓRIAS</p>
                    <button class="placar" id="total-win-text"> {{ vitorias }} </button>
                </div>
                <div class="flex flex-col items-center px-8">
                    <p class="placar-label">DERROTAS</p>
                    <button class="placar" id="total-lose-text"> {{ derrotas }} </button>
                    <br>
                </div>
            </div>
            <div v-if="isGameOver" id="countdown">
                <div class="countdown-div">
                    <p class="countdown-title">PRÓXIMA PALAVRA</p>
                    <p class="countdown">{{  countdown }}</p>
                    <br>
                </div>
                <div class="compartilhe">
                    <button @click="comparilhe">➥ Compartilhe</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .gameover {
        margin-top: 80px;
    }

</style>