function includeReviewForm(url) {
    // create http request for page
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            // add html content to pop-up
            let rootForInlcudedContent = document.getElementById("include-review-form");
            rootForInlcudedContent.innerHTML = this.responseText;

            }
          }
    xhttp.open("GET", url, true);
    xhttp.send();
}