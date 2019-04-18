<template>
  <div id="vtb-info-panel">
    <div class="row">
      <h2 id="vtb-channel" class="vtb-name">{{vtb.channel}}</h2>
    </div>
    <div class="row">
      <img
        id="vtb-icon"
        class="img-thumbnail rounded-circle mx-auto d-block vtb-icon"
        :src="thumbnil"
      >
    </div>
    <div id="vtb-info" class="row" style="padding-top:40px">
      <p id="vtb-name" class="vtb-info-item typewriter">
        <strong id="vtb-name">{{vtb.name}}</strong>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    vtb: {
      name: String,
      channel: String
    }, 
    thumbnil: String
  }
};
</script>


<style scoped>
/* css file for data page */

/* 
html, body {margin:0;padding:0;height:100%;} */

code {
  font-size: 80%;
}

.vtb-name {
  padding-top: 10px;
  padding-bottom: 10px;
  margin-bottom: 40px;
}

.vtb-icon {
  height: 300px;
  width: 300px;
  animation: fade-in 1s;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.typewriter {
  overflow: hidden; /* Ensures the content is not revealed until the animation */
  border-right: 0.15em solid black; /* The typwriter cursor */
  white-space: nowrap; /* Keeps the content on a single line */
  margin: 0 auto; /* Gives that scrolling effect as the typing happens */
  letter-spacing: 0.15em; /* Adjust as needed */
  animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
}

/* The typing effect */
@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

/* The typewriter cursor effect */
@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: black;
  }
}

.vtb-info-item {
  font-size: 30px;
}
</style>

