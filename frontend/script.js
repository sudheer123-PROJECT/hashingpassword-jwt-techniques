const API_URL = "http://127.0.0.1:8000";


// Display message on page
function showMessage(message) {
    const element = document.getElementById("message");

    if (element) {
        element.textContent = message;
    }
}


// Get error message from FastAPI
function getErrorMessage(data) {
    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (Array.isArray(data.detail)) {
        return data.detail
            .map(error => error.msg)
            .join(", ");
    }

    return "Something went wrong";
}


// REGISTER
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                showMessage("Registration successful! Redirecting...");

                window.location.href = "login.html";
            } else {
                showMessage(getErrorMessage(data));
            }

        } catch (error) {
            showMessage("Cannot connect to backend");
        }
    });
}


// LOGIN
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                sessionStorage.setItem(
                    "access_token",
                    data.access_token
                );

                window.location.href = "profile.html";
            } else {
                showMessage(getErrorMessage(data));
            }

        } catch (error) {
            showMessage("Cannot connect to backend");
        }
    });
}


// Get saved JWT token
function getToken() {
    return sessionStorage.getItem("access_token");
}


// Clear token and redirect
function logout() {
    sessionStorage.removeItem("access_token");
    window.location.href = "login.html";
}


// Send authenticated API request
async function authenticatedFetch(path, options = {}) {
    const token = getToken();

    if (!token) {
        logout();
        return null;
    }

    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            ...options.headers,
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        logout();
        return null;
    }

    return response;
}


// LOAD PROFILE
async function loadProfile() {
    try {
        const response = await authenticatedFetch("/profile");

        if (!response) return;

        const data = await response.json();

        if (response.ok) {
            document.getElementById("userId").textContent = data.id;
            document.getElementById("profileName").textContent = data.username;
            document.getElementById("profileEmail").textContent = data.email;
            document.getElementById("newUsername").value = data.username;
        } else {
            showMessage(getErrorMessage(data));
        }

    } catch (error) {
        showMessage("Failed to load profile");
    }
}


// PROFILE PAGE
const updateForm = document.getElementById("updateForm");

if (updateForm) {

    loadProfile();

    updateForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("newUsername").value;

        try {
            const response = await authenticatedFetch("/profile", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username
                })
            });

            if (!response) return;

            const data = await response.json();

            if (response.ok) {
                showMessage("Profile updated successfully");
                document.getElementById("profileName").textContent = data.username;
            } else {
                showMessage(getErrorMessage(data));
            }

        } catch (error) {
            showMessage("Failed to update profile");
        }
    });
}


// DASHBOARD BUTTON
const dashboardBtn = document.getElementById("dashboardBtn");

if (dashboardBtn) {
    dashboardBtn.addEventListener("click", async function () {
        try {
            const response = await authenticatedFetch("/dashboard");

            if (!response) return;

            const data = await response.json();

            if (response.ok) {
                showMessage(data.message);
            } else {
                showMessage(getErrorMessage(data));
            }

        } catch (error) {
            showMessage("Dashboard request failed");
        }
    });
}


// LOGOUT BUTTON
const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
}