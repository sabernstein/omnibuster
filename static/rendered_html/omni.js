var coll = document.getElementsByClassName("collapsible");
        var i;
        var j;
        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var parent = this.parentElement;
            var content = parent.children;
            for (j = 0; j < content.length; j++) {
                var kiddo = content.item(j);
                let booleanValue = false;
                if ((kiddo.tagName == "SUBSECTION") || (kiddo.tagName == "PARAGRAPH") || (kiddo.tagName == "SUBPARAGRAPH") || (kiddo.tagName == "CLAUSE") || (kiddo.tagName == "SUBCLAUSE") || (kiddo.tagName == "ITEM")) {
                    booleanValue = true;
                }
                else {
                    booleanValue = false;
                }
                if (booleanValue == true) {
                    if (kiddo.style.display === "none") {
                    kiddo.style.display = "block";
                    }
                    else {
                    kiddo.style.display = "none";
                    }
                }
                else {
                }
            }
          });
        }

// SOURCE: https://stackoverflow.com/questions/6328718/how-to-wrap-surround-highlighted-text-with-an-element

function highlightSelection() {       
    let selection= window.getSelection().getRangeAt(0);
    let selectedContent = selection.extractContents();
    var span= document.createElement("span");
    span.style.backgroundColor = "yellow";
    span.appendChild(selectedContent);
    selection.insertNode(span);
}

document.body.addEventListener("click", function() {
  if (document.getElementById('textAreaDiv').style.visibility="hidden"){
  document.getElementById('textAreaDiv').style.visibility="visible";}
  else{
  document.getElementById('textAreaDiv').style.visibility="hidden";}
})

