async function fetchRaceInfo() {
    try {
        const urlInput = document.getElementById("urlInput").value;
        const response = await fetch(`/get_race_info?url=${urlInput}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        displayRaceInfo(data);
    } catch (error) {
        console.error('Error fetching race info:', error.message);
    }
}

function displayRaceInfo(data) {
    try {
        const raceInfoDiv = document.getElementById("raceInfo");
        raceInfoDiv.innerHTML = "";
        for (const race of data) {
            const raceElement = document.createElement("div");
            raceElement.innerHTML = `<p>R: ${race.r}</p><p>発走時刻: ${race.time}</p><p>レース名: ${race.name}</p><p>内容: ${race.content}</p>`;
            raceInfoDiv.appendChild(raceElement);
        }
    } catch (error) {
        console.error('Error displaying race info:', error.message);
    }
}
