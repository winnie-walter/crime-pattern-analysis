class MyHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML =
      `
<header class="navbar navbar-nav navbar-expand navbar-light navbar-theme-primary">

<div class="container-fluid px-3 px-md-4">


  <!-- -----------------website name and icon-------------- -->

  <div class="d-flex align-item pt-2 pb-2 pr-2s-center">
    <a class="navbar-brand shadow-soft py-2 px-3 rounded border border-light mr-xl-4" href="#">

      <span class="ml-2 text-dark" style="font-size: large;"><i class="fas fa-chart-pie"></i>&nbsp &nbsp Crime Data
        Analytics</span>
    </a>
  </div>

  <!-- ---------------------nav-bar-item pt-2 pb-2 pr-2s---------------------------- -->
  <div class="d-flex align-item pt-2 pb-2 pr-2s-center">
    <div class="d-none d-lg-block">
      <a href="index.html" class="btn btn-light text-dark mr-2"><i class="fas fa-home"></i>&nbsp Home</a>
      <a href="crime-charts.html" class="btn btn-light text-dark mr-2"><i class="fas fa-globe-asia"></i>&nbsp CrimeCharts</a>
      <a href="crime-predictor.html" class="btn btn-light text-dark mr-2"><i class="fas fa-robot"></i>&nbsp CrimePredictor</a>  
      <a href="about.html" class="btn btn-light text-dark mr-2"><i class="fas fa-user-secret"></i>&nbsp About Us</a>
      <a href="help-page.html" class="btn btn-light text-dark mr-2"><i class="fas fa-info-circle"></i>&nbsp Help</a>
      <a href="/data" class="btn btn-light text-dark mr-2"><i class="fas fa-info-circle"></i>&nbsp Data</a>
      <a href="/logout" class="btn btn-light text-dark mr-2"><i class="fas fa-info-circle"></i>&nbsp Logout</a>
    </div>
  </div>

  <a href="#" class="btn-emoji" onclick="audio()"></a>
    <i class="far fa-grin-tongue"></i>
  </a>

  <div id="" class="">
  <div class="drop">
    <div class="dropdown1">
      <button class="dropdown1-button btn btn-light outset-neomo">
        User
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown1-content ">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value="" id="defaultCheck1" checked>
          <label class="form-check-label" for="defaultCheck1">
            <a href="/user">User Management</a>
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value="" id="defaultCheck2">
          <label class="form-check-label" for="defaultCheck2">
            <a href=""> Profile</a>
          </label>
        </div>
      </div>

    </div>
  </div>
</div>
  <div id="txt"> </div>


</div>

<script src="https://kit.fontawesome.com/7bdcd846e8.js" crossorigin="anonymous"></script>


`

  }
}

customElements.define('my-header', MyHeader);
//<a href="/logout" class="btn-emoji" onclick="audio()"></a>
class MyHeader2 extends HTMLElement {
  connectedCallback() {
    this.innerHTML =
      `
<header class="navbar navbar-nav navbar-expand navbar-light navbar-theme-primary">

<div class="container-fluid px-3 px-md-4">


  <!-- -----------------website name and icon-------------- -->

  <div class="d-flex align-item pt-2 pb-2 pr-2s-center">
    <a class="navbar-brand shadow-soft py-2 px-3 rounded border border-light mr-xl-4" href="#">

      <span class="ml-2 text-dark" style="font-size: large;"><i class="fas fa-chart-pie"></i>&nbsp &nbsp Crime Data
        Analytics</span>
    </a>
  </div>

  <!-- ---------------------nav-bar-item pt-2 pb-2 pr-2s---------------------------- -->
  <div class="d-flex align-item pt-2 pb-2 pr-2s-center">
    <div class="d-none d-lg-block">
      <a href="index.html" class="btn btn-light text-dark mr-2"><i class="fas fa-home"></i>&nbsp Home</a>
      <a href="crime-charts.html" class="btn btn-light text-dark mr-2"><i class="fas fa-globe-asia"></i>&nbsp CrimeCharts</a>  
      <a href="about.html" class="btn btn-light text-dark mr-2"><i class="fas fa-user-secret"></i>&nbsp About Us</a>
      <a href="help-page.html" class="btn btn-light text-dark mr-2"><i class="fas fa-info-circle"></i>&nbsp Help</a>
      <a href="/logout" class="btn btn-light text-dark mr-2"><i class="fas fa-info-circle"></i>&nbsp Logout</a>
    </div>
  </div>

  <a href="#" class="btn-emoji" onclick="audio()"></a>
    <i class="far fa-grin-tongue"></i>
  </a>

  
  <div id="txt"> </div>


</div>

<script src="https://kit.fontawesome.com/7bdcd846e8.js" crossorigin="anonymous"></script>


`

  }
}

customElements.define('my-header2', MyHeader2);


class MyFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML =
      `
<footer>
<div class="row pt-5 mx-auto" style="
position: absolute;
bottom: 5;
left: 0;
right: 0;
display: flex;
flex-direction: row;
flex-wrap: nowrap;
align-content: center;
justify-content: center;
align-items: center;">
    <div class="col-3 "><i class="fas fa-copyright"></i> 2023 Crime Data Analysis All rights reserved </div>
</div>
</footer>


`

  }
}

customElements.define('my-footer', MyFooter);