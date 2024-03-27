const fileInput = document.getElementById('file');
const paperContainer = document.getElementById('paper-container');
const paperTitle = document.getElementById('paper-title');
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

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    papers = JSON.parse(event.target.result);
    displayPaper(currentPaperIndex);
    updateNavigation();
  };
  reader.readAsText(file);
});

function displayPaper(index) {
  const paper = papers[index];
  if (!paper) return;

  paperTitle.textContent = paper['title'];
  paperTitle.href = `${paper['abstract url']}.pdf`.replace("abs", "pdf");
  ratingValue.textContent = `${paper['rating']}`;
  paperKeywords.textContent = `${paper['keywords'].join(', ')}`;
  paperAbstract.textContent = `${paper['abstract']}`;
  paperSubjects.textContent = `${paper['subjects'].join(', ')}`;
  paperComments.textContent = `${paper['comments']}`;
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
  } else if (key == "Enter") {
    window.open(`${papers[currentPaperIndex]['abstract url']}.pdf`.replace("abs", "pdf"), '_blank', 'location=yes,scrollbars=yes,status=yes')
  }
}
