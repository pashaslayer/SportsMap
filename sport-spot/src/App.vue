<template>
<!--  
  data-bs-keyboard        ... schließen des bootstrap offcanvas mittels esc
  data-bs-backdrop="true" ... schließen des offcanvas geht mit Klick auf restliche fläche falls "false" ... schließen geht nur über button rest ist mit unsichtbarem gitter
  d-none                  ... Diese Klasse bewirkt, dass das Element nicht auf dem Bildschirm sichtbar ist, es bleibt jedoch im HTML-Dokument vorhanden
  d-sm-block              ... Diese Klasse gehört zu den Responsive-Utilities von Bootstrap und ermöglicht es, Elemente je nach Bildschirmgröße und Breakpoint anzuzeigen oder auszublenden.
  px-0                    ... Die CSS-Klasse px-0 wird in Bootstrap verwendet, um den horizontalen (X-Achse) Padding (Innenabstand) eines HTML-Elements auf null zu setzen
  <i class="fs-5 bi-table"> .. für icon geht aber nicht bei links daher löäschen

-->
<div class="offcanvas offcanvas-start w-15" id="offcanvas" data-bs-keyboard="false" data-bs-backdrop="true">
    <div class="offcanvas-header">
        <h6 class="offcanvas-title d-none d-sm-block" id="offcanvas">Menu</h6>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body px-0">
        <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-start" id="menu">
            <li class="nav-item">
                <a class="nav-link text-truncate"> 
                    <span class="ms-1 d-none d-sm-inline"><router-link to="/">Home</router-link></span>
                </a>
            </li>
            <li>
                <a class="nav-link text-truncate">
                    <span class="ms-1 d-none d-sm-inline"><router-link to="/about">About</router-link></span> </a>
            </li>
            <li>
                <a class="nav-link text-truncate">
                    <span class="ms-1 d-none d-sm-inline"><router-link to="/login">Login</router-link></span> </a>
            </li>
            <li>
                <a class="nav-link text-truncate">
                    <span class="ms-1 d-none d-sm-inline"><router-link to="/registration">Registration</router-link></span> </a>
            </li>
            <li>
                <a class="nav-link text-truncate">
                    <span class="ms-1 d-none d-sm-inline"><router-link to="/admin">Admin</router-link></span> </a>
            </li>
        </ul>
    </div>
</div>
<button class="btn float-end" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" role="button">
  <i class="fa-solid fa-bars fa-xl" data-bs-toggle="offcanvas" data-bs-target="#offcanvas"></i>
            </button>
            <br>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: whitesmoke;
  border: 5px;
  border-color: black;
}

body{
  background-color: #108EB3;
  color: whitesmoke;
  border: 5px;
  border-color: black;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

export default {
  data() {
    return {
    }
  }
};
