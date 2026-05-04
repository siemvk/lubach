const lubachSearch = fetch("data.json").then((res) => res.json());
const { Fzf } = window.fzf;

const isTheYtdlpServerRunning = fetch("http://localhost:8080/health").then((res) => res.ok).catch(() => false);

function turnTimeToSeconds(time) {
    const parts = time.split(":").map(Number);
    const [hours = 0, minutes = 0, seconds = 0] =
        parts.length === 2 ? [0, ...parts] : parts;
    return String(hours * 3600 + minutes * 60 + seconds).split(".")[0];
}

lubachSearch.then((data) => {
    const fzf = new Fzf(data, {
        // With selector you tell FZF where it can find
        // the string that you want to query on
        selector: (item) => item.text,
    });
    const searchInput = document.getElementById("search-input");
    const resultsContainer = document.getElementById("results-container");

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
        const results = fzf.find(query).map((result) => result.item);
        displayResults(results, query);
    });

    function displayResults(results, query) {
        console.log(isTheYtdlpServerRunning);
        resultsContainer.innerHTML = "";
        results = results.slice(0, 40); // Limit to top 10 results
        results.forEach((result) => {
            if (!result.text.toLowerCase().includes(query)) {
                return;
            }
            const resultElement = document.createElement("div");
            resultElement.classList.add("result");
            // https://youtu.be/xpedFIZFmhc?t=30
            resultElement.innerHTML = `
            ${result.text} ${"  -   "} <a href="https://www.youtube.com/watch?v=${result.video}&t=${turnTimeToSeconds(result.start)}" target="_blank">Bekijk op YouTube</a>
      `;
            resultsContainer.appendChild(resultElement);
        });
    }
});