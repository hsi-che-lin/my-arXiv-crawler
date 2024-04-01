const paperFile = document.getElementById('paper-file');
const paperContainer = document.getElementById('paper-container');
const paperTitle = document.getElementById('paper-title');
const paperPdf = document.getElementById('paper-pdf');
const paperAbs = document.getElementById('paper-abs');
const ratingValue = document.getElementById('paper-rating');
const paperKeywords = document.getElementById('paper-keywords');
const paperAbstract = document.getElementById('paper-abstract');
const paperSubjects = document.getElementById('paper-subjects');
const paperComments = document.getElementById('paper-comments');
const currentIndexSpan = document.getElementById('current-index');
const totalPapersSpan = document.getElementById('total-papers');
const prevButton = document.getElementById('prev-paper');
const jumpButton = document.getElementById('jump-paper');
const nextButton = document.getElementById('next-paper');

let papers = [];
let currentPaperIndex = 0;

function displayPaper(index) {
    const paper = papers[index];
    if (!paper) return;

    paperTitle.textContent = paper['title'];
    paperPdf.href = `${paper['abstract url']}.pdf#view=FitH`.replace("abs", "pdf");
    paperAbs.href = `${paper['abstract url']}`;
    ratingValue.textContent = `${paper['rating']}`;
    paperKeywords.textContent = `${paper['keywords'].join(', ')}`;
    paperAbstract.textContent = `${paper['abstract']}`;
    paperSubjects.textContent = `${paper['subjects'].join(', ')}`;
    paperComments.textContent = `${paper['comment']}`;
}

function updateNavigation() {
    currentIndexSpan.textContent = currentPaperIndex + 1;
    totalPapersSpan.textContent = papers.length;
    prevButton.disabled = currentPaperIndex === 0;
    nextButton.disabled = currentPaperIndex === papers.length - 1;
}

function selectFile() {
    fetch("/", {
        method: "POST",
        headers: {"Content-Type": "application/json; charset=utf-8"},
        body: JSON.stringify({task: "selectFile", fileName: paperFile.value})
    })
        .then(response => response.json())
        .then(data => {papers = data;})
        .then(() => {
            currentPaperIndex = 0;
            displayPaper(currentPaperIndex);
            updateNavigation();
        })
}

function prevPaper() {
    if (currentPaperIndex > 0) {
        currentPaperIndex--;
        displayPaper(currentPaperIndex);
        updateNavigation();
    }
}

function nextPaper() {
    if (currentPaperIndex < papers.length - 1) {
        currentPaperIndex++;
        displayPaper(currentPaperIndex);
        updateNavigation();
    }
}

function jumpPaper() {
    const newIndex = parseInt(prompt("Enter an index:"));
    if (!isNaN(newIndex)) {
        if (newIndex < 1) {
            currentPaperIndex = 0;
        } else if (newIndex > papers.length) {
            currentPaperIndex = papers.length - 1;
        } else {
            currentPaperIndex = newIndex - 1;
        }
        displayPaper(currentPaperIndex);
        updateNavigation();
    }
}

window.addEventListener('load', selectFile);
paperFile.addEventListener('change', selectFile);
prevButton.addEventListener('click', prevPaper);
nextButton.addEventListener('click', nextPaper);
jumpButton.addEventListener('click', jumpPaper);


// for keyboard shortcut
document.addEventListener("keydown", handleKeyDown);
function handleKeyDown(event) {
    const key = event.key;

    if (key === "ArrowLeft" || key === "h") {
        prevPaper();
    } else if (key === "ArrowRight" || key === "l") {
        nextPaper();
    } else if (key === "/") {
        jumpPaper();
    } else if (key == "s") {
        paperFile.focus();
    } else if (key == "p") {
        window.open(`${papers[currentPaperIndex]['abstract url']}.pdf#view=FitH`.replace("abs", "pdf"), '_blank', 'location=yes,scrollbars=yes,status=yes')
    } else if (key == "n") {
        const data = {
            task: "writeNotes",
            date: paperFile.value.replace(".json", ""),
            title: papers[currentPaperIndex]['title'],
            note: prompt("Enter note here:"),
            url: papers[currentPaperIndex]['abstract url'],
            keywords: papers[currentPaperIndex]['keywords']
        };
        fetch("/", {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(data)
        })
    } else if (key == "t") {
        navigator.clipboard.writeText(papers[currentPaperIndex]['title'])
        alert("title copied");
    } else if (key == "a") {
        navigator.clipboard.writeText(papers[currentPaperIndex]['abstract url'])
        alert("abstract url copied");
    } else if (key == "?") {
        alert("Keyboard shortcuts:\nprevious paper    : left, h\nnext paper           : right, l\nJump to index     : /\nFocus select file   : s\nOpen pdf             : p\nWrite note           : n\nCopy title             : t\nCopy abstract url : a");
    }
}