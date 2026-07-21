<script setup>
  import { onMounted, ref, computed, useTemplateRef } from 'vue'

  import Topo from './components/Topo.vue';
  import Teclado from './components/Teclado.vue';
  import svgstate1 from './assets/svg/svg-state-1.svg'
  import svgstate2 from './assets/svg/svg-state-2.svg'
  import svgstate3 from './assets/svg/svg-state-3.svg'
  import svgstate4 from './assets/svg/svg-state-4.svg'
  import svgstate5 from './assets/svg/svg-state-5.svg'
  import svgstate6 from './assets/svg/svg-state-6.svg'
  import svgstate7 from './assets/svg/svg-state-7.svg'
  import JanelaAjuda from './components/JanelaAjuda.vue';
  import JanelaDica from './components/JanelaDica.vue';
  import JanelaStats from './components/JanelaStats.vue';
  import BoxWin from './components/BoxWin.vue';
  import BoxGameover from './components/BoxGameover.vue';

  function normalizeAcento(a) { return a.normalize('NFD').replace(/[\u0300-\u036f]/g, "") };

  const server = import.meta.env.VITE_APP_API 

  let palavra = ref('')
  let palavraNormalize = ref('') 
  let letrasRestantes = ref('')
  let palavraEncrypt = ref('')
  let dicaEncrypt = ref('')
  let dica = ref('')
  let curDay = ref(0)
  let num_erros = ref(0);
  
  const palpitesCertos = ref([])
  const palpitesErrados = ref([null, null, null, null, null, null])
 
  const palpitesTotal = computed(() => {
    return [...palpitesCertos.value, ...palpitesErrados.value]
  })

  const arrayLetrasNaoAdivinhadas = useTemplateRef('letrasNaoAdivinhadas');

  const letras = computed(() => {
      return Array.from(palavraNormalize.value)
    })
    
  const textoDica = computed(() => {
    if (num_erros.value < 2) {
      return (2 - num_erros.value > 1) ? `Faltam ${2 - num_erros.value} erros para desbloquear.` : `Falta ${2 - num_erros.value} erro para desbloquear.`;
    }
    return dica.value
  })

  onMounted(async () => {
    try {
      const response = await fetch(server);
      const dados = await response.json();

      palavraEncrypt.value = dados['palavra_encrypt']
      dicaEncrypt.value = dados['dica'];
      curDay = dados['curDay']

      let k = 'NPxMG4yxGjb6999v'
      k = CryptoJS.enc.Utf8.parse(k)
    
      let palavraDecrypt = CryptoJS.AES.decrypt(palavraEncrypt.value, k, {mode:CryptoJS.mode.ECB})
      palavra.value = palavraDecrypt.toString(CryptoJS.enc.Utf8).toUpperCase();
      let dicaDecrypt = CryptoJS.AES.decrypt(dicaEncrypt.value, k, {mode:CryptoJS.mode.ECB})
      dica.value = dicaDecrypt.toString(CryptoJS.enc.Utf8)

      palavraNormalize.value = normalizeAcento(palavra.value);

      } catch (error) {
      console.log('Error fecthing data: ' + error)
    }
    
    // Wait for DOM to update before accessing refs
    await new Promise(resolve => setTimeout(resolve, 0));

    initGame();
  });

  // janelas
  let showJanelaAjuda = ref(false)
  let showJanelaDica = ref(false)
  let showJanelaStats = ref(false)
  let showBoxWin = ref(false)
  let showBoxGameover = ref(false)

  const bodyStates = [svgstate1, svgstate2, svgstate3, svgstate4, svgstate5, svgstate6, svgstate7];

  let totalVitorias = 0;
  let totalDerrotas = 0;

  let gameData = {
        'vitorias'        :0,
        'derrotas'        :0,
        'curDay'          :0,
        'status'          :'init',
        'palpitesCertos'  :[],
        'palpitesErrados' :[],
        'num_erros'       :0,
      }

  let gameStatusPOSTRequest = {'status': ''}

  if(localStorage.length){ 
      gameData = JSON.parse(localStorage.getItem('status'))
    }

  reloadScoreboard();

  // ------- JOGO ------- //
  function keyPressed(key){
    if(palavraNormalize.value.includes(key)){
      if(!palpitesCertos.value.includes(key)){
        palpitesCertos.value.push(key)
      }
    } 
    else {
      if(!palpitesErrados.value.includes(key)){
        palpitesErrados.value[num_erros.value] = key;
      }
      num_erros.value += 1;
    }

    gameData.status = 'playing'
    gameData.curDay = curDay
    gameData.palpitesCertos = palpitesCertos.value
    gameData.palpitesErrados = palpitesErrados.value
    gameData.num_erros = num_erros.value
    localStorage.setItem('status', JSON.stringify(gameData))

    checkWinCondition()
  }

  const checkWinCondition = () => {
    letrasRestantes.value = normalizeAcento(palavra.value).split('').filter(letra => !palpitesCertos.value.includes(letra)).join('');

    if(letrasRestantes.value.length === 0) {
      endGame('winner')
      mostraJanelaFimJogo('winner')
    }
    else if(num_erros.value == 6) {
      endGame('lost')
      mostraJanelaFimJogo('lost')
      revelaLetrasNaoAdivinhadas()
    }
  }

  function revelaLetrasNaoAdivinhadas(){
    arrayLetrasNaoAdivinhadas.value.map((e, i) => { 
      setTimeout(() => {
        e.innerHTML = palavra.value.charAt(e.id)
        e.classList.replace('letra-hidden', 'letra-incorrect')
      }, 100 * i)
    })
  }

  function initGame(){
    if (gameData.status == 'init'){
    }

    else if(curDay > gameData.curDay){
      gameData.palpitesCertos = []
      gameData.palpitesErrados = []
      gameData.num_erros = 0
      localStorage.setItem('status', JSON.stringify(gameData))
    }

    else if(gameData.status == 'playing'){ 
      palpitesCertos.value = gameData.palpitesCertos
      palpitesErrados.value = gameData.palpitesErrados
      num_erros.value = gameData.num_erros
      checkWinCondition()
    }
    
    else if(gameData.status == 'winner' || gameData.status == 'lost' && gameData.curDay == curDay){
      palpitesCertos.value = gameData.palpitesCertos
      palpitesErrados.value = gameData.palpitesErrados
      num_erros.value = gameData.num_erros
      mostraJanelaFimJogo(gameData.status)
      revelaLetrasNaoAdivinhadas()
    }
  }

  async function endGame(event){
    if(event === 'winner'){
      totalVitorias += 1;
      gameData.status = 'winner';
    } else {
      totalDerrotas += 1;
      gameData.status = 'lost';
    }

    gameData.vitorias = totalVitorias;
    gameData.derrotas = totalDerrotas;
    gameStatusPOSTRequest.status = gameData.status
    localStorage.setItem('status', JSON.stringify(gameData))
 
    try {
      const response = await fetch(server, 
                                  {method: 'POST',
                                  headers: {
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/json'
                                          },
                                  body: JSON.stringify(gameStatusPOSTRequest)});
      const statusCheck = await response.json();
      }
      catch(error){
        console.log(error)
      }
    }

  function mostraJanelaFimJogo(event){
    disableKeyboard();
    setTimeout(() => {
      if (event == 'winner') showBoxWin.value = true
      else showBoxGameover.value = true
    }, 500)

    setTimeout(() => {
      showJanelaStats.value = true;
    }, 550)
  }

  function disableKeyboard(){
    const arrButtons= Array.prototype.slice.call(document.getElementsByClassName('keyboard'));
    arrButtons.forEach(element => {
      element.classList = 'keyboard-disabled'
      })
    }

  function reloadScoreboard(){
    totalVitorias = gameData.vitorias;
    totalDerrotas = gameData.derrotas;
  }

</script>

<template>

  <!-- CONTAINER -->
  <div class="container">
    
    <!-- TOPO -->
    <Topo @janelaDicaEvent="showJanelaDica = true; showJanelaAjuda =showJanelaStats = false;"
          @janelaAjudaEvent="showJanelaAjuda = true; showJanelaStats = showJanelaDica = false"
          @janelaStatsEvent="showJanelaStats = true; showJanelaDica = showJanelaAjuda = false" />

    <!-- PRINCIPAL -->
    <div class="secao-principal">
      
      <div class="popup-overlay" 
        v-if="showJanelaAjuda || showJanelaDica || showJanelaStats"
        @click="showJanelaDica = showJanelaAjuda = showJanelaStats = false">
      </div>

      <BoxWin v-if="showBoxWin"/>
      <BoxGameover v-if="showBoxGameover"/>
      
      <JanelaAjuda v-if="showJanelaAjuda" 
                  @fechaJanela="showJanelaAjuda=false"/>

      <JanelaStats v-if="showJanelaStats"
                  @fechaJanela="showJanelaStats=false"
                  :vitorias="totalVitorias"
                  :derrotas="totalDerrotas"
                  :num_erros="num_erros"
                  :status="gameData.status"/>


      <JanelaDica v-if="showJanelaDica" 
                  @fechaJanela="showJanelaDica=false" 
                  :dica="textoDica"/>      

      <!-- BONECO -->
      <div class="corda-container">
        <img :src="bodyStates[num_erros]" class="corda"/>
      </div>

      <!-- BANCO -->
      <div class="tentativas">
        <div class="flex justify-center items-center">
          <p>Tentativas</p>
        </div>

        <div class="tentativas-box">
          <div v-for="(item, index) in palpitesErrados" 
          :key="index"
          v-text="palpitesErrados[index] == null ? '' : palpitesErrados[index]" 
          :class="palpitesErrados[index] == null ? 'banco' : 'banco-erro'" 
          ref="banco"></div>
        </div>
      </div>

      <!--LETRAS -->
      <div class="letras-div">
        <p v-for="(item, index) in letras" 
          :key="index" 
          :id="index"
          v-text="palpitesCertos.includes(item) ? palavra[index] : ''"
          :class="palpitesCertos.includes(item) ? 'letra-correct' : 'letra-hidden'"
          :ref="palpitesCertos.includes(item) ? '' : 'letrasNaoAdivinhadas'">
        </p>  
      </div>

      <!-- TECLADO -->
      <div class="teclado-componente">
        <Teclado @keyPressed="keyPressed" :items="palpitesTotal"/>
      </div>

    </div> <!--SECAO PRINCIPAL--> 
  </div>
</template>
