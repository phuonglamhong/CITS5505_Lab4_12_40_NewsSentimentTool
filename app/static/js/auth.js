// AUTH.JS — Flask‑WTF native forms
document.addEventListener("DOMContentLoaded", () => {
  console.log("AUTH.JS LOADED");

  // Clear ONLY errors when switching to Register tab
  document.getElementById("register-tab").addEventListener("click", () => {
    const err = document.getElementById("register-error");
    if (err) err.classList.add("d-none");
  });

  // Clear ONLY errors when switching to Sign In tab
  document.getElementById("signin-tab").addEventListener("click", () => {
    const err = document.getElementById("login-error");
    if (err) err.classList.add("d-none");
  });

  // Auto-switch to Sign In AFTER success message is visible
  const successMsg = document.getElementById("register-success");

  if (successMsg) {
    requestAnimationFrame(() => {
      setTimeout(() => {
        document.getElementById("signin-tab").click();
      }, 1500);
    });
  }
});
