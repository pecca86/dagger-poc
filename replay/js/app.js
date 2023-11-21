const reader = new FileReader();

randomNumber = 0;
currentDiv = null;
isCode = false;

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
            let info = "File uploaded (`" + file.name + "`)";
            console.log(info);
        }
    }
}

function parseContents(file_contents) {
    // put the paragraph into the div with id chat
    let targetDiv = document.getElementById("chat-window");

    // split the file_contents into an array of lines
    let lines = file_contents.split("\n");

    // function loopWithDelay() {
    //     // Assuming 'lines' is your array
    //     for (let i = 0; i < lines.length; i++) {
    //         setTimeout(function () {
    //             checkLine(lines[i], targetDiv);
    //         }, i * 1); // 1 = Pause for 1 millisecond
    //     }
    // }

    async function loopWithDelay() {
        for (let i = 0; i < lines.length; i++) {
            checkLine(lines[i], targetDiv);
            await new Promise(resolve => setTimeout(resolve, 500))// 500 = Pause for 0.5 seconds
        }
    }
    loopWithDelay();
}


function checkLine(line, targetDiv) {
    let lineParagraph = document.createElement("p");
    const phaseRegex = /^\[.*\] \*\*.*\*\*$/; // [text] ** text **
    const lineRegex = /^\[.*\] \[.*\]: .*/; // [text] [text]: text
    const systemMessageRegex = /^\[.*\]/; // [text]

    // start of a new phase
    if (phaseRegex.test(line)) {
        lineParagraph.classList.add("phase");
        lineParagraph.textContent = line;
        targetDiv.appendChild(lineParagraph);
        lineParagraph.scrollIntoView({ behavior: 'smooth' });
    }

    // Start of a new message
    if (lineRegex.test(line)) {
        // we might have more text to add to this message
        this.randomNumber = Math.floor(Math.random() * 10000);

        // separate the header from the message [timestamp] [agent name]
        let headerText = line.match(systemMessageRegex)[0];
        let cleanedLine = line.replace(headerText + ':', "");

        // get the agent name, so we can select with image to use
        headerElements = headerText.split(" ");
        agent_name = headerElements[3].replace("[", "").replace("]", "");
        let agentImage = document.createElement("img");
        agentImage.classList.add("agent-image");
        agentImage.src = "static/" + agent_name + ".png";

        // add content to the paragraph
        headerParagraph = document.createElement("p");
        headerParagraph.classList.add("header-paragraph");
        headerParagraph.textContent = headerText;

        // add a paragraph for the message which contains of the text without the header
        lineParagraph.classList.add("message");
        lineParagraph.textContent = cleanedLine;

        // create a new div for the message and give it a unique class name, then append it to the parent div
        let newDiv = document.createElement("div");
        classNameWithRandomNumber = "message-body-" + randomNumber;
        newDiv.classList.add(classNameWithRandomNumber);
        this.currentDiv = newDiv;

        newDiv.appendChild(agentImage);
        newDiv.appendChild(headerParagraph);
        newDiv.appendChild(lineParagraph);
        // add a border to the div
        newDiv.classList.add("message-border");
        targetDiv.appendChild(newDiv);
        // Scroll to the new paragraph
        lineParagraph.scrollIntoView({ behavior: 'smooth' });
    }

    // Continuation of a message
    // TODO: Check for code snippet and style that differently
    if (!lineRegex.test(line) && !phaseRegex.test(line) && !systemMessageRegex.test(line)) {
        // check if line has content
        if (line !== "") {
            if (this.isCode) {
                lineParagraph.classList.add("code");
                lineParagraph.textContent = line;
                if (line.includes("```")) {
                    this.isCode = false;
                }
            } else if (line.includes("```")) {
                this.isCode = true;
                lineParagraph.classList.add("code");
                lineParagraph.textContent = line;
            } else {
                lineParagraph.classList.add("message");
                lineParagraph.textContent = line;
            }
            this.currentDiv.appendChild(lineParagraph);
            targetDiv.appendChild(currentDiv);
            lineParagraph.scrollIntoView({ behavior: 'smooth' });
        }
    }

    if (systemMessageRegex.test(line) && !phaseRegex.test(line) && !lineRegex.test(line)) {
        lineParagraph.classList.add("system");
        lineParagraph.textContent = line;
        targetDiv.appendChild(lineParagraph);
        lineParagraph.scrollIntoView({ behavior: 'smooth' });
    }

}