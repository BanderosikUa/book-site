
const rating = document.querySelectorAll('.rating')[0]
console.log(rating)
initRating();


function initRating(){
    let ratingActive, ratingValue;
    initRatingVars(rating);
    setRatingActiveWidth();

    function initRatingVars(rating){
        ratingActive = rating.querySelector('.rating__active');
        console.log(ratingActive);
        ratingValue = rating.querySelector('.rating__value');
        console.log(ratingValue);
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML){
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }
}
