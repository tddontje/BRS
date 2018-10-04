function saveRecipe() {
    var name = $("#inputName").val();
    var category = $("#inputCategory").val();
    var amt = $("#inputAmount").val()
    var targets = ""
    var ingredients = ""
    var instructions = $("#inputInstructions").val();

    var success_alert = $("#success_alert");

    $.post("/api/recipes", {
                name: name,
                category: category,
                amt: amt,
                targets: targets,
                ingredients: ingredients,
                instructions: instructions}, function(response){
                    console.log(response.id);

                    $(success_alert).find("#success_message").text("Recipe successfully created with ID:" + response.id);
                    $(success_alert).removeClass("hidden");
    });
}
