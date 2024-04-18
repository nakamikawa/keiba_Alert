async function fetchRaceInfo() {
    const urlInput = document.getElementById("urlInput").value;
    const response = await fetch(`/get_race_info?url=${urlInput}`);
    const data = await response.json();
    displayRaceInfo(data);
}

function displayRaceInfo(data) {
    const raceInfoDiv = document.getElementById("raceInfo");
    raceInfoDiv.innerHTML = "";
    for (const race of data) {
        const raceElement = document.createElement("div");
        raceElement.innerHTML = `<p>R: ${race.r}</p><p>発走時刻: ${race.time}</p><p>レース名: ${race.name}</p><p>内容: ${race.content}</p>`;
        raceInfoDiv.appendChild(raceElement);
    }
}