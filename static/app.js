const $form = $("#boggle-form");

$form.on('submit', eventHandler);

function eventHandler(evt){
    evt.preventDefault();

    return alert('hi!');
}

