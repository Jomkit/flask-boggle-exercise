const $form = $("#boggle-form");
const $word = $("#word");
const $resultField = $(".result");
const $timer = $("#timer");
let score = 0;

async function submitHandler(evt){
    evt.preventDefault();
    
    // axios post request to flask server, checks
    // if word is on boggle-board and responds with result
    res = await axios({
        method: 'post',
        url: '/check-word',
        data: {
            'word': $word.val()
        }
    })
    
    $resultField.html('');
    const result = res.data;

    // result == 'ok', update score
    if(result=='ok'){
        scoreKeeper($word.val());
    }
    
    $word.val('');
    return $resultField.html(result);
}
$form.on('submit', submitHandler);

/** track score */
function scoreKeeper(word){
    score += word.length;
    $("#score").html(score);

    return;
}

/* Countdown Timer */
function cntDwnTimer(start = 60){
    const stop = setInterval(()=>{
        $timer.html(start);
        start--;
        
        if(start < 50){
            clearInterval(stop);
            $timer.html("<b>Time's Up!</b>");
            $word.attr("disabled", true);
            return;
        }
    }, 1000, start);

    
}

cntDwnTimer();
