const $form = $("#boggle-form");
const $word = $("#word");
const $resultField = $(".result");
const $timer = $("#timer");
const $hiScore = $('#hi-score');

class Game {
    constructor(start = 60){
        this.start = start;
        this.cntDwnTimer();
        this.repeatWords = new Set();
        this.score = 0;
        
        $form.on('submit', this.submitHandler.bind(this));
    }

    async submitHandler(evt){
        evt.preventDefault();
        const userWord = $word.val();

        if(this.repeatWords.has(userWord)){
            $word.val('');
            return $resultField.html('<b>Already Guessed</b>');
        }

        this.repeatWords.add(userWord);

        // axios post request to flask server, checks
        // if word is on boggle-board and responds with result
        const res = await axios({
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
            this.scoreKeeper(userWord);
        }

        $word.val('');
        return $resultField.html(result);
    }

    /** track score */
    scoreKeeper(word){
    this.score += word.length;
    $("#score").html(this.score);

    return;
    }

    /* Countdown Timer */
    cntDwnTimer(){
    const stopCntr = setInterval(()=>{
        $timer.html(this.start);
        this.start--;
        
        // Ends timer and displays "Game Over" when timer
        // reaches 0. Also calls statistics(score) to 
        // determine if new hi-score
        if(this.start < 0){
            clearInterval(stopCntr);
            $timer.html("<b>Time's Up!</b>");
            $word.attr("disabled", true);
            $resultField.html("<b>Game Over</b>");
            this.statistics();
            return;
        }
    }, 1000, this.start);


    }
    /** statistics() - Store statistics
     * 
     * Store high score
     */
    async statistics() {
    const res = await axios({
        method: 'post',
        url: '/store-statistics',
        data: {
            'score': this.score,
        }
    })

    $hiScore.html = res.data;
    }
}

let boggleGame = new Game(start=60);