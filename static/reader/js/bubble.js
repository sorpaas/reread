/*
 * Scroll bubble
 * based on http://jsfiddle.net/michaelhue/7NAvm/7/light/
 */

$(window).load(function() {
	var total_reading_time = new Time(),
			scrollTimer = null,
			touch = 'ontouchstart' in window,
			totalScroll = 0,
			previousScroll = 0,
			viewportHeight = $(window).height(),
			documentHeight = $(document).height(),
			bubble = $('#scrollbubble'),
			post = $("#content"),
			bubbleText = $('#scrollBubbleText');

	// calculate total reading time
	total_reading_time.setTime(timeToRead(post.children())); 
	// show initial bubble
	//staticBubble(total_reading_time.firstString());


	/* event listeners */

	// detect starts and stops to evaluate if we need to show the bubble or not
	$(window).bind('scrollstart', function(e) {
		previousScroll = null;
	});

	$(window).bind('scrollstop', function(e) {
		totalScroll = 0;
	});

	if(touch)
		bubble.css('webkit-transition', '-webkit-transform 0.2s ease-out');

	// main scroll function
	$(window).scroll(function() {
		if($(document).scrollTop() < 100) { 
			// post start
			//staticBubble(total_reading_time.firstString());
			bubble.fadeOut(100);
		} else if(((post.offset().top + post.height() - viewportHeight) - $(document).scrollTop()) < 100) {
			// post end
			//staticBubble(total_reading_time.lastString());
			bubble.fadeOut(100);

		} else if(!touch && $(document).scrollTop() > 300) { 
			// normal cases
			scrollBubble();
		} else {
			bubble.fadeOut(100);
		}
	});

	function staticBubble(text) {
		if (scrollTimer !== null)
			clearTimeout(scrollTimer);

		var distance = distanceBubbleTop();

		if(touch)
			bubble.css('-webkit-transform', 'translate3d(0, ' + (distance + window.pageYOffset) + 'px, 0)');
		else
			bubble.css('top', distance);

		bubbleText.html(text)
		bubble.fadeIn(100);
	}

	function scrollBubble() {
		var progressPost = $(document).scrollTop() / post.height();
				distanceTop = $(document).scrollTop();

		var distance = distanceBubbleTop();

		bubble.css('top', distance);

		if(previousScroll != null)
			totalScroll += Math.abs(previousScroll - distanceTop);

		previousScroll = distanceTop;

		var final_time = new Time();
		final_time.setTime(total_reading_time.seconds*(1-progressPost));

		bubbleText.html(final_time.readingString());

		if(totalScroll >= viewportHeight*1.5 && bubble.css('display') == 'none')
			bubble.fadeIn(100);
		
		// Fade out the annotation after 1 second of no scrolling.
		if (scrollTimer !== null) {
			clearTimeout(scrollTimer);
		}

		scrollTimer = setTimeout(function() {
			bubble.fadeOut(100);
		}, 1000);
	}

	// helper function to calculate where to draw the bubble 
	function distanceBubbleTop() {
		var progress = $(document).scrollTop() / (documentHeight - viewportHeight),
				scrollbarHeight = viewportHeight / documentHeight * viewportHeight,
				distance = 0;

		return progress * (viewportHeight - scrollbarHeight) + scrollbarHeight/2 - bubble.height()/2;
	}


	// helper function to count the number of words in an array
	function timeToRead(array) {
		var total = 0;

		array.each(function() {
			total += Math.round(60*$(this).text().split(' ').length/200); // 200 = number of words per minute
		});	

		return total; 
	}
});



/*
 * Time Object 
 */

function Time() {
	this.m = 0;
	this.s = 0;
	this.seconds = 0;
	this.strings = {
		'en': {
			'Thank you.': 'Thank you.',
			'less than 1 minute left': 'less than 1 minute left',
			'1 minute left': '1 minute left',
			' minutes left':' minutes left',
			'1 minute reading time': '1 minute reading time',
			' minutes reading time': ' minutes reading time'
		},
		'ch': {
			'Thank you.': 'Danke.',
			'less than 1 minute left': '< 1 Minute verbleibend',
      '1 minute left': '1 Minute verbleibend',
      ' minutes left':' Minuten verbleibend',
      '1 minute reading time': '1 Minute Lesezeit',
      ' minutes reading time': ' Minuten Lesezeit'
		},
		'de': {
			'Thank you.': 'Danke.',
			'less than 1 minute left': '< 1 Minute verbleibend',
      '1 minute left': '1 Minute verbleibend',
      ' minutes left':' Minuten verbleibend',
      '1 minute reading time': '1 Minute Lesezeit',
      ' minutes reading time': ' Minuten Lesezeit'
		},
		'ja': {
			'Thank you.': 'Thank you.',
			'less than 1 minute left': 'less than 1 minute left',
			'1 minute left': '1 minute left',
			' minutes left':' minutes left',
			'1 minute reading time': '1 minute reading time',
			' minutes reading time': ' minutes reading time'
		}
	}

	// country detection mechanism
	var href = window.location.href;
	if(href.indexOf('/ch/') != -1)
		this.country = 'ch';
	else if(href.indexOf('/ja/') != -1)
		this.country = 'ja';
	else if(href.indexOf('/de/') != -1)
		this.country = 'de';
	else
		this.country = 'en';
}

Time.prototype.toString = function() {
	var m = (this.m < 10) ? '0' + this.m : this.m,
			s = (this.s < 10) ? '0' + this.s : this.s;
	return m + ':' + s;
}

Time.prototype.readingString = function() {
	if(this.seconds < 0 || (this.m == 0 && this.s <= 20))
		return this.lang('Thank you.');
	else if(this.m == 0 && this.s <= 60)
		return this.lang('less than 1 minute left');
	else if(this.m == 1)
		return this.lang('1 minute left');
	else
		return this.m + this.lang(' minutes left');
}

Time.prototype.firstString = function() {
	if(this.m <= 1)
		return this.lang('1 minute reading time');
	else
		return this.m + this.lang(' minutes reading time');
}

Time.prototype.lastString = function() {
	return this.lang('Thank you.');
}

Time.prototype.setTime = function(seconds) {
	this.m = Math.floor(seconds / 60);
	this.s = seconds % 60;

	this.seconds = seconds;
}

Time.prototype.lang = function(string) {
	return this.strings[this.country][string];
}
