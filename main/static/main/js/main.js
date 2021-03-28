

$(document).ready(function (){
    AOS.init();

    // click to scroll top
    $('.move-up span').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })
})



const nav = document.querySelector('.navbar-nav'),
    navList = nav.querySelectorAll('li'),
    totalNavList = navList.length;

for (let i = 0; i<totalNavList; i++) {
    const a = navList[i].querySelector('a');
    a.addEventListener('click', function() {
        for (let j = 0; j<totalNavList; j++){
            navList[j].querySelector('a').classList.remove('active');
        }
        this.classList.add('active');
    })
}