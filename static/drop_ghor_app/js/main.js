
let nav = document.querySelector(".navbar");
window.onscroll = function () {
    if(document.documentElement.scrollTop > 20){
        nav.classList.add("header-scrolled");
        navCollapse.classList.remove("show");

    }else{
        nav.classList.remove("header-scrolled");
    }
}
// nav hide 
let navBar = document.querySelectorAll(".nav-link");
let navCollapse = document.querySelector(".navbar-collapse.collapse");
navBar.forEach(function(a){
    a.addEventListener("click", function(){
        navCollapse.classList.remove("show");
    })
})
const pass="pass"
sc=screen.width
if (sc<360) {
    let te=document.querySelectorAll(".res");
    te.forEach(b=>{
        b.classList.remove("col-6");
        b.classList.add("col-12");
    })
} else {
    pass
}
// copy affilink
function copyaffilink() {

    var content =document.getElementById('affilink').textContent; 
    console.log(content);
    navigator.clipboard.writeText(content);
    document.getElementById("copyaffi").innerHTML = "copied!";
    
  }
  
