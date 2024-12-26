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
  let palavra_decrypt = ref('')
  let palavraNormalize = ref('')
  let palavraArr = ref('')
  let cr = ref('')
  let dica = ''
  let curDay = ref(0)
  let acertos = []
  let erros = []
  let num_erros = 0;


  onMounted(async () => {
    try {
      const response = await fetch(server);
      const dados = await response.json();
      palavra = dados['palavra'].toUpperCase();
      cr = dados['palavra_encrypt']
      dica = dados['dica'];
      curDay = dados['curDay']

      let k = 'NPxMG4yxGjb6999v'
      k = CryptoJS.enc.Utf8.parse(k)
      let decrypted =  CryptoJS.AES.decrypt(cr, k, {mode:CryptoJS.mode.ECB});
      palavra_decrypt = decrypted.toString(CryptoJS.enc.Utf8).toUpperCase()

      // console.log(cr)
      // console.log('Decrypted: ' + decrypted.toString(CryptoJS.enc.Utf8))
      // console.log('Decrypted normalized: ' + normalizeAcento(decrypted.toString(CryptoJS.enc.Utf8)))
      console.log('Palavra_dectrypt: ', palavra_decrypt)

      palavraArr = palavraNormalize = normalizeAcento(palavra);
      // console.log(palavraArr, palavraNormalize, curDay)

      } catch (error) {
      console.log('Error fecthing data: ' + error)
      }
    
    updateDica();
    criaJogo();
    initStatus();
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

  let finalGamePOSTRequest = { 'status': '' }

  if(localStorage.length){ 
      gameData = JSON.parse(localStorage.getItem('status'))
    }

  getScoreboard();

  // ------- JOGO ------- //
  function keyPressed(kp){
    let arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    let arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));
    let image = document.getElementsByClassName('corda')


    if(palavraNormalize.includes(kp)){
      palavraArr = palavraArr.replaceAll(kp, '')
      acertos.push(kp)

    let temp = []

      for (let i = 0; i <= palavraNormalize.length; i++){
        if (palavraNormalize[i] === kp){
          for (let j = 0; j < arrSelectdiv.length; j++){
            if (arrSelectdiv[j].innerHTML == i){
              temp.push(arrSelectdiv[j])
              arrSelectdiv[j].innerHTML = palavra[i]
            }
          }
        }
      }
    temp.map((e, i) => { 
                    setTimeout(() => {
                      e.classList = 'letra-correct'
                    }, 100 * i)
                  })
    } else {
      erros.push(kp)
      num_erros += 1;
      arrBancoDiv[0].innerHTML = kp;
      arrBancoDiv[0].classList = 'banco-erro';
      image.item(0).src = bodyStates[num_erros];
    }

    // CHECK IF WIN
    if(palavraArr.length === 0) {

        endGame('winner')
        showJanelaEndGame('winner')
      }

    // CHECK IF LOSE
    if(num_erros == 6) {
      endGame('gameover')
      showJanelaEndGame('gameover')
      arrSelectdiv.map((e, i) => { 
                    setTimeout(() => {
                      e.innerHTML = palavraNormalize.charAt(e.innerHTML)
                      e.classList = 'letra-incorrect'
                    }, 100 * i)
                  })
    }
  }

  function retriveLastGame(la, le){
    const arrSelectdiv = Array.prototype.slice.call(document.getElementsByClassName('letra-hidden'));
    const arrBancoDiv = Array.prototype.slice.call(document.getElementsByClassName('banco'));
    const image = document.getElementsByClassName('corda');

    erros = le
    
    for (let i = 0; i < palavraNormalize.length; i++){
      if (la.includes(palavraNormalize[i])){
        arrSelectdiv[i].innerHTML = palavra[i]
        setTimeout(() => {
          arrSelectdiv[i].classList = 'letra-correct'
        }, 50 * i + 1)

      }
      else {
        arrSelectdiv[i].innerHTML = palavra[i]
        setTimeout(() => {
          arrSelectdiv[i].classList = 'letra-not-guessed'
        }, 50 * i + 1)
        
      }
    }

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

  function initStatus(){
    if (gameData['game_status'] == 'init'){
      janelaAjuda();
    }
    else if(gameData['curDay'] == curDay) {

      retriveLastGame(gameData['last_acertos'], gameData['last_erros']);
      if(gameData['game_status'] == 'lost'){
        showJanelaEndGame('gameover')
      } else {
        showJanelaEndGame('winner')
      }
    }
  }

  function criaJogo() {
    var div = document.getElementsByClassName("letras-div").item(0); 
    for(let c in palavra){
      var p = document.createElement('p1');
      p.classList.add('letra-hidden');
      // p.innerText = palavra[c];
      p.innerText = c;
      if(palavra[c] === " "){
        p.classList.add('opacity-0', 'blank')
      }
      div.appendChild(p);
    }
  }

  async function endGame(event){
    let gameResult;

    if(event === 'winner'){
      totalVitorias += 1;
      gameResult = 'win'
      finalGamePOSTRequest['status'] = 'winner'
    } else {
      totalDerrotas += 1;
      gameResult = 'lost'
      finalGamePOSTRequest['status'] = 'lost'
    }

    gameData['vitorias']      = totalVitorias;
    gameData['derrotas']      = totalDerrotas;
    gameData['game_status']   = gameResult;
    gameData['curDay']        = curDay;
    gameData['last_acertos']  = acertos;
    gameData['last_erros']    = erros;
    localStorage.setItem('status', JSON.stringify(gameData))
 
    try {
      const response = await fetch(server, 
                                  {method: 'POST',
                                  headers: {
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/json'
                                          },
                                  body: JSON.stringify(finalGamePOSTRequest)});
      const statusCheck = await response.json();
      // console.log(statusCheck)
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
    // countdown.innerText = '14:22:26'
    cdDiv.appendChild(countdown)
    cdRoot.style.display = "flex"
    cdRoot.style.flex = "1"
    cdRoot.style.flexDirection = 'column '
    

    // Set the date we're counting down to
    const now = new Date()
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

      // Display the result in the element with id="demo"
      countdown.innerHTML = hours + "h " + ( minutes < 10 ? "0" + minutes : minutes) + "m " + ( seconds < 10 ? "0" + seconds : seconds) + "s ";

    // If the count down is finished, write some text
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

  function updateDica(){
    document.getElementById('dica-text-body').innerHTML = dica;
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
    
    await navigator.share({'text': shareResultText[erros.length]})
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
      <div class="janela gameover">
        <!-- <button @click="closeWindow" class="close-button btn-gameover"> x </button> -->
        <div class="janela-title">
          <p class="title title-winner-lose">Game over :(</p>
        </div>
      </div>

      <!-- WINNER -->
      <div class="janela winner">
        <!-- <button @click="closeWindow" class="close-button btn-winner"> x </button> -->
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
          <p class="dica-text-body" id="dica-text-body"> {{ dica }} </p>
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

      <!--LETRAS -->
      <div class="letras-div">  </div>

      <!-- TECLADO -->
      <div class="teclado-componente">
        <Teclado @keyPressed="keyPressed"/>
      </div>

    </div> <!--SECAO PRINCIPAL-->



  </div>
</template>
