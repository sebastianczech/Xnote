$(document).ready(function(){

    $(".chip").click(function() {
        var reminder_group_id = this.id.split("_")[2];
        console.log("filter reminders by group " + reminder_group_id);
        window.location.href = "/reminder/" + reminder_group_id;
    });

});