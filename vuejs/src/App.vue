<script setup>
  import {onMounted, ref, computed, useTemplateRef} from 'vue'
  import Topo from './components/Topo.vue';
  import Teclado from './components/Teclado.vue';
  import svgstate1 from './assets/svg/svg-state-1.svg'
  import svgstate2 from './assets/svg/svg-state-2.svg'
  import svgstate3 from './assets/svg/svg-state-3.svg'
  import svgstate4 from './assets/svg/svg-state-4.svg'
  import svgstate5 from './assets/svg/svg-state-5.svg'
  import svgstate6 from './assets/svg/svg-state-6.svg'
  import svgstate7 from './assets/svg/svg-state-7.svg'

  // ------------------------------- HELPERS & CONSTANTES ------------------------------ //                          
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
    // palavraEncrypt.value = flaskData.palavra_encrypt;
    // dicaEncrypt.value = flaskData.dica;
    // curDay = flaskData.curDay

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

    console.log('Palavra: ', palavra.value)
    console.log('Dica: ', dica.value)
    
    // Wait for DOM to update before accessing refs
    await new Promise(resolve => setTimeout(resolve, 0));

    initStatus();
  });

  // WINDOW MANAGER BOOL
  let isWindowOpen = false; 

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

  getScoreboard();

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
      showJanelaEndGame('winner')
    }
    else if(num_erros.value == 6) {
      endGame('lost')
      showJanelaEndGame('lost')
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

  function initStatus(){
    if (gameData.status == 'init'){
      janelaAjuda()
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
      showJanelaEndGame(gameData.status)
      revelaLetrasNaoAdivinhadas()
    }
  }

  async function endGame(event){
    if(event === 'winner'){
      totalVitorias += 1;
      gameData.status = 'winner';
      // gameStatusPOSTRequest.status = 'winner'
    } else {
      totalDerrotas += 1;
      gameData.status = 'lost';
      // gameStatusPOSTRequest.status = 'lost'
    }

    gameData.vitorias = totalVitorias;
    gameData.derrotas = totalDerrotas;
    // gameData.curDay = curDay;
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
  

  function showJanelaEndGame(event){
    disableKeyboard();
    setTimeout(() => {
      document.getElementsByClassName(event).item(0).style.opacity = '100%'
      document.getElementsByClassName(event).item(0).style.visibility = "visible";
      document.getElementById('total-win-text').innerHTML = totalVitorias;
      document.getElementById('total-lose-text').innerHTML = totalDerrotas;
    }, 500)

    let cdDiv = document.querySelector('.countdown-div')
    let cdRoot = document.querySelector('#countdown')
    let cdTitle = document.createElement('p')
    cdTitle.classList.add('countdown-title')
    cdTitle.innerText = 'PRÓXIMA PALAVRA:'
    cdDiv.appendChild(cdTitle)

    let countdown = document.createElement('p')
    countdown.classList.add('countdown')
    cdDiv.appendChild(countdown)
    cdRoot.style.display = "flex"
    cdRoot.style.flex = "1"
    cdRoot.style.flexDirection = 'column '
    

    // Set the date we're counting down to
    var countDownDate = new Date("Jan 5, 2030 23:59:59").getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

      // Get today's date and time
      var now = new Date().getTime();

      // Find the distance between now and the count down date
      var distance = countDownDate - now;

      // Time calculations for days, hours, minutes and seconds
      // var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      countdown.innerHTML = hours + "h " + ( minutes < 10 ? "0" + minutes : minutes) + "m " + ( seconds < 10 ? "0" + seconds : seconds) + "s ";

      if (distance < 0) {
        clearInterval(x);
        countdown.innerHTML = "EXPIRED";
      }
    }, 1000);


    setTimeout(() => {
      janelaStats();
    }, 550)
  }

  function disableKeyboard(){
    const arrButtons= Array.prototype.slice.call(document.getElementsByClassName('keyboard'));
    arrButtons.forEach(element => {
      element.classList = 'keyboard-disabled'
      })
    }

  function janelaDica(){
    if (!isWindowOpen) {
      isWindowOpen = true;
      popupoverlay('60%')
      const dicaWindow = document.getElementsByClassName('dica');
      dicaWindow.item(0).style.opacity = '100%';
      dicaWindow.item(0).style.visibility = "visible";
    }
  }

  function janelaAjuda(){
    if(!isWindowOpen) {
      isWindowOpen = true;
      popupoverlay('60%');
      const ajudawindow = document.getElementsByClassName('ajuda');
      ajudawindow.item(0).style.opacity = '100%';
      ajudawindow.item(0).style.visibility = "visible";
    }
  }

  function janelaStats(){
    getScoreboard();
    if (!isWindowOpen) {
      isWindowOpen = true;
      popupoverlay('60%')
      const statsWindow = document.getElementsByClassName('stats');
      statsWindow.item(0).style.opacity = '100%';
      statsWindow.item(0).style.visibility = "visible";
      }
    }

  function closeWindow(e){
    e.target.parentNode.style.opacity = "0%";
    e.target.parentNode.style.visibility = "hidden";
    popupoverlay('0%');
    isWindowOpen = false;
  }

  function popupoverlay(po){
    const popup_overlay = document.getElementsByClassName('popup-overlay');
    popup_overlay.item(0).style.opacity = po;
  }

  function getScoreboard(){
    totalVitorias = gameData.vitorias;
    totalDerrotas = gameData.derrotas;
  }

  async function comparilhe(){
    const shareResultText = {
      0: '🔥Joguei Enforcado e acertei de primeira! \n🟩🟩🟩🟩🟩🟩 \nTente em enforcado.app',
      1: '🔥Joguei Enforcado e acertei na segunda! \n🟥🟩🟩🟩🟩🟩 \nTente em enforcado.app',
      2: '🔥Joguei Enforcado e acertei na terceira! \n🟥🟥🟩🟩🟩🟩 \nTente em enforcado.app',
      3: '🔥Joguei Enforcado e até que fui bem! \n🟥🟥🟥🟩🟩🟩 \nTente em enforcado.app',
      4: '🔥Quase! Acertei Enforcado na penúltima! 🔥 \n🟥🟥🟥🟥🟩🟩 \nTente em enforcado.app',
      5: '🔥Quase! Acertei Enforcado na última! \n🟥🟥🟥🟥🟥🟩 \nTente em enforcado.app',
      6: '😔Joguei Enforcado, mas não foi dessa vez :/ \n🟥🟥🟥🟥🟥🟥\nTente em enforcado.app'
    }
    
    await navigator.share({text: shareResultText[num_erros.value]})
  }

</script>

<template>

  <!-- CONTAINER -->
  <div class="container">
    
    <!-- TOPO -->
    <Topo @janelaDicaEvent="janelaDica"
          @janelaAjudaEvent="janelaAjuda"
          @janelaStatsEvent="janelaStats"/>

    <!-- PRINCIPAL -->
    <div class="secao-principal">

      <div class="popup-overlay"></div>

      <!-- GAME OVER -->
      <div class="janela lost">
        <div class="janela-title">
          <p class="title title-winner-lose">Game over :(</p>
        </div>
      </div>

      <!-- WINNER -->
      <div class="janela winner">
        <div class="janela-title">
          <p class="title title-winner-lose">Parabéns :)</p>
        </div>
      </div>

      <!-- ESTATISICAS -->
      <div class="janela stats">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title-stats">Sua evolução:</p>
          <br>
        </div>
        <div class="janela-body">
          <div class="flex flex-row flex-1 justify-center">
            <div class="flex flex-col items-center px-8">
              <button class="placar" id="total-win-text"> {{ totalVitorias }} </button>
              <p class="placar-label">VITÓRIAS</p>
            </div>
            <div class="flex flex-col items-center px-8">
              <button class="placar" id="total-lose-text"> {{ totalDerrotas }} </button>
              <p class="placar-label">DERROTAS</p>
              <br>
            </div>
          </div>
          <div id="countdown">
            <div class="countdown-div">
            </div>
            <div class="compartilhe">
              <button @click="comparilhe">➥ Compartilhe</button>
            </div>
          </div>
        </div>
    
      </div>

      <!-- DICA -->
      <div class="janela dica">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title">Dica: 👀</p>
        </div>
        <div class="janela-body-dica">
          <p class="dica-text-body" id="dica-text-body"> {{ textoDica }} </p>
        </div>
      </div>


      <!-- AJUDA -->
      <div class="janela ajuda">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title">Como jogar:</p>
        </div>
        <div class="janela-body">
          <p>Enforcado é o jogo da forca </p>
          <p>que você já conhece de cara nova :)</p>
          <br>
          <p>Tente adivinhar a palavra secreta 
            clicando nas letras, mas cuidado: 
            cada erro te deixa mais próximo 
            de um trágico fim. </p>
          <br>
          <div class="flex flex-col">
            <div class="flex flex-row items-center">
              <button class="helpers">!</button>
              <p class="ajuda-buttons-label">dica</p>
            </div>
            <div class="flex flex-row items-center">
              <button class="helpers">ılıı</button>
              <p class="ajuda-buttons-label">placar</p>
            </div>
            <div class="flex flex-row items-center">
              <button class="helpers">?</button>
              <p class="ajuda-buttons-label">ajuda </p>
            </div>
          </div>
        </div>
      </div>
      

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

    </div> <!--SECAO PRINCIPAL--> </div>
</template>
