<script setup>

const machine = {
  state: 'hidden',
  transitions: {
    hidden: {
      switch() {
        this.state = 'visible'
      }
    },
    visible: {
      switch() {
        this.state = 'hidden'
      }
    }
  },
  dispatch(actionName){
    const action = this.transitions[this.state][actionName];

    if (action) {
      action.call(this);
    } else {
      console.log('Invalid action.')
    }
  }

}
  
</script>

<template>

 
</template>
