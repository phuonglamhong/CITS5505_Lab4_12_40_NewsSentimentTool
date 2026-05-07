// Wait until the page is fully loaded before running authentication scripts
document.addEventListener("DOMContentLoaded", () => {
  console.log("AUTH.JS LOADED");

  // Clear messages, errors when switching to [Register] tab
  document.getElementById("register-tab").addEventListener("click", () => {
    document.getElementById("register-error").classList.add("d-none");
    document.getElementById("register-success").classList.add("d-none");
  });

  // Clear messages, errors when switching to [Sign In] tab
  document.getElementById("signin-tab").addEventListener("click", () => {
    document.getElementById("login-error").classList.add("d-none");
  });

  // LOGIN SECTION
  document
    .getElementById("login-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();

      // Get email
      const email = document.getElementById("login-email").value.trim();
      // Get password
      const password = document.getElementById("login-password").value.trim();

      // Make a POST request to /login with the user's email and password as JSON
      const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      // Convert the server response into a usable JavaScript object
      const data = await res.json();

      // If login failed, show error message, else forward to dashboard page
      if (data.status === "error") {
        document.getElementById("login-error").textContent = data.message;
        document.getElementById("login-error").classList.remove("d-none");
      } else {
        // edit later after having route for dashboard
        window.location.href = "/dashboard";
      }
    });

  // REGISTER SECTION
  document
    .getElementById("register-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();

      // User name
      const name = document.getElementById("reg-name").value.trim();
      // User email
      const email = document.getElementById("reg-email").value.trim();
      // User role
      const role = document.getElementById("reg-role").value;
      // User password
      const password = document.getElementById("reg-password").value;
      // User confirm password
      const confirm = document.getElementById("reg-confirm").value;

      // Basic email validation (Fast feedback, prevents obvious mistakes)
      // Regex: matches any non-space characters before and after '@', followed by a dot '.' and domain
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      // If email pattern is not matched, show error message "Please enter a valid email address.".
      if (!emailPattern.test(email)) {
        document.getElementById("register-error").textContent =
          "Please enter a valid email address.";
        document.getElementById("register-error").classList.remove("d-none");
        return;
      }

      // Password length validation with at least 8 characters.
      if (password.length < 8) {
        document.getElementById("register-error").textContent =
          "Password must be at least 8 characters long.";
        document.getElementById("register-error").classList.remove("d-none");
        return;
      }

      // If password and confim password not matched, show error "Passwords do not match."
      if (password !== confirm) {
        document.getElementById("register-error").textContent =
          "Passwords do not match.";
        document.getElementById("register-error").classList.remove("d-none");
        return;
      }

      // Make a POST request to /register with the user's name, email, role and password as JSON
      const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, role, password }),
      });

      // Convert the server response into a usable JavaScript object
      const data = await res.json();

      // If register failed, show error message, else show success message.
      if (data.status === "error") {
        document.getElementById("register-error").textContent = data.message;
        document.getElementById("register-error").classList.remove("d-none");
      } else {
        document.getElementById("register-error").classList.add("d-none");
        document.getElementById("register-success").textContent = data.message;
        document.getElementById("register-success").classList.remove("d-none");

        // Clear the register form
        document.getElementById("register-form").reset();

        // Auto switch to [Sign In] tab after success
        setTimeout(() => {
          document.getElementById("signin-tab").click();
        }, 1200);
      }
    });
});
