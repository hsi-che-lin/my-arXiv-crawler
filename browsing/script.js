const fileInput = document.getElementById('file');
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
let notes = "sep=|\ndate|title|url|note|keywords\n";
let download = "n";

window.addEventListener('load', function (event) {
  setDownload();
});

function setDownload() {
    download = prompt(`Do you want to download notes.csv when closing this browse? (y/n)\n(current value = ${download})`)
}

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    papers = JSON.parse(event.target.result);
    currentPaperIndex = 0;
    displayPaper(currentPaperIndex);
    updateNavigation();
  };
  reader.readAsText(file);
});

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

prevButton.addEventListener('click', () => {
  if (currentPaperIndex > 0) {
    currentPaperIndex--;
    displayPaper(currentPaperIndex);
    updateNavigation();
  }
});

jumpButton.addEventListener('click', () => {
    currentPaperIndex = parseInt(prompt("Enter an index:")) - 1;
    displayPaper(currentPaperIndex);
    updateNavigation();
});

nextButton.addEventListener('click', () => {
  if (currentPaperIndex < papers.length - 1) {
    currentPaperIndex++;
    displayPaper(currentPaperIndex);
    updateNavigation();
  }
});

// for keyboard shortcut
document.addEventListener("keydown", handleKeyDown);
function handleKeyDown(event) {
  const key = event.key;

  if (key === "ArrowLeft" || key === "h") {
    if (currentPaperIndex > 0) {
        currentPaperIndex--;
        displayPaper(currentPaperIndex);
        updateNavigation();
    }
  } else if (key === "ArrowRight" || key === "l") {
    if (currentPaperIndex < papers.length - 1) {
        currentPaperIndex++;
        displayPaper(currentPaperIndex);
        updateNavigation();
    }
  } else if (key === "/") {
    currentPaperIndex = parseInt(prompt("Enter an index:")) - 1;
    displayPaper(currentPaperIndex);
    updateNavigation();
  } else if (key == "p") {
    window.open(`${papers[currentPaperIndex]['abstract url']}.pdf#view=FitH`.replace("abs", "pdf"), '_blank', 'location=yes,scrollbars=yes,status=yes')
  } else if (key == "n") {
    const date = fileInput.files[0].name.replace(".json", "");
    const title = papers[currentPaperIndex]['title'];
    const url = papers[currentPaperIndex]['abstract url'];
    const keywords = papers[currentPaperIndex]['keywords'].join(', ');
    const note = prompt("Enter note here:");
    notes = notes.concat(`${date}|${title}|${url}|${note}|${keywords}\n`)
  } else if (key == "t") {
    navigator.clipboard.writeText(papers[currentPaperIndex]['title'])
    alert("title copied");
  } else if (key == "a") {
    navigator.clipboard.writeText(papers[currentPaperIndex]['abstract url'])
    alert("abstract url copied");
  } else if (key == "d") {
    setDownload();
  } else if (key == "?") {
    alert("Keyboard shortcuts:\nprevious paper    : left, h\nnext paper           : right, l\nJump to index     : /\nOpen pdf             : p\nWrite note           : n\nCopy title             : t\nCopy abstract url : a\nSet download      : d");
  }
}

window.addEventListener('beforeunload', function (event) {
  if (download == "y") {
    const blob = new Blob([notes], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = "notes.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
});