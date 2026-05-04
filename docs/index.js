const { Fzf } = window.fzf;

const itemSet = {};
let fzf = undefined;
let downloadServerOnline = false;

function turnTimeToSeconds(time) {
    const parts = time.split(":").map(Number);
    const [hours = 0, minutes = 0, seconds = 0] =
        parts.length === 2 ? [0, ...parts] : parts;
    return String(hours * 3600 + minutes * 60 + seconds).split(".")[0];
}
async function main() {
    try {
        downloadServerOnline = await fetch("http://localhost:8080/health").then(res => res.text()).then(text => text.includes("OK"));
    } catch (error) {
        downloadServerOnline = false;
    }

    const dropdown = document.getElementById("dropdown");
    const config = await fetch("./config.json").then(res => res.json());
    for (const item of config) {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item.name;
        dropdown.appendChild(option);
        itemSet[item.id] = await fetch(item.file).then(res => res.json());
    }
    updateFzf();
}
document.getElementById("dropdown").addEventListener("change", updateFzf);
document.getElementById("search-input").addEventListener("input", render);
function updateFzf() {
    const selected = document.getElementById("dropdown").value;
    const items = itemSet[selected];
    fzf = new Fzf(items, {
        selector: item => item.text || ""
    });
    // we update tha info
    const element = document.getElementById("info");
    element.innerText = element.getAttribute("og").replace("x", items.length).replace("y", downloadServerOnline ? "online" : "offline");
    render();
}

function render() {
    const container = document.getElementById("results-container");
    const selected = document.getElementById("dropdown").value;
    const items = itemSet[selected];
    container.innerHTML = "";
    const search = document.getElementById("search-input").value.toLowerCase();

    let results = fzf.find(search).map((result) => result.item);
    results = results.slice(0, 40);
    results.forEach((result) => {
        if (!result.text.toLowerCase().includes(search)) {
            return;
        }
        const resultElement = document.createElement("div");
        resultElement.classList.add("result");
        // https://youtu.be/xpedFIZFmhc?t=30
        resultElement.innerHTML = `
                        ${result.text} ${"  -   "} <a href="https://www.youtube.com/watch?v=${result.video}&t=${turnTimeToSeconds(result.start)}" target="_blank">Bekijk op YouTube</a>
                        ${downloadServerOnline ? `${"  -   "} <a href="http://localhost:8080/download/${result.video}/${turnTimeToSeconds(result.start)}/${turnTimeToSeconds(result.end)}" target="_blank">Video</a> ${"  -   "} <a href="http://localhost:8080/download/${result.video}/${turnTimeToSeconds(result.start)}/${turnTimeToSeconds(result.end)}" target="_blank">Audio</a>` : ""}
            `;
        container.appendChild(resultElement);
    });

}

main();