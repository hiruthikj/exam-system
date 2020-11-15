                        /*
            *  Creates a progressbar.
            *  @param id the id of the div we want to transform in a progressbar
            *  @param duration the duration of the timer example: '10s'
            *  @param callback, optional function which is called when the progressbar reaches 0.
            */
           function createProgressbar(id, duration, time_sec, callback) {
            // We select the div that we want to turn into a progressbar
            var progressbar = document.getElementById(id);
            progressbar.className = 'progressbar progress-bar-striped progress-bar-animated';
        
            // We create the div that changes width to show progress
            var progressbarinner = document.createElement('div');
            progressbarinner.className = 'inner';
        
            // Now we set the animation parameters
            progressbarinner.style.animationDuration = duration;
        
            // Eventually couple a callback
            if (typeof(callback) === 'function') {
            progressbarinner.addEventListener('animationend', callback);
            }
        
            // Append the progressbar to the main progressbardiv
            progressbar.appendChild(progressbarinner);

            // When everything is set up we start the animation
            display = document.querySelector('#timer');
            startTimer(time_sec, display); 
            progressbarinner.style.animationPlayState = 'running';    
        }

        function startTimer(duration, display) {
        var timer = duration, minutes, seconds;
        setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                timer = duration;
            }
        }, 1000);
    }
        
        addEventListener('load', function() {
            createProgressbar('progressbar1', '10s', 10, function() {$( "#mysubmit" ).click(); $( "#modalsubmit" ).click(); });
        });


 
.progressbar {
    width: 80%;
    margin: 25px auto;
    border: solid 1px #000;
  }
  .progressbar .inner {
    height: 15px;
    animation: progressbar-countdown;
    /* Placeholder, this will be updated using javascript */
    animation-duration: 40s;
    /* We stop in the end */
    animation-iteration-count: 1;
    /* Stay on pause when the animation is finished finished */
    animation-fill-mode: forwards;
    /* We start paused, we start the animation using javascript */
    animation-play-state: paused;
    /* We want a linear animation, ease-out is standard */
    animation-timing-function: linear;
  }
  @keyframes progressbar-countdown {
    0% {
      width: 100%;
      background: #0F0;
    }
    100% {
      width: 0%;
      background: #F00;
    }
  }   

  */