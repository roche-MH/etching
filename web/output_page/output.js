const carouselSlide = document.querySelector('.carousel-slide');
const carouselImages = document.querySelectorAll('.carousel-slide img');
const carouselSlide2 = document.querySelector('.carousel-slide2');
const carouselImages2 = document.querySelectorAll('.carousel-slide2 img');
const carouselSlide3 = document.querySelector('.carousel-slide3');
const carouselImages3 = document.querySelectorAll('.carousel-slide3 img');


//Buttons
const previousBtn = document.querySelector('#previousBtn');
const nextBtn = document.querySelector('#nextBtn');
const previousBtn2 = document.querySelector('#previousBtn2');
const nextBtn2 = document.querySelector('#nextBtn2');
const previousBtn3 = document.querySelector('#previousBtn3');
const nextBtn3 = document.querySelector('#nextBtn3');

//Counter
let counter = 1;
const size = carouselImages[0].clientWidth;


carouselSlide.style.transform = 'translateX(' + (-size*counter) + 'px)';

nextBtn.addEventListener('click',()=>{
    if(counter >= carouselImages.length - 1) return;
    carouselSlide.style.transition = 'transform 0.2s ease-in-out';
    counter++;
    carouselSlide.style.transform = 'translateX(' + (-size*counter) + 'px)';
});

previousBtn.addEventListener('click',()=>{
    if(counter <= 0) return;
    carouselSlide.style.transition = 'transform 0.2s ease-in-out';
    counter--;
    carouselSlide.style.transform = 'translateX(' + (-size*counter) + 'px)';
});

nextBtn2.addEventListener('click',()=>{
    if(counter >= carouselImages2.length - 1) return;
    carouselSlide2.style.transition = 'transform 0.2s ease-in-out';
    counter++;
    carouselSlide2.style.transform = 'translateX(' + (-size*counter) + 'px)';
});

previousBtn2.addEventListener('click',()=>{
    if(counter <= 0) return;
    carouselSlide2.style.transition = 'transform 0.2s ease-in-out';
    counter--;
    carouselSlide2.style.transform = 'translateX(' + (-size*counter) + 'px)';
});

nextBtn3.addEventListener('click',()=>{
    if(counter >= carouselImages3.length - 1) return;
    carouselSlide3.style.transition = 'transform 0.2s ease-in-out';
    counter++;
    carouselSlide3.style.transform = 'translateX(' + (-size*counter) + 'px)';
});

previousBtn3.addEventListener('click',()=>{
    if(counter <= 0) return;
    carouselSlide3.style.transition = 'transform 0.2s ease-in-out';
    counter--;
    carouselSlide3.style.transform = 'translateX(' + (-size*counter) + 'px)';
});



carouselSlide.addEventListener('transitionend',()=>{
    if(carouselImages[counter].id === 'lastClone'){
        carouselSlide.style.transition = 'none';
        counter = carouselImages.length -2;
        carouselSlide.style.transform = 'translateX(' + (-size*counter) + 'px)';
    }
    if(carouselImages[counter].id === 'firstClone'){
        carouselSlide.style.transition = 'none';
        counter = carouselImages.length - counter;
        carouselSlide.style.transform = 'translateX(' + (-size*counter) + 'px)';

    }
});

function imageClick(img) {
    location.href="https://google.com";
}