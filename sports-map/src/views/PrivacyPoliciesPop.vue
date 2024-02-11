<template>
  <div v-if="showPopupPolicies" class="popup-form">
    <div class="popup-content">
      <h2>Privatsphäre-Einstellungen</h2>
      <p>
        Diese Seite nutzt Website-Tracking-Technologien von Dritten, um ihre
        Dienste anzubieten, stetig zu verbessern und Werbung entsprechend den
        Interessen der Nutzer anzuzeigen.
      </p>
      <div class="policy-links">
        <!-- target="_blank => opens a new window"-->
        <a href="./../assets/privacy-policy.pdf" @click="openPdf">Datenschutzerklärung</a> |
        <router-link to="/about" @click="handleImpressum">About</router-link>
      </div>
      <div class="cookie-options">
        <div class="cookie-option">
          <input type="checkbox" id="marketing" v-model="acceptMarketing" />
          <label for="marketing">Marketing</label>
        </div>
        <div class="cookie-option">
          <input type="checkbox" id="functional" v-model="acceptFunctional" />
          <label for="functional">Funktionell</label>
        </div>
        <div class="cookie-option">
          <input
            type="checkbox"
            id="essential"
            v-model="acceptEssential"
            disabled
            checked
          />
          <label for="essential">Essenziell</label>
        </div>
      </div>
      <div class="buttons">
        <button @click="savePreferences">Dienste speichern</button>
        <button @click="declineAll">Ablehnen</button>
        <button @click="acceptAll">Alles akzeptieren</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showPopupPolicies: Boolean,
    onClose: Function,
  },
  data() {
    return {
      acceptMarketing: false,
      acceptFunctional: false,
      acceptEssential: true, // Essential cookie
    };
  },
  methods: {
    closePopup() {
      this.$emit("handlepoliciespopupclose");
    },
    handleImpressum(){
      this.closePopup();
    },
    openPdf() {
      const pdfPath = '../assets/privacy-policy.pdf';
      const pdfUrl = `${window.location.origin}/${pdfPath}`;
            window.open(pdfUrl, '_blank');
    },
    savePreferences() {
      // Logic to save preferences
      this.closePopup();
    },
    declineAll() {
      this.acceptMarketing = false;
      this.acceptFunctional = false;
      this.savePreferences();
      this.closePopup();
    },
    acceptAll() {
      this.acceptMarketing = true;
      this.acceptFunctional = true;
      this.savePreferences();
    },
  },
};
</script>

<style>
.popup-form {
  background-color: #fff; /* changed from lightblue to white */
  position: fixed; /* changed from absolute to fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* this centers the popup */
  z-index: 1000;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #333; /* changed from darkblue to a softer dark color */
  width: 50%; /* changed to a percentage to adapt to different screen sizes */
  max-width: 500px; /* maximum width of the popup */
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popup-content h3 {
  margin-top: 0;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="number"],
select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

#description {
  height: 2cm;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #444;
  color: white;
  cursor: pointer;
}

.policy-links {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px; /* Add some space before the cookie options */
}

.policy-links a {
  color: #000103;
  text-decoration: none;
}

.policy-links a:hover {
  text-decoration: underline;
}

</style>
