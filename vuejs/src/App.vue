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

  let palavra = ref('')
  let dica = ''
  let curDay = ref(0)
  let palavraNormalize = ref('')
  let arrPalavra = ref('')
  let acertos = []
  let erros = []
  let num_erros = 0;

  onMounted(async () => {
    try {
      const response = await fetch(server);
      const dados = await response.json();
      palavra = dados['palavra'].toUpperCase();
      dica = dados['dica'];
      curDay = dados['curDay']
      } catch (error) {
      console.log('Error fecthing data.')
      }

    palavraNormalize = normalizeAcento(palavra);
    arrPalavra = normalizeAcento(palavra)

    gameStart();
  });

  // WINDOW MANAGER BOOL
  let isWindowOpen = false; 

  const bodyStates = [svgstate1, svgstate2, svgstate3, svgstate4, svgstate5, svgstate6, svgstate7];

  var totalVitorias = 0;
  var totalDerrotas = 0;

  let gameData = {
        'vitorias'    :0,
        'derrotas'    :0,
        'curDay'      :0,
        'game_status' :'init',
        'last_erros'  :[],
        'last_acertos':[]
      }

  if(localStorage.length){ 
      gameData = JSON.parse(localStorage.getItem('status'))
    }

  getScoreboard();

  // ------- JOGO ------- //
  function mainFunction(kp){
    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));
    const image = document.getElementsByClassName('corda');

    if(palavraNormalize.includes(kp)){
      acertos.push(kp)
      arrSelectdiv.filter(e => normalizeAcento(e.innerHTML) === kp)
                  .map((e, i) => { 
                    setTimeout(() => {
                      e.classList = 'letra-correct'
                    }, 100 * i)
                  })
      if(arrSelectdiv.length - 1 == 0) {
        endGame('winner')
      }
    } else {
      num_erros += 1;
      erros.push(kp)
      arrBancoDiv[0].innerHTML = kp;
      arrBancoDiv[0].classList = 'banco-erro';
      image.item(0).src = bodyStates[num_erros];
      if(num_erros == 6) {
        endGame('gameover')
      }
    }
  }

  function gameStart(){
    updateDica();
    criaJogo();

    if (gameData['game_status'] == 'init'){
      janelaAjuda();
    }

    if(gameData['curDay'] == curDay) {
      disableKeyboard();
      retriveLastGame(gameData['last_acertos'], gameData['last_erros']);
      if(gameData['game_status'] == 'lost'){
        janelaLose();
      } else {
        janelaWin();
      }
    }
  }

  function retriveLastGame(la, le){
    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));
    const image = document.getElementsByClassName('corda');

    
    arrSelectdiv
                .filter(e => la.includes(normalizeAcento(e.innerHTML)))
                .map((e, i) => { 
                  setTimeout(() => {
                    e.classList = 'letra-correct'
                  }, 50 * i)
                })
    arrSelectdiv
                .filter(e => !la.includes(normalizeAcento(e.innerHTML)))
                .map((e, i) => { 
                  setTimeout(() => {
                    e.classList = 'letra-not-guessed'
                  }, 50 * i)
                })

    arrBancoDiv
              .slice(0, le.length)
              .map((e, i) => {
                setTimeout(() => {
                  e.innerHTML = le[i]
                  e.classList = 'banco-erro';       
                }, 50 * i)
              })
    image.item(0).src = bodyStates[le.length];
  }

  function criaJogo() {
    var div = document.getElementsByClassName("letras-div").item(0); 
    for(let c in palavra){
      var p = document.createElement('p1');
      p.classList.add('letra-hidden');
      p.innerText = palavra[c];
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
    let gameResult;
    isWindowOpen = true
    disableKeyboard();

    if(event === 'winner'){
      totalVitorias += 1;
      gameResult = 'win'
    } else {
      totalDerrotas += 1;
      gameResult = 'lost'

    }
    
    updateCookie(totalVitorias, totalDerrotas, gameResult, curDay, acertos, erros);
    setTimeout(() => {
      popupoverlay('60%')
      document.getElementsByClassName(event).item(0).style.opacity = '100%'
      document.getElementsByClassName(event).item(0).style.visibility = "visible";
      document.getElementById('total-win-text').innerHTML = totalVitorias;
      document.getElementById('total-lose-text').innerHTML = totalDerrotas;
    }, 500)
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

  function janelaWin(){
    if(!isWindowOpen) {
      isWindowOpen = true;
      popupoverlay('60%')
      const winWindow = document.getElementsByClassName('winner');
      winWindow.item(0).style.opacity = '100%';
      winWindow.item(0).style.visibility = "visible";
    }
  }

  function janelaLose(){
    if(!isWindowOpen) {
      isWindowOpen = true;
      popupoverlay('60%')
      const loseWindow = document.getElementsByClassName('gameover');
      loseWindow.item(0).style.opacity = '100%';
      loseWindow.item(0).style.visibility = "visible";
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

  function getScoreboard(){
    totalVitorias = gameData['vitorias'];
    totalDerrotas = gameData['derrotas'];
  }

  function updateCookie (vitoria, derrota, result, curDay, last_acertos, last_erros){
      gameData['vitorias']    = vitoria;
      gameData['derrotas']    = derrota;
      gameData['game_status'] = result;
      gameData['curDay']      = curDay;
      gameData['last_acertos'] = last_acertos;
      gameData['last_erros']  = last_erros;
      localStorage.setItem('status', JSON.stringify(gameData))
      console.log(gameData)
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
