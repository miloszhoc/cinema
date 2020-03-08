function highlight_element(hovered, highlighted) {
    return $(document).ready(function () {
        $(hovered).hover(function () {
            $(highlighted).css("background-color", "yellow");
        }, function () {
            $(highlighted).css("background-color", "pink");
        });
    });
}

function myFunction() {
    var x = document.getElementById("mySelect").value;
    document.getElementById("demo").innerHTML = "You selected: " + x;
}

