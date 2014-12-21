$(function() {
  var arrowNav = $('.arrow_nav.top.right');
  var topOffset = arrowNav.offset().top;
  var rightOffset = ($(window).width() - (arrowNav.offset().left + arrowNav.outerWidth()));

  var nextArticles = $('.next-articles');
  nextArticles.css('top', (topOffset + arrowNav.outerHeight()) + 'px');
  nextArticles.css('right', rightOffset + 'px');

  var DEBUG = false;
  if(DEBUG) {
    nextArticles.show();
    return;
  }

  var naShowing = false;
  var naAbortHiding = false;
  var hoverIn = function() {
    naAbortHiding = true;
    if(naShowing) {
      return;
    }
    nextArticles.show(100);
    naShowing = true;
  };
  var hoverOut = function() {
    if(!naShowing) {
      return;
    }

    naAbortHiding = false;
    setInterval(function() {
      if(naAbortHiding) {
        return;
      }
      nextArticles.hide(100);
      naShowing = false;
    }, 750);
  };

  var nextButton = $('#next-button');
  nextButton.hover(hoverIn, hoverOut);
  nextArticles.hover(hoverIn, hoverOut);
});
