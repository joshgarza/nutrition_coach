$(function() {
    
   goals_callback = function(goals) {
      $("#goals-table").html('<tr>' + '<td>' + goals.protein + '</td>' + '<td>' + goals.carbs + '</td>' + '<td>' + goals.fat + '</td>' + '<td>' + goals.calories + '</td>' + '</tr>'); 
   }

   getJsonFromServer('/goals', goals_callback);
   
   
   macros_callback = function(response) {
      alert("Saved!");
   }
   
   $("#macros-form").submit(function(e){
	   e.preventDefault();
      macros_form = {'protein': $("input[name=protein]").val(), 'carbs': $("input[name=carbs]").val(), 'fat': $("input[name=fat]").val()};
      sendToServer("/macros", macros_form, macros_callback);
      getJsonFromServer('/goals', goals_callback);
    });

});