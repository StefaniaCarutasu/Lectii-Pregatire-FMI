function includeContent(url, date=null) {
    // create http request for page
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            // add html content to pop-up
            let rootForInlcudedContent = document.getElementById("include-content");
            rootForInlcudedContent.innerHTML = this.responseText;

            }
          }
    xhttp.open("GET", url, true);
    xhttp.send();
}