$(document).ready(function boxes() {
    var counter = 2;
    var counterN = counter - 1;
    var names = [];

    $("#addButton").click(function () {

        if (counter > 10) {
            alert("Only 10 names allowed");
            return false;
        }

        if (counter > 1) {
            names.push($('#textbox' + counterN).val());
        }
        counterN++;
        console.log(names);


        var newTextBoxDiv = $(document.createElement('div'))
            .attr("id", 'TextBoxDiv' + counter);

        newTextBoxDiv.after().html('<label>Name #' + counter + ' : </label>' +
            '<input type="text" name="textbox' + counter +
            '" id="textbox' + counter + '" value="" >');

        newTextBoxDiv.appendTo("#TextBoxesGroup");


        counter++;
    });

    $("#removeButton").click(function () {
        if (counter == 1) {
            alert("No more names to remove");
            return false;
        }

        counter--;

        $("#TextBoxDiv" + counter).remove();

        if (counter - names.length == 0) {
            names.pop();
        }
        counterN--;
        console.log(names);

    });

    $('#submit').click(function () {
        names.push($('#textbox' + counterN).val());
        counterN++;
        console.log(names);
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: "/post_article",
            traditional: "true",
            data: JSON.stringify({
                names
            }),
            dataType: "json"
        });
    });

});