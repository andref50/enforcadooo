<script setup>
  import {onMounted} from 'vue'
  import Topo from './components/Topo.vue';
  import Teclado from './components/Teclado.vue';


  // ------------------------------- HELPERS & CONSTANTES ------------------------------ //                          
  function normalizeAcento(a) { return a.normalize('NFD').replace(/[\u0300-\u036f]/g, "") };

  const palavra = "ARAPUÃ".toUpperCase();
  let arrPalavra = normalizeAcento(palavra.toUpperCase())
  let errors = 0;

  let totalVitorias = 0;
  let totalDerrotas = 0;

  // WINDOW MANAGER BOOL
  let isWindowOpen = false; 

  let popup_overlay = document.getElementsByClassName('popup-overlay');

    onMounted(gameStart);
    /* 
    onMounted(async () => {}); */

  // ------- JOGO ------- //
  function mainFunction(kp){

    kp = kp.toUpperCase();

    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));


    //  CAPTURA ACERTOS //
    let captureError = false;
     arrSelectdiv.forEach((element, i) => { 
       if(normalizeAcento(element.innerHTML) === kp) {
            setTimeout(() => {
            element.classList = 'letra-correct';
            captureError = true;
        
        }, i * 30)} // SET TIMER LETTER REVEAL //
      });

      arrPalavra = arrPalavra.replaceAll(kp, '');
      if (!arrPalavra) { gameWin() }


    //  CAPTURA ERROS //
    if(!palavra.includes(kp) && kp != 'ENTER'){
      arrBancoDiv[0].innerHTML = kp;
      arrBancoDiv[0].classList = 'banco-erro';
      errors += 1;
      if(errors == 6) {
        arrSelectdiv.forEach((element, i) => { 
          setTimeout(() => {
            element.classList = 'letra-correct' }, i * 100);
          });
          gameOver();
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

  function gameWin(){
    disableKeyboard();
    popupoverlay('60%')
    const winnerWindow = document.getElementsByClassName('winner');
    winnerWindow.item(0).style.opacity = '100%'
    winnerWindow.item(0).style.visibility = "visible";
    totalVitorias += 1;
    updateCookie(totalVitorias, totalDerrotas);
  }

  function gameOver() {
    disableKeyboard();
    popupoverlay('60%')
    const gameoverWindow = document.getElementsByClassName('gameover');
    gameoverWindow.item(0).style.opacity = '100%';
    gameoverWindow.item(0).style.visibility = "visible";
    totalDerrotas += 1;
    updateCookie(totalVitorias, totalDerrotas);
    }

  function janelaDica(){
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
    popup_overlay.item(0).style.opacity = po;
  }

  function setCookie(){
    document.cookie = 'vitorias=0';
    document.cookie = 'derrotas=0';
  }

  function getCookie(){
    const readCookie = document.cookie;
    let eachElement = readCookie.split(';').map((e) => e.trim());

    const element1 = Number(eachElement[0].split('=')[1])
    const element2 = Number(eachElement[1].split('=')[1])

    if(eachElement[0].includes('vitorias')){
      totalVitorias = element1;
      totalDerrotas = element2;
    } else {
      totalVitorias = element2;
      totalDerrotas = element1;
    }
    console.log(totalVitorias);
    console.log(totalDerrotas);
  }

  function updateCookie (vitoria, derrota){
    document.cookie = 'vitorias=' + vitoria
    document.cookie = 'derrotas=' + derrota
    console.log(document.cookie)

  }

  function gameStart(){
    if(document.cookie.indexOf('vitorias') == -1 ){ setCookie() }
    else { getCookie() }
    console.log(document.cookie)
    criaJogo();
  }
</script>

<template>

  <!-- CONTAINER -->
  <div class="container h-screen w-screen flex flex-col">
    <div class="popup-overlay"></div>

    <!-- TOPO -->
    <Topo @janelaDicaEvent="janelaDica"
          @janelaAjudaEvent="janelaAjuda"
          @janelaStatsEvent="janelaStats"/>

    <!-- PRINCIPAL -->
    <div class="flex flex-1 flex-col justify-center items-center">

      <!-- GAME OVER -->
      <div class="janela gameover">
        <button @click="closeWindow" class="close-button btn-gameover"> x </button>
        <!-- <div class="decorationBar"></div> -->
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
        <div class="janela-body">
          <p>A Thais Mara</p>
          <p>gosta muito de fazer :)</p>
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
              <button class="placar"> {{ totalVitorias }} </button>
              <p>VITÓRIAS</p>
            </div>
            <div class="flex flex-col items-center px-8">
              <button class="placar"> {{ totalDerrotas }} </button>
              <p>DERROTAS</p>
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
          <p>Tente adivinhar a palavra secreta</p>
          <p>clicando nas letras, mas cuidado:</p>
          <p>cada erro te deixa mais próximo</p>
          <p>de um trágico fim. </p>
          <br>
        </div>
      </div>
      
      <!-- FORCA -->
      <div class="flex flex-1 flex-col">

        <!-- BONECO -->
        <div class="flex flex-1 mb-4 justify-center">

        </div>

        <!-- BANCO -->
        <div class="">
          <div class="flex justify-center items-center">
            <div class="line"></div>
            <div class="p-line"> <p>Tentativas</p> </div>
            <div class="line"></div>
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
      </div>
        

      <!----------->
      <!--LETRAS -->
      <!----------->
      <div class="letras-div">  </div>


    </div>

      <!-- TECLADO -->
      <div class="flex justify-center">
        <Teclado @keyPressed="mainFunction"/>
      </div>

  </div>
</template>
