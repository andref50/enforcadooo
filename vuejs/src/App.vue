<script setup>
  import {onMounted, ref} from 'vue'
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
  const API_palavra = ref('')
  const API_dica = ref('')
  let palavra = ref('')
  let dica = ''
  let palavraNormalize = ref('')
  let arrPalavra = ref('')

  onMounted(async () => {
    try {
      const response = await fetch(server);
      const dados = await response.json();
      API_palavra.value = dados['palavra'];
      API_dica.value = dados['dica'];
      } catch (error) {
      console.log('Error fecthing data.')
      }

    palavra = API_palavra.value.toUpperCase();
    dica = API_dica.value;
    palavraNormalize = palavra.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    arrPalavra = normalizeAcento(palavra.toUpperCase())

    gameStart();
    console.log(localStorage.length)
    console.log(localStorage)
  });

  let errors = 0;

  // WINDOW MANAGER BOOL
  let isWindowOpen = false; 

  const bodyStates = [svgstate1, svgstate2, svgstate3, svgstate4, svgstate5, svgstate6, svgstate7];
  let atualState = bodyStates[0];

  var totalVitorias = 0;
  var totalDerrotas = 0;

  let firstPlay = false;

  if(!checkCookie()){ 
      setCookie();
      firstPlay = true;
    }
  getCookie();


  // ------- JOGO ------- //
  function mainFunction(kp){
    kp = kp.toUpperCase();

    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));


    //  ------------ CAPTURA ACERTOS --------------- //
    let captureError = false;
     arrSelectdiv.forEach((element, i) => { 
       if(normalizeAcento(element.innerHTML) === kp) {
            setTimeout(() => {
            element.classList = 'letra-correct';
            captureError = true;
        }, i * 30)
      } // SET TIMER LETTER REVEAL //
    });
    arrPalavra = arrPalavra.replaceAll(kp, '');
    if (!arrPalavra) { 
      // gameWin();
      endGame('winner');
    }


    //  ------------------ CAPTURA ERRO -------------------- //
    if(!palavraNormalize.includes(kp)){
      arrBancoDiv[0].innerHTML = kp;
      arrBancoDiv[0].classList = 'banco-erro';

      errors += 1;

      atualState = bodyStates[errors];
      const image = document.getElementsByClassName('corda');
      image.item(0).src = atualState;

      if(errors == 6) {
        arrSelectdiv.forEach((element, i) => { 
          setTimeout(() => {
            element.classList = 'letra-incorrect' }, i * 100);
          });
          // gameOver();
          endGame('gameover');
      }
    }
  }

  function criaJogo() {
    var div = document.getElementsByClassName("letras-div").item(0); 
    for(let c in palavra){
      var p = document.createElement('p1');
      p.classList.add('letra-hidden');
      p.innerText = palavra[c].toUpperCase();
      if(palavra[c] === " "){
        p.classList.add('opacity-0', 'blank')
      }
      div.appendChild(p);
    }
  }

  function disableKeyboard(){
  const arrButtons= Array.prototype.slice.call(document.getElementsByClassName('keyboard'));
  arrButtons.forEach(element => {
    element.classList = 'keyboard-disabled'
    })
  }

  function endGame(event){
    isWindowOpen = true
    disableKeyboard();

    if(event === 'winner'){
      totalVitorias += 1;
      document.getElementById('total-win-text').innerHTML = totalVitorias;
    } else {
      totalDerrotas += 1;
      document.getElementById('total-lose-text').innerHTML = totalDerrotas;
    }

    updateCookie(totalVitorias, totalDerrotas);
    setTimeout(() => {
      popupoverlay('60%')
      const winnerWindow = document.getElementsByClassName(event);
      winnerWindow.item(0).style.opacity = '100%'
      winnerWindow.item(0).style.visibility = "visible";
    }, 500)
  }


  function janelaDica(){
    updateDica();
    if(!isWindowOpen) {
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
    getCookie();
    if(!isWindowOpen) {
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

  function checkCookie(){
    return localStorage.length
  }

  function getCookie(){
    totalVitorias = parseInt(localStorage.getItem('vitorias'));
    totalDerrotas = parseInt(localStorage.getItem('derrotas'));
  }

  function updateCookie (vitoria, derrota){
      localStorage.setItem('vitorias', vitoria.toString())
      localStorage.setItem('derrotas', derrota.toString())
  }

  function setCookie(){
    localStorage.setItem('vitorias', 0)
    localStorage.setItem('derrotas', 0)
    localStorage.setItem('day', 0)
    
    let data = {
      'vitorias': 0,
      'derrotas': 0,
      '_day': 0,
      'lastState': 'init'
    }
    localStorage.setItem('state', JSON.stringify(data))
  }

  function gameStart(){
    if (firstPlay){
      janelaAjuda();
    }
    criaJogo();
    firstPlay = false;
  }

  function updateDica(){
    document.getElementById('dica-text-body').innerHTML = dica;
  }
</script>

<template>

  <!-- CONTAINER -->
  <div class="container">
    <div class="popup-overlay"></div>

    <!-- TOPO -->
    <Topo @janelaDicaEvent="janelaDica"
          @janelaAjudaEvent="janelaAjuda"
          @janelaStatsEvent="janelaStats"/>

    <!-- PRINCIPAL -->
    <div class="secao-principal">

      <!-- GAME OVER -->
      <div class="janela gameover">
        <button @click="closeWindow" class="close-button btn-gameover"> x </button>
        <div class="janela-title">
          <p class="title">Game over :(</p>
        </div>
        <div class="janela-body">
          <p>Não desanima!</p>
          <p>Amanhã tem mais ;)</p>
        </div>
      </div>

      <!-- WINNER -->
      <div class="janela winner">
        <button @click="closeWindow" class="close-button btn-winner"> x </button>
        <div class="janela-title">
          <p class="title">Parabéns :)</p>
        </div>
        <div class="janela-body">
          <p>Você adivinhou a</p>
          <p>palavra de hoje :)</p>
        </div>
      </div>

      <!-- DICA -->
      <div class="janela dica">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title">Dica: 👀</p>
        </div>
        <div class="janela-body-dica">
          <button class="dica-text-body" id="dica-text-body"> {{ dica }} </button>
        </div>
      </div>

      <!-- ESTATISICAS -->
      <div class="janela stats">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title-stats">Sua evolução</p>
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
        </div>
      </div>

      <!-- AJUDA -->
      <div class="janela ajuda">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p class="title">Como jogar:</p>
        </div>
        <div class="janela-body">
          <p>Enforcad.ooo é o jogo da forca </p>
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
        <img :src="svgstate1" class="corda"/>
      </div>

      <!-- BANCO -->
      <div class="tentativas">
        <div class="flex justify-center items-center">
          <p>Tentativas</p>
        </div>

        <div class="tentativas-box">
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
          <div class="banco"></div>
        </div>
      </div>

        

      <!----------->
      <!--LETRAS -->
      <!----------->
      <div class="letras-div">  </div>

    </div>

      <!-- TECLADO -->
      <Teclado @keyPressed="mainFunction"/>

  </div>
</template>
