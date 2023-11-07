const $form = $("#boggle-form");
const $word = $("#word");
const $resultField = $(".result");
const $timer = $("#timer");
const $hiScore = $('#hi-score');
const stop = 0;
let repeatWords = [];

let score = 0;

async function submitHandler(evt){
    evt.preventDefault();
    const userWord = $word.val();
    
    if(repeatWords.includes(userWord)){
        $word.val('');
        return $resultField.html('<b>Already Guessed</b>');
    }

    repeatWords.push(userWord);
    
    // axios post request to flask server, checks
    // if word is on boggle-board and responds with result
    res = await axios({
        method: 'post',
        url: '/check-word',
        data: {
            'word': userWord
        }
    })
    
    $resultField.html('');
    const result = res.data;

    // result == 'ok', update score
    if(result=='ok'){
        scoreKeeper(userWord);
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
    const stopCntr = setInterval(()=>{
        $timer.html(start);
        start--;
        
        // Ends timer and displays "Game Over" when timer
        // reaches 0. Also calls statistics(score) to 
        // determine if new hi-score
        if(start < stop){
            clearInterval(stopCntr);
            $timer.html("<b>Time's Up!</b>");
            $word.attr("disabled", true);
            $resultField.html("<b>Game Over</b>");
            statistics(score);
            return;
        }
    }, 1000, start);

    
}

cntDwnTimer();

/** statistics() - Store statistics
 * 
 * Store high score
 */
async function statistics(score) {
    const res = await axios({
        method: 'post',
        url: '/store-statistics',
        data: {
            'score': score,
        }
    })

    $hiScore.html = res.data;
}