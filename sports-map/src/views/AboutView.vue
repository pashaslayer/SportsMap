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
          <div class="description">
            <img :src="developer.image" :alt="developer.name" class="developer-image">
            <div class="text-container">
              <div v-html="developer.description"></div>
            </div>
          </div>
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
    <div class="impressum">
      <h3>Impressum</h3>
      <p>
        SportsMap GmbH<br>
        Museumstraße 9<br>
        6020 Innsbruck<br>
        Telefon: +42 650 2842852<br>
        E-Mail: sportsmap@outlook.com<br>
        Vertreten durch: Jonathan Gendu
      </p>
    </div>
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
          description: '<b>Pavel Khaklou</b><br>Max Mustermann, ein erfahrener Projektmanager in der Musterfirma, koordiniert erfolgreich komplexe Projekte und pflegt Kundenbeziehungen. Seine Fähigkeit, Mitarbeiter zu motivieren und strategische Ziele zu verfolgen, macht ihn zu einer wertvollen Bereicherung für das Unternehmen.'
        },
        {
          name: 'David Cech',
          image: require('@/assets/chad.jpg'),
          description: '<b>Cech David</b><br>Max Mustermann, ein erfahrener Projektmanager in der Musterfirma, koordiniert erfolgreich komplexe Projekte und pflegt Kundenbeziehungen. Seine Fähigkeit, Mitarbeiter zu motivieren und strategische Ziele zu verfolgen, macht ihn zu einer wertvollen Bereicherung für das Unternehmen.'
        },
        {
          name: 'Jonathan Gendu',
          image: require('@/assets/chad.jpg'),
          description: '<b>Jonathan Gendu</b><br>Max Mustermann, ein erfahrener Projektmanager in der Musterfirma, koordiniert erfolgreich komplexe Projekte und pflegt Kundenbeziehungen. Seine Fähigkeit, Mitarbeiter zu motivieren und strategische Ziele zu verfolgen, macht ihn zu einer wertvollen Bereicherung für das Unternehmen.' 
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
  width: 300px;
  margin-bottom: 20px;
}

.developer-info {
  display: flex;
  flex-direction: column;
}

.description {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 10px;
  border-radius: 8px;
  color: black;
  font-size: 12px;
  margin-top: 10px;
  overflow: auto;
}

.developer-image {
  width: 100%;
  max-width: 200px; 
  height: auto;
  border-radius: 8px; 
}

.text-container {
  padding-top: 10px; 
}

.project-info {
  margin-top: 40px; 
}

.impressum {
  background-color: white; 
  padding: 20px;
  border-radius: 8px;
  margin-top: 40px; 
}

.impressum h3,
.impressum p {
  color: black;
}
</style>
