console.log("JS WORKING");

// Selections from page

let $submittedGuess = $("#guess-input");
let $guessSubmit = $("#guess-submit");
let $guessResponseMessage = $("#guess-response-message");

// let currentGuess = null;

$guessSubmit.on('submit', handleGuessSubmit);

async function handleGuessSubmit(e) {

    e.preventDefault();

    console.log('Guess Submitted');

    const currentGuess = $submittedGuess.val();

    resp = await checkWord(currentGuess);

    console.log(resp);

    handleCheckWordResponse(resp);

}

async function checkWord(wordToCheck) {

    console.log(wordToCheck);
    let resp = await axios.get("/check-word", {params: {word : wordToCheck}});
    console.log(resp);
    return resp.data.result

}

function handleCheckWordResponse(response){

    if (response === 'not-word'){
        console.log('handling not-word');

        $guessResponseMessage.text('Your guess is not a word.');

    }

    if (response === 'not-on-board'){
        console.log('handling not-on-board');

        $guessResponseMessage.text('Your guess is not on the board.');

    }

    if (response === 'ok'){
        console.log('handling ok');

        $guessResponseMessage.text('Your guess is valid!');

    }

}