      (function makeDiv(){
          var divsize = 200;
          var color = '#'+ Math.round(0xffffff * Math.random()).toString(16);
          $newdiv = $('<div/>').css({
              'width':divsize+'px',
              'height':divsize+'px',
              'color': color
          });
          
          var posx = (Math.random() * ($(document).width() - divsize)).toFixed();
          var posy = (Math.random() * ($(document).height() - divsize)).toFixed();
          $newdiv.append("<h1>JERE<h1>");
          $newdiv.css({
              'position':'absolute',
              'left':posx+'px',
              'top':posy+'px',
              'display':'none'
          }).appendTo( '#main' ).fadeIn(200).delay(400).fadeOut(400, function(){
            $(this).remove();
            makeDiv(); 
          }); 
      })();