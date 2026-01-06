<template>
  <div>
    <video ref="video" autoplay style="width: 400px; border: 2px solid black;"></video>
    <p v-if="status === 'Disconnected'" style="color: red;">Server Offline</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,
      status: "Connecting..."
    }
  },
  mounted() {
    
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        this.$refs.video.srcObject = stream;
        this.startEngine(); 
      })
      .catch((err) => {
        console.log("Camera error:", err);
      });
  },
  methods: {
    startEngine() {
      
      this.ws = new WebSocket("ws://127.0.0.1:8000/ws/student");

      this.ws.onopen = () => {
        this.status = "Connected";
        console.log("Server se jud gaya!");
        
        
        setInterval(() => {
          this.sendDataToServer();
        }, 300); 
      };

      this.ws.onclose = () => {
        this.status = "Disconnected";
      };
    },
    
    sendDataToServer() {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

      const v = this.$refs.video;
      const canvas = document.createElement("canvas");
      
      
      canvas.width = 300; 
      canvas.height = 200;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(v, 0, 0, canvas.width, canvas.height);

     
      const frame = canvas.toDataURL("image/jpeg", 0.6);

      
      const payload = {
        id: "student_01",
        image: frame
      };

      this.ws.send(JSON.stringify(payload));
    }
  }
}
</script>