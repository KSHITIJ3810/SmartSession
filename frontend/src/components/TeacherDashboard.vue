<template>
  <div style="padding: 20px; font-family: Arial, sans-serif;">
    <h2>Teacher's "Super Vision" Dashboard</h2>
    
    <div :style="statusCardStyle">
      <h3>Student Status: {{ displayStatus }}</h3>
      <p>Last Gaze Direction: {{ gazeDir }}</p>
      <p>Mood: {{ emotion }}</p>
    </div>

    <div style="margin-top: 20px; border: 1px solid #ccc; padding: 10px;">
      <h4>Session Timeline</h4>
      <p style="font-size: 12px; color: gray;">(Real-time updates happening...)</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,
      gazeDir: "Checking...",
      emotion: "Neutral",
      alertLevel: "Green",
      displayStatus: "Student is Focused"
    }
  },
  computed: {
    statusCardStyle() {
      let bgColor = "#d4edda"; // Green
      if (this.alertLevel === "Yellow") bgColor = "#fff3cd"; // Yellow
      if (this.alertLevel === "Red") bgColor = "#f8d7da"; // Red
      
      return {
        padding: '20px',
        borderRadius: '10px',
        backgroundColor: bgColor,
        border: '1px solid #333'
      };
    }
  },
  mounted() {
    this.ws = new WebSocket("ws://127.0.0.1:8000/ws/teacher");

    this.ws.onopen = () => {
      console.log("Teacher WebSocket connected");
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.gazeDir = data.gaze;
        this.emotion = data.emotion;

        if (data.is_proctor_alert) {
          this.alertLevel = "Red";
          this.displayStatus = "PROCTOR ALERT!";
        } else if (data.emotion === "Confused") {
          this.alertLevel = "Yellow";
          this.displayStatus = "Student is Confused";
        } else {
          this.alertLevel = "Green";
          this.displayStatus = "Student is Focused";
        }
      } catch (err) {
        console.error("Invalid JSON from backend:", event.data);
      }
    };
  }
}
</script>

<style scoped>
h2 {
  color: #42b983;
}
</style>