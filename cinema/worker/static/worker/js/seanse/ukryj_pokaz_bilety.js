//funkcja pokazuje/ukrywa szczegoly rezerwacji
function show_hide(element_id) {
    let ticket_full_id = 'tickets' + element_id;
    let details_full_id = 'details' + element_id;

    let ticket = document.getElementById(ticket_full_id);
    let show_hide_text = document.getElementById(details_full_id);

    if (ticket.style.display === "none") {
        show_hide_text.innerText = 'Ukryj szczegóły';
        ticket.style.display = 'block';
    } else {
        show_hide_text.innerText = 'Pokaż szczegóły';
        ticket.style.display = 'none';
    }
}