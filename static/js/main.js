      (function makeDiv(){
        var names = ['Browsi',
        'CYTIOT',
        'ApolloShield',
        'PATH',
        'Causemo',
        'Cinchcast',
        'Zoey',
        'Women.com',
        'DevMynd',
        'GovX',
        'LeaseAccelerator',
        'Datami',
        'Wildfang',
        'FINCAD',
        'WebyClip',
        'doubleTwist',
        'Jia.com',
        'PipelineDeals',
        'Vindi',
        'Storone',
        'Olpays',
        'Bioscale',
        'Hepstar',
        'Enflux',
        'Tribridge',
        'DevicePilot',
        'Sweetch',
        'Roseonly',
        'Hedgy',
        'CityBldr',
        'Flipps',
        'misterb&b',
        'Paxos',
        'Weimob',
        'ClearScholar',
        'LumaTax',
        'Thatgamecompany',
        'Thunkable',
        'Transfluent',
        'Inventorum',
        'ivee',
        'PrivacyCheq',
        'PredicSis',
        'Pulpix',
        'SecretSales',
        'Stratumn',
        'Bonaverde',
        'Pushbullet',
        'Velvetcase',
        'Giftagram',
        'Paradromics',
        'AFAR',
        'Farmobile',
        'Travelio',
        'MedCrypt',
        'AuditFile',
        'ClickDimensions'];

        var name =  names[Math.floor(Math.random() * names.length)];
        console.log(name)

          var divsize = 200;
          var color = '#'+ Math.round(0xffffff * Math.random()).toString(16);
          $newdiv = $('<div/>').css({
              'width':divsize+'px',
              'height':divsize+'px',
              'color': color
          });

          var posx = (Math.random() * ($(document).width() - divsize)).toFixed();
          var posy = (Math.random() * ($(document).height() - divsize)).toFixed();
          $newdiv.append("<h1>"+name.toString()+"<h1>");
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
