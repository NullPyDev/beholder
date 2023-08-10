let httpRequest;
let dashboardContentElement = document.getElementById("dashboard");
let refreshIntervalId = window.setInterval(refreshDashboard, 10000);

function refreshDashboard() {
    httpRequest = new XMLHttpRequest();
    if (!httpRequest) {
        console.log("It was not possible to prepare a request to refresh the dashboard content.");
        return;
    }

    httpRequest.onreadystatechange = updateDashboardContent;
    httpRequest.open("GET", "/?template=dashboard", true);
    httpRequest.send();
}

function updateDashboardContent() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
        if (httpRequest.status === 200) {
            dashboardContentElement.innerHTML = httpRequest.responseText;
            new Masonry(dashboardContentElement, { itemSelector: ".widget", percentPosition: true });
        } else {
            console.log("It was not possible to update the dashboard: " + httpRequest.status);
        }
    }
}
