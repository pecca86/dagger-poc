const reader = new FileReader();

hasMoreText = false;
currentDiv = null;
randomNumber = 0;

function watchfileInput(files) {
    if (files.length) {
        const file = files[0];
        if (file) {
            contents = null;
            // file = "static/demo_log.log"
            const reader = new FileReader();
            reader.onload = function () {
                contents = this.result;
                parseContents(contents);
            };
            reader.readAsText(file);
            var info = "File uploaded (`" + file.name + "`)";
            console.log(info);

            // dialog = extraction(contents);
        }
    }
}

function parseContents(file_contents) {
    let text_paragraph = document.querySelector("#text");

    // create a new paragraph
    let createParagraph = document.createElement("p");
    // put the paragraph into the div with id chat
    let targetDiv = document.getElementById("chat-window");

    // split the file_contents into an array of lines
    let lines = file_contents.split("\n");

    // loop through each line
    for (let i = 0; i < lines.length; i++) {
        // create a new paragraph for each line
        // let lineParagraph = document.createElement("p");
        checkLine(lines[i], targetDiv);
        // set the text content of the paragraph to the line
        // lineParagraph.textContent = lines[i];
        // append the line paragraph to the target div
        // targetDiv.appendChild(lineParagraph);
    }
}



// hasMoreText = false;
// currentDiv = null;
// randomNumber = 0;
function checkLine(line, targetDiv) {
    let lineParagraph = document.createElement("p");
    // targetDiv.appendChild(lineParagraph);
    // IDEA: create a dictionary for the messages...
    const phaseRegex = /^\[.*\] \*\*.*\*\*$/; // [text] ** text **
    const lineRegex = /^\[.*\] \[.*\]: .*/; // [text] [text]: text
    const systemMessageRegex = /^\[.*\]/; // [text]

    // start of a new phase
    if (phaseRegex.test(line)) {
        // add a style of yellow background to the paragraph
        lineParagraph.classList.add("phase");
        lineParagraph.textContent = line;
        targetDiv.appendChild(lineParagraph);
    }

    // Start of a new message
    if (lineRegex.test(line)) {
        // we might have more text to add to this message
        hasMoreText = true;
        this.randomNumber = Math.floor(Math.random() * 10000);
        // create a new div for the message
        let newDiv = document.createElement("div");
        classNameWithRandomNumber = "message-body-" + randomNumber;
        newDiv.classList.add(classNameWithRandomNumber);
        newDiv.appendChild(lineParagraph);


        lineParagraph.classList.add("message");
        lineParagraph.textContent = line;
        targetDiv.appendChild(lineParagraph);
    }

    // Continuation of a message
    if (!lineRegex.test(line) && !phaseRegex.test(line) && !systemMessageRegex.test(line)) {
        // check if line is empty
        if (line !== "") {
            lineParagraph.textContent = line;
            // let newDiv = document.createElement("div");
            // randomNumber = Math.floor(Math.random() * 10000);
            // classNameWithRandomNumber = "message-body-" + randomNumber;
            // newDiv.classList.add(classNameWithRandomNumber);
            // newDiv.appendChild(lineParagraph);
            // targetDiv.appendChild(newDiv);
            targetDiv.appendChild(lineParagraph);
            let i = 0;
            let speed = 20;
            // typeWriter();
            function typeWriter() {
                if (i < line.length) {
                    lineParagraph.textContent += line.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            }
        }
    }

    if (systemMessageRegex.test(line) && !phaseRegex.test(line) && !lineRegex.test(line)) {
        lineParagraph.classList.add("system");
        lineParagraph.textContent = line;
        targetDiv.appendChild(lineParagraph);
    }

}

