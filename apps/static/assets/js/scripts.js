$(document).ready(function () {

    let artigo = document.getElementById('artigo');
    let livros = document.getElementById('livros');
    let capitulos = document.getElementById('capitulos');

    if(artigo === null){
        $('#capitulos').removeClass('show').removeClass('active');
        $('#grafico-livros').addClass('active')
    }else if(livros === null && artigo === null){
        $('#grafico-capitulos').addClass('active')
    }else{
        $('#livros').removeClass('show').removeClass('active');
        $('#capitulos').removeClass('show').removeClass('active');
    }

    $('#loading').css('display', 'none'); 

});


