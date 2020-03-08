function highlight_element(hovered, highlighted) {
    return $(document).ready(function () {
        $(hovered).hover(function () {
            $(highlighted).css("background-color", "yellow");
        }, function () {
            $(highlighted).css("background-color", "pink");
        });
    });
}

