// SOURCE: https://stackoverflow.com/questions/6328718/how-to-wrap-surround-highlighted-text-with-an-element

function highlightSelection() {       
    let selection= window.getSelection().getRangeAt(0);
    let selectedContent = selection.extractContents();
    var span= document.createElement("span");
    span.style.backgroundColor = "yellow";
    span.appendChild(selectedContent);
    selection.insertNode(span);
}