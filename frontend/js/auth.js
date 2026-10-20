/**
 * ScholarTrack — Authentication Frontend
 * File: frontend/js/auth.js
 *
 * Handles:
 * - Login form validation
 * - Signup form validation
 * - Password visibility
 * - Password strength indicator
 * - User-friendly error messages
 * - Flask backend integration
 *
 * Security:
 * - Never stores passwords in localStorage.
 * - Never treats frontend validation as authentication.
 * - Actual authentication must happen on the Flask backend.
 */

(() => {
    "use strict";

    // =====================================================
    // CONFIGURATION
    // =====================================================

    const CONFIG = {
        API_BASE_URL: (typeof window !== "undefined" && window.location.port === "5000")
            ? "/api"
            : (typeof window !== "undefined" && window.location.hostname)
                ? `${window.location.protocol}//${window.location.hostname}:5000/api`
                : "http://127.0.0.1:5000/api",

        LOGIN_ENDPOINT: "/auth/login",
        REGISTER_ENDPOINT: "/auth/register",
        FORGOT_PASSWORD_ENDPOINT: "/auth/forgot-password",
        REQUEST_TIMEOUT: 15000
    };


    // =====================================================
    // SHARED UTILITIES
    // =====================================================

    /**
     * Find an element by its ID.
     */
    function getElement(id) {
        return document.getElementById(id);
    }


    /**
     * Display a form message.
     */
    function showMessage(element, message, type = "error") {
        if (!element) return;

        element.textContent = message;
        element.className = `auth-message show ${type}`;

        // Support the signup message styling as well.
        if (element.id === "signupMessage") {
            element.className = `signup-message show ${type}`;
        }
    }


    /**
     * Clear a form message.
     */
    function clearMessage(element) {
        if (!element) return;

        element.textContent = "";

        element.className =
            element.id === "signupMessage"
                ? "signup-message"
                : "auth-message";
    }


    /**
     * Display a field validation error.
     */
    function markInvalid(field) {
        if (!field) return;

        field.classList.add("is-invalid");
        field.setAttribute("aria-invalid", "true");
    }


    /**
     * Remove a field validation error.
     */
    function clearInvalid(field) {
        if (!field) return;

        field.classList.remove("is-invalid");
        field.removeAttribute("aria-invalid");
    }


    /**
     * Basic email validation.
     *
     * The backend must independently validate the email.
     */
    function isValidEmail(email) {
        const value = String(email || "").trim();

        return (
            value.length <= 254 &&
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
        );
    }


    /**
     * Set the submit button loading state.
     */
    function setButtonLoading(button, labelElement, loading, defaultText) {
        if (!button) return;

        button.disabled = loading;
        button.setAttribute("aria-busy", String(loading));

        if (labelElement) {
            labelElement.textContent = loading
                ? "Please wait..."
                : defaultText;
        }
    }


    /**
     * Make a request to the Flask backend.
     *
     * credentials: include allows the browser to send
     * and receive session cookies.
     *
     * The backend must configure secure session handling,
     * CSRF protection, and appropriate CORS settings.
     */
    async function apiRequest(endpoint, payload) {
        const controller = new AbortController();

        const timeoutId = window.setTimeout(() => {
            controller.abort();
        }, CONFIG.REQUEST_TIMEOUT);

        try {
            const response = await fetch(
                `${CONFIG.API_BASE_URL}${endpoint}`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "include",

                    signal: controller.signal,

                    body: JSON.stringify(payload)
                }
            );

            let result = {};

            try {
                result = await response.json();
            } catch {
                result = {};
            }

            if (!response.ok) {
                const error = new Error(
                    result.message ||
                    result.error ||
                    "The request could not be completed."
                );

                error.status = response.status;

                throw error;
            }

            return result;

        } catch (error) {
            if (error.name === "AbortError") {
                throw new Error(
                    "The request timed out. Please try again."
                );
            }

            if (error instanceof TypeError) {
                throw new Error(
                    "Cannot connect to the server. Check whether the Flask backend is running."
                );
            }

            throw error;

        } finally {
            window.clearTimeout(timeoutId);
        }
    }


    /**
     * Convert server errors into user-friendly messages.
     */
    function getFriendlyError(error, action) {
        if (error.status === 400) {
            return error.message || "Please check the information you entered.";
        }

        if (error.status === 401) {
            return action === "login"
                ? "Invalid email or password."
                : "Your request could not be authenticated.";
        }

        if (error.status === 403) {
            return "This action is not permitted. Please refresh and try again.";
        }

        if (error.status === 409) {
            return "An account with this email may already exist.";
        }

        if (error.status === 429) {
            return "Too many attempts. Please wait before trying again.";
        }

        if (error.status >= 500) {
            return "A server error occurred. Please try again later.";
        }

        return error.message || "Something went wrong. Please try again.";
    }


    // =====================================================
    // PASSWORD VISIBILITY
    // =====================================================

    /**
     * Supports both login and signup password buttons.
     *
     * Login HTML:
     * #togglePassword
     *
     * Signup HTML:
     * [data-toggle-password="password"]
     * [data-toggle-password="confirmPassword"]
     */
    function initializePasswordVisibility() {
        const buttons = document.querySelectorAll(
            "#togglePassword, #toggleConfirmPassword, [data-toggle-password], .auth-password-toggle, .signup-password-toggle"
        );

        buttons.forEach((button) => {
            if (button.dataset.authInitialized === "true") {
                return;
            }

            button.dataset.authInitialized = "true";

            button.addEventListener("click", () => {
                let fieldId = button.dataset.togglePassword;

                if (!fieldId && button.id === "togglePassword") {
                    fieldId = "password";
                }

                if (!fieldId && button.id === "toggleConfirmPassword") {
                    fieldId = "confirmPassword";
                }

                if (!fieldId) {
                    const parentWrapper = button.closest(".auth-input-wrapper, .signup-input-wrapper");
                    const input = parentWrapper ? parentWrapper.querySelector("input") : null;
                    if (input && input.id) {
                        fieldId = input.id;
                    }
                }

                const field = getElement(fieldId);

                if (!field) return;

                const showPassword = field.type === "password";

                field.type = showPassword ? "text" : "password";

                const icon = button.querySelector("i");

                if (icon) {
                    icon.className = showPassword
                        ? "bi bi-eye-slash"
                        : "bi bi-eye";
                }

                button.setAttribute(
                    "aria-pressed",
                    String(showPassword)
                );

                button.setAttribute(
                    "aria-label",
                    showPassword ? "Hide password" : "Show password"
                );
            });
        });
    }


    // =====================================================
    // LOGIN FORM
    // =====================================================

    function initializeLoginForm() {
        const form = getElement("loginForm");

        if (!form) return;

        const emailField = getElement("email");
        const passwordField = getElement("password");

        const messageElement = getElement("authMessage");

        const button = getElement("loginButton");
        const buttonLabel = getElement("loginButtonText");

        const defaultButtonText = "Sign In";

        /**
         * Clear validation errors when users edit fields.
         */
        [emailField, passwordField].forEach((field) => {
            if (!field) return;

            field.addEventListener("input", () => {
                clearInvalid(field);
                clearMessage(messageElement);
            });
        });


        /**
         * Login form submission.
         */
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            clearMessage(messageElement);

            clearInvalid(emailField);
            clearInvalid(passwordField);

            const email = emailField.value.trim();
            const password = passwordField.value;

            if (!isValidEmail(email)) {
                markInvalid(emailField);

                showMessage(
                    messageElement,
                    "Please enter a valid email address."
                );

                emailField.focus();

                return;
            }

            if (!password) {
                markInvalid(passwordField);

                showMessage(
                    messageElement,
                    "Please enter your password."
                );

                passwordField.focus();

                return;
            }

            setButtonLoading(
                button,
                buttonLabel,
                true,
                defaultButtonText
            );

            try {
                /*
                 * Requires a real Flask endpoint:
                 * POST /api/auth/login
                 *
                 * Expected response example:
                 * {
                 *   "success": true,
                 *   "message": "Login successful",
                 *   "redirect_url": "/dashboard"
                 * }
                 *
                 * Adapt this contract to the actual backend.
                 */
                const result = await apiRequest(
                    CONFIG.LOGIN_ENDPOINT,
                    {
                        email: email,
                        password: password
                    }
                );

                if (result.success === false) {
                    throw new Error(
                        result.message || "Login failed."
                    );
                }

                showMessage(
                    messageElement,
                    result.message || "Login successful.",
                    "success"
                );

                /*
                 * Only redirect after the server confirms login.
                 * Do not store passwords or trust client-side
                 * flags as proof of authentication.
                 */
                const redirectUrl =
                    (result.data && result.data.redirect_url) ||
                    result.redirect_url ||
                    "dashboard.html";

                window.setTimeout(() => {
                    window.location.assign(redirectUrl);
                }, 500);

            } catch (error) {
                showMessage(
                    messageElement,
                    getFriendlyError(error, "login")
                );

            } finally {
                setButtonLoading(
                    button,
                    buttonLabel,
                    false,
                    defaultButtonText
                );
            }
        });
    }


    // =====================================================
    // SIGNUP PASSWORD STRENGTH
    // =====================================================

    /**
     * Estimate password strength for user feedback.
     *
     * This is not a substitute for server-side password
     * policy enforcement or secure password hashing.
     */
    function calculatePasswordStrength(value) {
        if (!value) return 0;

        let score = 0;

        if (value.length >= 8) score++;
        if (value.length >= 12) score++;

        if (/[a-z]/.test(value) && /[A-Z]/.test(value)) {
            score++;
        }

        if (/\d/.test(value) && /[^a-zA-Z0-9]/.test(value)) {
            score++;
        }

        return Math.min(score, 4);
    }


    function initializePasswordStrength() {
        const passwordField = getElement("password");
        const strengthText = getElement("passwordStrengthText");

        const bars = document.querySelectorAll(
            ".signup-password-strength .signup-strength-bar"
        );

        if (!passwordField || !strengthText || !bars.length) {
            return;
        }

        const labels = [
            "",
            "Weak password",
            "Fair password",
            "Good password",
            "Strong password"
        ];

        const colors = [
            "",
            "#f87171",
            "#fbbf24",
            "#60a5fa",
            "#6ce7ad"
        ];

        function updateStrength() {
            const score = calculatePasswordStrength(
                passwordField.value
            );

            strengthText.textContent = labels[score];

            bars.forEach((bar, index) => {
                bar.style.background =
                    index < score ? colors[score] : "#29384b";
            });
        }

        passwordField.addEventListener("input", updateStrength);
    }


    // =====================================================
    // SIGNUP FORM
    // =====================================================

    function initializeSignupForm() {
        const form = getElement("signupForm");

        if (!form) return;

        const fullNameField = getElement("fullName");
        const emailField = getElement("email");

        const educationField = getElement("educationLevel");
        const institutionField = getElement("institution");

        const passwordField = getElement("password");
        const confirmPasswordField = getElement("confirmPassword");

        const termsField = getElement("agreeTerms");

        const messageElement = getElement("signupMessage");

        const button = getElement("signupButton");
        const buttonLabel = getElement("signupButtonText");

        const defaultButtonText = "Create Account";


        /**
         * Validate signup fields.
         */
        function validateSignup() {
            const fields = [
                fullNameField,
                emailField,
                educationField,
                institutionField,
                passwordField,
                confirmPasswordField
            ];

            fields.forEach(clearInvalid);

            clearMessage(messageElement);

            if (!fullNameField.value.trim()) {
                markInvalid(fullNameField);

                showMessage(
                    messageElement,
                    "Please enter your full name."
                );

                fullNameField.focus();

                return false;
            }

            if (fullNameField.value.trim().length > 100) {
                markInvalid(fullNameField);

                showMessage(
                    messageElement,
                    "Your name must not exceed 100 characters."
                );

                fullNameField.focus();

                return false;
            }

            if (!isValidEmail(emailField.value)) {
                markInvalid(emailField);

                showMessage(
                    messageElement,
                    "Please enter a valid email address."
                );

                emailField.focus();

                return false;
            }

            if (!educationField.value) {
                markInvalid(educationField);

                showMessage(
                    messageElement,
                    "Please select your education level."
                );

                educationField.focus();

                return false;
            }

            if (!institutionField.value.trim()) {
                markInvalid(institutionField);

                showMessage(
                    messageElement,
                    "Please enter your institution name."
                );

                institutionField.focus();

                return false;
            }

            if (institutionField.value.trim().length > 150) {
                markInvalid(institutionField);

                showMessage(
                    messageElement,
                    "Your institution name must not exceed 150 characters."
                );

                institutionField.focus();

                return false;
            }

            if (
                passwordField.value.length < 8 ||
                passwordField.value.length > 128
            ) {
                markInvalid(passwordField);

                showMessage(
                    messageElement,
                    "Your password must contain between 8 and 128 characters."
                );

                passwordField.focus();

                return false;
            }

            if (!/[A-Z]/.test(passwordField.value) || !/[a-z]/.test(passwordField.value) || !/\d/.test(passwordField.value)) {
                markInvalid(passwordField);

                showMessage(
                    messageElement,
                    "Password must include at least one uppercase letter, one lowercase letter, and one number."
                );

                passwordField.focus();

                return false;
            }

            if (passwordField.value !== confirmPasswordField.value) {
                markInvalid(confirmPasswordField);

                showMessage(
                    messageElement,
                    "The passwords do not match."
                );

                confirmPasswordField.focus();

                return false;
            }

            if (!termsField.checked) {
                showMessage(
                    messageElement,
                    "Please accept the Terms of Service and Privacy Policy."
                );

                termsField.focus();

                return false;
            }

            return true;
        }


        /**
         * Clear errors as the user edits fields.
         */
        [
            fullNameField,
            emailField,
            educationField,
            institutionField,
            passwordField,
            confirmPasswordField
        ].forEach((field) => {
            if (!field) return;

            field.addEventListener("input", () => {
                clearInvalid(field);
                clearMessage(messageElement);
            });

            field.addEventListener("change", () => {
                clearInvalid(field);
                clearMessage(messageElement);
            });
        });


        /**
         * Submit registration to the Flask backend.
         */
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            if (!validateSignup()) {
                return;
            }

            setButtonLoading(
                button,
                buttonLabel,
                true,
                defaultButtonText
            );

            try {
                /*
                 * Requires a real Flask endpoint:
                 * POST /api/auth/register
                 *
                 * Example payload:
                 * {
                 *   "full_name": "...",
                 *   "email": "...",
                 *   "education_level": "...",
                 *   "institution": "...",
                 *   "password": "..."
                 * }
                 *
                 * Password hashing must happen on the backend.
                 */
                const result = await apiRequest(
                    CONFIG.REGISTER_ENDPOINT,
                    {
                        full_name: fullNameField.value.trim(),
                        email: emailField.value.trim(),
                        education_level: educationField.value,
                        institution: institutionField.value.trim(),
                        password: passwordField.value
                    }
                );

                if (result.success === false) {
                    throw new Error(
                        result.message || "Registration failed."
                    );
                }

                showMessage(
                    messageElement,
                    result.message ||
                    "Your account has been created successfully.",
                    "success"
                );

                /*
                 * Do not redirect until the backend confirms success.
                 */
                window.setTimeout(() => {
                    window.location.assign("login.html");
                }, 1000);

            } catch (error) {
                showMessage(
                    messageElement,
                    getFriendlyError(error, "register")
                );

            } finally {
                setButtonLoading(
                    button,
                    buttonLabel,
                    false,
                    defaultButtonText
                );
            }
        });
    }


    // =====================================================
    // FORGOT PASSWORD
    // =====================================================

    function initializeForgotPassword() {
        const button = getElement("forgotPassword");

        if (!button) return;

        button.addEventListener("click", async (event) => {
            event.preventDefault();

            const emailField = getElement("email");
            const messageElement = getElement("authMessage");

            clearMessage(messageElement);

            const email = emailField
                ? emailField.value.trim()
                : "";

            if (!isValidEmail(email)) {
                showMessage(
                    messageElement,
                    "Enter your email address first to request a password reset."
                );

                if (emailField) {
                    emailField.focus();
                }

                return;
            }

            try {
                /*
                 * This endpoint must be implemented on the backend.
                 * The server should return a generic response that
                 * does not reveal whether an account exists.
                 */
                const result = await apiRequest(
                    CONFIG.FORGOT_PASSWORD_ENDPOINT,
                    { email: email }
                );

                showMessage(
                    messageElement,
                    result.message ||
                    "If an account exists for this email, password reset instructions will be sent.",
                    "success"
                );

            } catch (error) {
                showMessage(
                    messageElement,
                    getFriendlyError(error, "forgot-password")
                );
            }
        });
    }


    // =====================================================
    // INITIALIZATION
    // =====================================================

    function initializeAuth() {
        initializePasswordVisibility();
        initializeLoginForm();
        initializeSignupForm();
        initializePasswordStrength();
        initializeForgotPassword();
    }


    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initializeAuth,
            { once: true }
        );
    } else {
        initializeAuth();
    }

})();