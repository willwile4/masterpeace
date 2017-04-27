$(document).ready(function() {
  $('.user_gallery').magnificPopup({type:'image'});
});

$('.user_gallery').magnificPopup({
  delegate: 'a', // child items selector, by clicking on it popup will open
  type: 'image',
  gallery: {
    enabled: false, // set to true to enable gallery

    preload: [0,2], // read about this option in next Lazy-loading section

    navigateByImgClick: true,

    arrowMarkup: '<button title="%title%" type="button" class="mfp-arrow mfp-arrow-%dir%"></button>', // markup of an arrow button

    tPrev: 'Previous (Left arrow key)', // title for left button
    tNext: 'Next (Right arrow key)', // title for right button
    tCounter: '<span class="mfp-counter">%curr% of %total%</span>' // markup of counter
  }
});
