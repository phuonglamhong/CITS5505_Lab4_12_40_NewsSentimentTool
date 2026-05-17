// AUTH.JS - Handles UI behavior for authentication page (Flask-WTF forms)
document.addEventListener("DOMContentLoaded", () => {
  console.log("AUTH.JS LOADED");

  // When user switches between Register and Sign In tabs,
  // we clear only the relevant error messages to avoid stale UI feedback.

  // Clear register-related error when user opens Register tab
  document.getElementById("register-tab").addEventListener("click", () => {
    const err = document.getElementById("register-error");
    if (err) err.classList.add("d-none");
  });

  // Clear login-related error when user opens Sign In tab
  document.getElementById("signin-tab").addEventListener("click", () => {
    const err = document.getElementById("login-error");
    if (err) err.classList.add("d-none");
  });

  // Auto-switch to Sign In AFTER register success is visible
  const successMsg = document.getElementById("register-success");

  if (successMsg && successMsg.textContent.trim()) {
    // Wait for DOM paint + small delay for better UX transition
    requestAnimationFrame(() => {
      setTimeout(() => {
        document.getElementById("signin-tab").click();
      }, 1500);
    });
  }
});
