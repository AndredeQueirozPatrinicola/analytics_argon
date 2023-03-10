function animaSearchBar(){
    document.querySelector(".search-input").addEventListener("focus", function() {
        document.querySelector(".searchbar-div").classList.add("is-toggled");
      });
      
    document.querySelector(".search-input").addEventListener("blur", function() {
        document.querySelector(".searchbar-div").classList.remove("is-toggled");
    });
}

export default animaSearchBar