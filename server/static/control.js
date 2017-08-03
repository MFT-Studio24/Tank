$(function() {
  var base_url = "http://" + location.host + "/";
  var object_map = {
    87: {"char": "w",     "obj": "tank",   "move": "forward" , "is_down": false},
    83: {"char": "s",     "obj": "tank",   "move": "backward", "is_down": false},
    65: {"char": "a",     "obj": "tank",   "move": "left"    , "is_down": false},
    68: {"char": "d",     "obj": "tank",   "move": "right"   , "is_down": false},
    38: {"char": "up",    "obj": "camera", "move": "up"      , "is_down": false},
    40: {"char": "down",  "obj": "camera", "move": "down"    , "is_down": false},
    37: {"char": "leff",  "obj": "camera", "move": "left"    , "is_down": false},
    39: {"char": "right", "obj": "camera", "move": "right"   , "is_down": false},
    32: {"char": "space", "obj": "camera", "move": "center"  , "is_down": false}
  };

  var isButtonDown = false;
  
  // for keyboard
  $(window).keydown(function(e){
    keyDown(e.keyCode);
  });
  
  $(window).keyup(function(e){
    keyUp(e.keyCode);
  });

  // for control pad
  $("#controlPad button").on("mousedown touchstart", function(e){
    if (!isButtonDown) {
      keyDown(e.target.value);
      isButtonDown = true;
      e.preventDefault();
    }
  });

  $("#controlPad button").on("mouseup touchend", function(e){
    if (isButtonDown) {
      keyUp(e.target.value);
      isButtonDown = false;
      e.preventDefault();
    }
  });

  var keyDown = function(keyCode) {
    if (object_map[keyCode]) {
      k = object_map[keyCode];
      if (k["is_down"] == false) {
        console.log("DOWN: " + k["char"]);
        $.get(base_url + "control", { obj:k["obj"], move:k["move"], mode:"start" });
      }
      k["is_down"] = true;
    }
  };

  var keyUp = function(keyCode) {
    if (object_map[keyCode]) {
      k = object_map[keyCode];
      console.log("UP: " + k["char"]);
      $.get(base_url + "control", { obj:k["obj"], move:k["move"], mode:"stop" });
      k["is_down"] = false;
    }
  };

});
