<template>
  <div id="app">
    <StudentPortal />
    <TeacherDashboard />
  </div>
</template>

<script>
import StudentPortal from './components/StudentPortal.vue'
import TeacherDashboard from './components/TeacherDashboard.vue'

export default {
  components: { StudentPortal, TeacherDashboard }
}
</script>