function closeAllAlerts() {
	const alerts = document.querySelectorAll(".alert");
	alerts.forEach((alertNode) => {
		new bootstrap.Alert(alertNode).close();
	});
}

document.addEventListener("DOMContentLoaded", () => {
	setTimeout(closeAllAlerts, 5000); // 5000 milliseconds = 5 seconds
});