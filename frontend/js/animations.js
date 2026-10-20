/**
 * ScholarTrack — Advanced UI Animations
 * Technologies: GSAP + ScrollTrigger
 *
 * Features:
 * 1. Hero entrance animation
 * 2. Scroll-triggered section reveals
 * 3. Feature card stagger animations
 * 4. Step-by-step workflow animations
 * 5. CTA entrance animation
 * 6. Navbar and button interactions
 * 7. Reduced-motion accessibility support
 *
 * No mouse-following or cursor-tracking animations.
 */

(() => {
    "use strict";

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    const gsapAvailable =
        typeof window.gsap !== "undefined" &&
        typeof window.ScrollTrigger !== "undefined";

    /**
     * Reveal all hidden content safely.
     * Used when animations are unavailable or disabled.
     */
    function revealEverything() {
        document.documentElement.classList.remove("js-animations");

        document.querySelectorAll(".reveal").forEach((element) => {
            element.classList.add("is-visible");
            element.style.opacity = "1";
            element.style.visibility = "visible";
            element.style.transform = "none";
        });

        document.querySelectorAll(".feature-card, .step-card").forEach((element) => {
            element.style.opacity = "1";
            element.style.visibility = "visible";
            element.style.transform = "none";
        });
    }

    /**
     * Set up basic interactions that do not require GSAP.
     */
    function setupBasicInteractions() {
        // Button click feedback.
        document.querySelectorAll(".btn").forEach((button) => {
            button.addEventListener("click", () => {
                button.classList.add("button-clicked");

                window.setTimeout(() => {
                    button.classList.remove("button-clicked");
                }, 180);
            });
        });

        // Update the current year in the footer.
        const yearElement = document.getElementById("currentYear");

        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    }

    /**
     * Initialize GSAP animations.
     */
    function initializeAnimations() {
        if (!gsapAvailable || prefersReducedMotion.matches) {
            revealEverything();
            return;
        }

        const gsap = window.gsap;
        const ScrollTrigger = window.ScrollTrigger;

        gsap.registerPlugin(ScrollTrigger);

        gsap.defaults({
            ease: "power3.out",
            duration: 0.8
        });

        // Avoid content staying hidden if initialization fails.
        try {
            setupHeroAnimation();
            setupScrollReveal();
            setupFeatureCards();
            setupWorkflowSteps();
            setupCTAAnimation();
            setupNavbarAnimation();
            setupButtonAnimations();

            // Refresh trigger positions after the page layout is ready.
            window.addEventListener(
                "load",
                () => {
                    ScrollTrigger.refresh();
                },
                { once: true }
            );
        } catch (error) {
            console.error("ScholarTrack animation initialization failed:", error);
            revealEverything();
        }
    }

    /**
     * Hero section entrance.
     * Animations run automatically when the page loads.
     */
    function setupHeroAnimation() {
        const hero = document.querySelector(".hero-section");

        if (!hero) return;

        const heroTitle = hero.querySelector(".hero-title");
        const heroDescription = hero.querySelector(".hero-description");
        const heroActions = hero.querySelector(".hero-actions");
        const heroVisual = hero.querySelector(".hero-visual");
        const heroBadge = hero.querySelector(".hero-badge");

        const timeline = gsap.timeline({
            defaults: {
                ease: "power3.out"
            }
        });

        if (heroBadge) {
            timeline.fromTo(
                heroBadge,
                {
                    opacity: 0,
                    y: 15
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.55
                }
            );
        }

        if (heroTitle) {
            timeline.fromTo(
                heroTitle,
                {
                    opacity: 0,
                    y: 35
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.85
                },
                "-=0.25"
            );
        }

        if (heroDescription) {
            timeline.fromTo(
                heroDescription,
                {
                    opacity: 0,
                    y: 20
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.7
                },
                "-=0.45"
            );
        }

        if (heroActions) {
            timeline.fromTo(
                heroActions,
                {
                    opacity: 0,
                    y: 18
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.65
                },
                "-=0.35"
            );
        }

        if (heroVisual) {
            timeline.fromTo(
                heroVisual,
                {
                    opacity: 0,
                    x: 25,
                    scale: 0.97
                },
                {
                    opacity: 1,
                    x: 0,
                    scale: 1,
                    duration: 1
                },
                "-=0.65"
            );
        }
    }

    /**
     * Reveal regular sections when they enter the viewport.
     */
    function setupScrollReveal() {
        const elements = document.querySelectorAll(
            ".reveal:not(.hero-title):not(.hero-description)"
        );

        elements.forEach((element) => {
            // Hero elements are handled by the hero timeline.
            if (element.closest(".hero-section")) {
                return;
            }

            gsap.fromTo(
                element,
                {
                    opacity: 0,
                    y: 28
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.75,
                    ease: "power3.out",
                    scrollTrigger: {
                        trigger: element,
                        start: "top 88%",
                        once: true
                    },
                    onStart: () => {
                        element.classList.add("is-visible");
                    },
                    onComplete: () => {
                        element.classList.add("is-visible");
                    }
                }
            );
        });
    }

    /**
     * Feature cards appear one after another.
     */
    function setupFeatureCards() {
        const featureSection = document.querySelector("#features");

        if (!featureSection) return;

        const cards = featureSection.querySelectorAll(".feature-card");

        if (!cards.length) return;

        gsap.fromTo(
            cards,
            {
                opacity: 0,
                y: 35
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.7,
                stagger: 0.12,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: featureSection,
                    start: "top 78%",
                    once: true
                }
            }
        );
    }

    /**
     * Workflow steps enter in sequence.
     */
    function setupWorkflowSteps() {
        const workflowSection = document.querySelector("#how-it-works");

        if (!workflowSection) return;

        const steps = workflowSection.querySelectorAll(
            ".step-card, .workflow-step, .process-step"
        );

        if (!steps.length) return;

        gsap.fromTo(
            steps,
            {
                opacity: 0,
                y: 25
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.65,
                stagger: 0.16,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: workflowSection,
                    start: "top 80%",
                    once: true
                }
            }
        );
    }

    /**
     * CTA section entrance animation.
     */
    function setupCTAAnimation() {
        const ctaSection = document.querySelector(
            ".cta-section, #cta, .final-cta"
        );

        if (!ctaSection) return;

        const ctaContent = ctaSection.querySelector(
            ".container, .cta-content"
        );

        if (!ctaContent) return;

        gsap.fromTo(
            ctaContent,
            {
                opacity: 0,
                y: 25
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.85,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: ctaSection,
                    start: "top 82%",
                    once: true
                }
            }
        );
    }

    /**
     * Navbar entrance animation.
     * This is automatic and does not track the mouse.
     */
    function setupNavbarAnimation() {
        const navbar = document.querySelector("#siteHeader");

        if (!navbar) return;

        gsap.fromTo(
            navbar,
            {
                opacity: 0,
                y: -12
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.65,
                delay: 0.1,
                clearProps: "transform"
            }
        );
    }

    /**
     * Small, accessible button hover animations.
     * No pointer-position tracking is used.
     */
    function setupButtonAnimations() {
        const buttons = document.querySelectorAll(
            ".btn-primary, .btn-outline-light, .btn-outline-primary"
        );

        buttons.forEach((button) => {
            button.addEventListener("mouseenter", () => {
                gsap.to(button, {
                    y: -2,
                    duration: 0.2,
                    ease: "power2.out",
                    overwrite: "auto"
                });
            });

            button.addEventListener("mouseleave", () => {
                gsap.to(button, {
                    y: 0,
                    duration: 0.2,
                    ease: "power2.out",
                    overwrite: "auto"
                });
            });
        });
    }

    /**
     * Respond to the operating system's reduced-motion preference.
     */
    function setupReducedMotionListener() {
        const handleMotionChange = () => {
            if (prefersReducedMotion.matches) {
                if (gsapAvailable) {
                    window.gsap.killTweensOf("*");

                    if (window.ScrollTrigger) {
                        window.ScrollTrigger.getAll().forEach((trigger) => {
                            trigger.kill();
                        });
                    }
                }

                revealEverything();
            } else {
                // Reloading gives the page a clean animation state.
                window.location.reload();
            }
        };

        if (typeof prefersReducedMotion.addEventListener === "function") {
            prefersReducedMotion.addEventListener("change", handleMotionChange);
        } else if (typeof prefersReducedMotion.addListener === "function") {
            // Compatibility for older browsers.
            prefersReducedMotion.addListener(handleMotionChange);
        }
    }

    /**
     * Start after the DOM has been parsed.
     */
    function start() {
        setupBasicInteractions();
        setupReducedMotionListener();
        initializeAnimations();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
        start();
    }
})();