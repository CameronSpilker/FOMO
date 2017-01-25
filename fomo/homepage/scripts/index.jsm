
$(function() {
    // update the time every n seconds
    window.setInterval(function() {
        $('.browser-time').text('The current browser time is ' + new Date());
    }, ${ request.urlparams[1] if request.urlparams[1] else '1000'});

    // update server time button
    // update button
    $('#server-time-button').click(function() {
        $('.server-time').load('/homepage/index.time');
    });
});
