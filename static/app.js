// console.log("JS WORKING");

// Selections from page

let $loadingMessage = $("#loading-message")
let $main = $("main")
let $submittedGuess = $("#guess-input");
let $guessSubmit = $("#guess-submit");
let $guessResponseMessage = $("#guess-response-message");
let $validWordList = $("#valid-word-list")
let $scoreQuantity = $("#score-quantity")
let $timer = $("#timer")
let $gameOver = $("#game-over")
let $highScore = $("#high-score")
let $highScoreLabel = $("#high-score-label")

let durationSeconds = 60
let validWordList = []
let score = 0

$guessSubmit.on('submit', handleGuessSubmit);

async function handleGuessSubmit(e) {

    e.preventDefault();

    // console.log('Guess Submitted');

    const currentGuess = $submittedGuess.val();

    resp = await requestCheckWord(currentGuess);

    // console.log(resp);

    if (handleCheckWordResponse(resp)){
        addValidWordToList(currentGuess);
        score = validWordList.length;
        showScore(score);
    }

}

async function requestCheckWord(wordToCheck) {

    // console.log(wordToCheck);
    let resp = await axios.get("/check-word", {params: {word : wordToCheck}});
    // console.log(resp);
    return resp.data.result

}

function handleCheckWordResponse(response){

    if (response === 'not-word'){
        // console.log('handling not-word');

        $guessResponseMessage.text('Your guess is not a word.');

        return false
    }

    if (response === 'not-on-board'){
        // console.log('handling not-on-board');

        $guessResponseMessage.text('Your guess is not on the board.');

        return false
    }

    if (response === 'ok'){
        // console.log('handling ok');

        $guessResponseMessage.text('Your guess is valid!');

        return true
    }

}

function addValidWordToList(validWord){

    // console.log(validWord)

    validWordList.push(validWord)
    const validWordHtml = addListHTML(validWord)
    $validWordList.append(validWordHtml)

}

function addListHTML(word) {

    return `<li>${word}</li>`

}

function showScore(score) {

    $scoreQuantity.text(score)

}

function updateHighScore(highScore){

    $highScore.text(highScore)

}

function secondsTimer(duration) {

    const timer = setInterval(async () => {

        duration -= 1;

        updateTimerHtml(duration);

        // console.log(duration);

        if (duration <= 0) {
            clearInterval(timer);
            await postScore(score);
            $guessSubmit.hide();
            $gameOver.show();
            $highScoreLabel.show();
            $highScore.show();
        }

    }, 1000)

}

function updateTimerHtml(duration) {
    $timer.text(duration)
}

async function postScore(score) {

    let resp = await axios.post("/post-score", {score : score});
    // console.log(resp);

    updateHighScore(resp.data.highScore);

}



// Startup -
showScore(score)
secondsTimer(durationSeconds);

$(document).ready($loadingMessage.hide())
$(document).ready($main.show())