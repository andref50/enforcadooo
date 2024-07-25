<script setup>
  import { ref, onMounted, cloneVNode } from 'vue'
  import Topo from './components/Topo.vue';
  import Teclado from './components/Teclado.vue';

  // onMounted(async () => {});
  onMounted(gameStart);

  function normalizeAcento(a) { return a.normalize('NFD').replace(/[\u0300-\u036f]/g, "") };

  const palavra = "CALENDÁRIO".toUpperCase();
  let arrPalavra = normalizeAcento(palavra.toUpperCase())
  let errors = 0;

  function mainFunction(kp){

    kp = kp.toUpperCase();

    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));


    // CAPTURA ACERTOS
    let captureError = false;
     arrSelectdiv.forEach((element, i) => { 
       if(normalizeAcento(element.innerHTML) === kp) {
            setTimeout(() => {
            element.classList = 'letra-correct';
            captureError = true;

        }, i * 30)} // SET TIMER LETTER REVEAL
      });

      arrPalavra = arrPalavra.replaceAll(kp, '');
      if (!arrPalavra) { gameWin() }

    // CAPTURA ERROS
    if(!palavra.includes(kp) && kp != 'ENTER'){
      arrBancoDiv[0].innerHTML = kp;
      arrBancoDiv[0].classList = 'banco-erro';

      errors += 1;

      if(errors == 6) {
        gameOver() ;
        arrSelectdiv.forEach(element => { element.classList = 'letra-correct' });
      }
    }
  }

  function criaLetras() {
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
    const enterDisable = Array.prototype.slice.call(document.getElementsByClassName('keyboard-enter'))
    enterDisable[0].classList = 'keyboard-enter-disabled';
  }

function gameOver() {
  disableKeyboard();
  const gameoverWindow = document.getElementsByClassName('gameover');
  gameoverWindow.item(0).style.opacity = '100'
  }

function gameWin(){
  disableKeyboard();
  const winnerWindow = document.getElementsByClassName('winner');
  winnerWindow.item(0).style.opacity = '100'
}

function janelaDica(){
  const winnerWindow = document.getElementsByClassName('dica');
  winnerWindow.item(0).style.opacity = '100'
  
}

function closeWindow(e){
  e.target.parentNode.style.opacity = "0"
}

function gameStart(){
  document.cookie = 'vitorias=0; derrotas=0';
  var allCookies = document.cookie;
  console.log(document.cookie)
  console.log(allCookies)
  criaLetras();
}
</script>

<template>

  <!-- CONTAINER -->
  <div class="container h-screen w-screen flex flex-col">

    <!-- TOPO -->
    <Topo @janelaDicaEvent="janelaDica"/>

    <!-- PRINCIPAL -->
    <div class="flex flex-1 flex-col justify-center items-center">

      <!-- GAME OVER -->
      <div class="janela gameover">
        <button @click="closeWindow" class="close-button"> x </button>
        <!-- <div class="decorationBar"></div> -->
        <div class="janela-title">
          <p>Game over :(</p>
        </div>
        <div class="janela-subtitle">
          <p>Mas não desanima!</p>
          <p>Tem uma palavra nova todo dia ;)</p>
        </div>
      </div>

      <!-- WINNER -->
      <div class="janela winner">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p>Acertou :)</p>
        </div>
        <div class="janela-subtitle">
          <p>Amanhã tem</p>
          <p>um novo desafio :)</p>
        </div>
      </div>

      <!-- WINNER -->
      <div class="janela dica">
        <button @click="closeWindow" class="close-button"> x </button>
        <div class="janela-title">
          <p>Dica: 👀</p>
        </div>
        <div class="janela-subtitle">
          <p>A Thais Mara</p>
          <p>gosta muito de fazer :)</p>
        </div>
      </div>
      
      <!-- FORCA -->
      <div class="flex flex-1 flex-col">

        <!-- BONECO -->
        <div class="flex flex-1 mb-4 justify-center">
          <button>PALAVRA</button>
        </div>

        <!-- BANCO -->
        <div class="flex flex-col mb-0">
          <div class="flex justify-center">
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
