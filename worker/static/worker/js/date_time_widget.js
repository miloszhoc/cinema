$('.timepicker').timepicker({
    timeFormat: 'HH:mm:ss',
    interval: 5,
    minTime: '00:05',
    maxTime: '23:55',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true
});

//https://xdsoft.net/jqplugins/datetimepicker/
$(function () {
    $("#id_start_date").datetimepicker({
        format: 'Y-m-d H:i',
        step: 30,
        lang: 'pl',
        todayButton: true,
    });
});