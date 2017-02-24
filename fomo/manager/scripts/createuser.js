
$(function(){

  console.log('hey');
  $('#id_birthdate').datetimepicker({
      timepicker:false,
      format:'Y-m-d'
    });
  $('#id_cc_exp_date').datetimepicker({
        timepicker:false,
        format:'Y-m-d'
    });

});
