<template>
  <div class="about">
    <div class="about-content">
      <h1>Über Uns</h1>
      <p>SportsMap ist eine innovative Plattform für Sportbegeisterte aller Art, entwickelt von drei Schülern der HTL Anichstraße im Rahmen ihrer Diplomarbeit. Ihre Vision ist es, die Welt des Sports für Menschen auf der ganzen Welt zugänglicher und vernetzter zu gestalten.</p>
      <p>Egal, ob Sie nach neuen Trainingspartnern suchen, an lokalen Sportevents teilnehmen möchten oder einfach nur Inspiration für Ihre nächste sportliche Aktivität brauchen – bei SportsMap Sie genau richtig!</p>
    </div>
    <h2>Die Entwickler</h2>
    <div class="developers">
      <div class="developer" v-for="developer in developers" :key="developer.name">
        <div class="developer-info">
          <div class="image-container">
            <img :src="developer.image" :alt="developer.name">
          </div>
          <div class="description" v-html="developer.description"></div>
        </div>
      </div>
    </div>
    <div class="project-info">
      
      <h3>Ausgangslage</h3>
      <p>Das Beginnen einer neuen Sportart oder das Finden von Gleichgesinnten innerhalb eines Sports kann eine Herausforderung sein. Diese Problematik soll erleichtert werden mit einem webbasierten Community-Portal zur Organisation von Gruppensportevents. Diese werden kartenbasiert dargestellt mit Informationen zu Ort, Zeit, Erfahrungslevel, Anzahl der Teilnehmer und einer Möglichkeit zur Kommunikation.</p>
      <h3>Zielsetzung</h3>
      <p>Unsere Zielsetzung ist es, durch Produktentwicklung im Bereich Softwareentwicklung und Wirtschaft einen umfassenden Einblick in dessen gesamten Entwicklungsprozess zu erhalten. In diesem Kontext wenden wir bereits erworbenes Wissen praktisch an und erweitern es um projektspezifische Neuerungen. Diese konzentrieren sich insbesondere auf die Bereiche Softwareentwicklung und die datenschutzkonforme Erfassung von Daten.</p>
      <h3>Geplantes Ergebnis</h3>
      <p>Das geplante Ergebnis ist, eine webbasierte GIS-Anwendung zu entwickeln, um die Organisation von Gruppensportevents zu erleichtern. Das schafft die Möglichkeit, neue Trainingspartner und Sportarten kennenzulernen. Dazu analysieren wir das Potential dieser Idee auf dem Markt, indem wir eine Feasibility-Study ausarbeiten.</p>
    </div>
    <br>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      developers: [
        {
          name: 'Pavel Khaklou',
          image: require('@/assets/chad.jpg'),
          description: '<b>Pavel Khaklou</b><br>先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地'
        },
        {
          name: 'David Cech',
          image: require('@/assets/chad.jpg'),
          description: '<b>Cech David</b><br>先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地'
        },
        {
          name: 'Jonathan Gendu',
          image: require('@/assets/chad.jpg'),
          description: '<b>Jonathan Gendu</b><br>先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地 生 先 天 地'
        }
      ]
    }
  }
}
</script>

<style>
.about {
  text-align: center;
  padding: 20px;
}

.about-content,
.project-info {
  padding-left: 20px;
  padding-right: 20px;
  text-align: left;
  margin-bottom: 40px;
}

.developers {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  background-image: url('@/assets/bg_start.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 20px 20px;
  margin-left: -20px;
  margin-right: -20px;
}

.developer {
  max-width: 300px;
  margin: 20px;
}

.image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
}

.image-container img {
  width: auto;
  height: 100%;
}

.developer-info {
  position: relative;
}

.description {
  position: absolute;
  top: 0;
  left: 160px;
  width: 200px;
  padding: 10px;
  background-color: white;
  border-radius: 8px;
  color: black;
  font-size: 12px;
}

.project-info {
  margin-top: 40px;
}
</style>
