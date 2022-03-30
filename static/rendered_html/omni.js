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


document.body.addEventListener("click", function() {
  if (document.getElementById('textAreaDiv').style.visibility="hidden"){
  document.getElementById('textAreaDiv').style.visibility="visible";}
  else{
  document.getElementById('textAreaDiv').style.visibility="hidden";}
})

function popUpText() {
    definitions = document.getElementById("[unique ID for defintion]")
    // document.getElementById("myPopup").innerHTML = definitions.innerHTML
    document.getElementById("myPopup").innerHTML = '"Administration" and "Administrator" mean the Small Business Administration and the Administrator thereof, respectively.'
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");            
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

function toggleGuidebars() {
    if (document.getElementsByTagName("subsection")[0].style.borderLeftStyle === "hidden") {
        for (i = 0; i < document.getElementsByTagName("subsection").length; i++){
            document.getElementsByTagName("subsection")[i].style.borderLeftStyle = "solid"; 
        }
        for (i = 0; i < document.getElementsByTagName("paragraph").length; i++){
            document.getElementsByTagName("paragraph")[i].style.borderLeftStyle = "solid"; 
        }
        for (i = 0; i < document.getElementsByTagName("subparagraph").length; i++){
            document.getElementsByTagName("subparagraph")[i].style.borderLeftStyle = "solid"; 
        }
        for (i = 0; i < document.getElementsByTagName("clause").length; i++){
            document.getElementsByTagName("clause")[i].style.borderLeftStyle = "solid"; 
        }
        for (i = 0; i < document.getElementsByTagName("subclause").length; i++){
            document.getElementsByTagName("subclause")[i].style.borderLeftStyle = "solid"; 
        }
        for (i = 0; i < document.getElementsByTagName("item").length; i++){
            document.getElementsByTagName("item")[i].style.borderLeftStyle = "solid"; 
        }
    }
    else {
        for (i = 0; i < document.getElementsByTagName("subsection").length; i++){
            document.getElementsByTagName("subsection")[i].style.borderLeftStyle = "hidden"; 
        }
        for (i = 0; i < document.getElementsByTagName("paragraph").length; i++){
            document.getElementsByTagName("paragraph")[i].style.borderLeftStyle = "hidden"; 
        }
        for (i = 0; i < document.getElementsByTagName("subparagraph").length; i++){
            document.getElementsByTagName("subparagraph")[i].style.borderLeftStyle = "hidden"; 
        }
        for (i = 0; i < document.getElementsByTagName("clause").length; i++){
            document.getElementsByTagName("clause")[i].style.borderLeftStyle = "hidden"; 
        }
        for (i = 0; i < document.getElementsByTagName("subclause").length; i++){
            document.getElementsByTagName("subclause")[i].style.borderLeftStyle = "hidden"; 
        }
        for (i = 0; i < document.getElementsByTagName("item").length; i++){
            document.getElementsByTagName("item")[i].style.borderLeftStyle = "hidden"; 
        }
    }
}

