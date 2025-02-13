document.getElementById("moveBtn").addEventListener("click", function() {
    fetch("/action/move", { method: "POST" })
        .then(response => response.json())
        .then(data => console.log(data));
    window.location.href = "#";
});

document.getElementById("streamBtn").addEventListener("click", function() {
    fetch("/action/stream", { method: "POST" })
        .then(response => response.json())
        .then(data => console.log(data));

    window.location.href = "stream.html";
});

document.getElementById("settingsBtn").addEventListener("click", function() {
    fetch("/action/settings", { method: "POST" })
        .then(response => response.json())
        .then(data => console.log(data));

    window.location.href = "settings.html";
});
