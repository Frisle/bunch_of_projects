function sendXHR(type, url, data, callback) {
    var newXHR = new XMLHttpRequest();
    newXHR.open(type, url, true);
    newXHR.send(data);
    newXHR.onreadystatechange = function() {
      if (this.status === 200 && this.readyState === 4){
        callback(this.response);
      }
    };
  }

  sendXHR("GET", "cardsFile.txt", null, function(response) { // response contains the content of the cardsFile.txt file.
    document.getElementById("textFile").innerHTML = response; // Use innerHTML to get or set the html content.
  });

  