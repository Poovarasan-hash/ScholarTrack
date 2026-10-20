"use strict";

/* =========================================================
   SCHOLARTRACK
   Main Frontend JavaScript
========================================================= */

(() => {
    const ScholarTrack = {
        config: {
            loaderDelay: 350,
            scrollThreshold: 30,
            threeEnabled: true
        },

        state: {
            scene: null,
            camera: null,
            renderer: null,
            animationFrame: null,
            resizeObserver: null,
            isDestroyed: false
        },

        init() {
            if (this.state.isDestroyed) {
                return;
            }

            this.enableAnimationStyles();
            this.hidePageLoader();
            this.updateFooterYear();
            this.initNavbar();
            this.initThreeScene();
            this.initReducedMotionHandling();
        },

        /* ================================================
           ENABLE ANIMATION STYLES
        ================================================ */

        enableAnimationStyles() {
            document.documentElement.classList.add("js-enabled");

            if (
                !window.matchMedia(
                    "(prefers-reduced-motion: reduce)"
                ).matches
            ) {
                document.documentElement.classList.add(
                    "js-animations"
                );
            }
        },

        /* ================================================
           PAGE LOADER
        ================================================ */

        hidePageLoader() {
            const loader = document.getElementById("pageLoader");

            if (!loader) {
                return;
            }

            const hideLoader = () => {
                loader.classList.add("is-hidden");

                window.setTimeout(() => {
                    loader.setAttribute("hidden", "");
                }, 500);
            };

            if (document.readyState === "complete") {
                window.setTimeout(
                    hideLoader,
                    this.config.loaderDelay
                );
            } else {
                window.addEventListener(
                    "load",
                    () => {
                        window.setTimeout(
                            hideLoader,
                            this.config.loaderDelay
                        );
                    },
                    { once: true }
                );
            }
        },

        /* ================================================
           FOOTER YEAR
        ================================================ */

        updateFooterYear() {
            const yearElement =
                document.getElementById("currentYear");

            if (yearElement) {
                yearElement.textContent =
                    new Date().getFullYear();
            }
        },

        /* ================================================
           NAVBAR
        ================================================ */

        initNavbar() {
            const header =
                document.getElementById("siteHeader");

            if (!header) {
                return;
            }

            let ticking = false;

            const updateNavbar = () => {
                if (window.scrollY > this.config.scrollThreshold) {
                    header.classList.add("is-scrolled");
                } else {
                    header.classList.remove("is-scrolled");
                }

                ticking = false;
            };

            window.addEventListener(
                "scroll",
                () => {
                    if (!ticking) {
                        window.requestAnimationFrame(updateNavbar);
                        ticking = true;
                    }
                },
                { passive: true }
            );

            updateNavbar();

            /* Close mobile navigation after clicking a section link */

            const navigation =
                document.getElementById("mainNavigation");

            if (!navigation || !window.bootstrap) {
                return;
            }

            navigation.querySelectorAll('a[href^="#"]').forEach(
                (link) => {
                    link.addEventListener("click", () => {
                        const isMobile =
                            window.matchMedia(
                                "(max-width: 991.98px)"
                            ).matches;

                        if (!isMobile) {
                            return;
                        }

                        const collapse =
                            window.bootstrap.Collapse.getInstance(
                                navigation
                            );

                        if (collapse) {
                            collapse.hide();
                        }
                    });
                }
            );
        },

        /* ================================================
           REDUCED MOTION
        ================================================ */

        initReducedMotionHandling() {
            const motionPreference = window.matchMedia(
                "(prefers-reduced-motion: reduce)"
            );

            const updateMotionPreference = (event) => {
                document.documentElement.classList.toggle(
                    "js-animations",
                    !event.matches
                );

                if (event.matches) {
                    this.stopThreeAnimation();
                } else if (
                    !this.state.renderer &&
                    !this.state.isDestroyed
                ) {
                    this.initThreeScene();
                }
            };

            if (motionPreference.addEventListener) {
                motionPreference.addEventListener(
                    "change",
                    updateMotionPreference
                );
            } else {
                motionPreference.addListener(
                    updateMotionPreference
                );
            }
        },

        /* ================================================
           THREE.JS INITIALIZATION
        ================================================ */

        initThreeScene() {
            const canvas =
                document.getElementById("heroCanvas");

            if (!canvas || !this.config.threeEnabled) {
                return;
            }

            if (
                window.matchMedia(
                    "(prefers-reduced-motion: reduce)"
                ).matches
            ) {
                return;
            }

            if (!window.THREE) {
                console.warn(
                    "ScholarTrack: Three.js could not be loaded."
                );

                return;
            }

            try {
                this.createThreeScene(canvas);
            } catch (error) {
                console.warn(
                    "ScholarTrack: 3D scene initialization failed.",
                    error
                );

                this.destroyThreeScene();
            }
        },

        /* ================================================
           THREE.JS SCENE
        ================================================ */

        createThreeScene(canvas) {
            const THREE = window.THREE;

            const scene = new THREE.Scene();

            const camera = new THREE.PerspectiveCamera(
                45,
                1,
                0.1,
                100
            );

            camera.position.set(0, 0, 8);

            let renderer;

            try {
                renderer = new THREE.WebGLRenderer({
                    canvas,
                    alpha: true,
                    antialias: true,
                    powerPreference: "low-power"
                });
            } catch (error) {
                console.warn(
                    "ScholarTrack: WebGL is unavailable."
                );

                return;
            }

            renderer.setPixelRatio(
                Math.min(window.devicePixelRatio || 1, 1.5)
            );

            renderer.setClearColor(0x000000, 0);

            scene.add(
                new THREE.AmbientLight(0xffffff, 1.4)
            );

            const mainLight = new THREE.PointLight(
                0x10b981,
                2,
                30
            );

            mainLight.position.set(2, 3, 5);

            scene.add(mainLight);

            /* Main decorative geometry */

            const geometry = new THREE.IcosahedronGeometry(
                1.5,
                1
            );

            const material = new THREE.MeshStandardMaterial({
                color: 0x10b981,
                emissive: 0x064e3b,
                emissiveIntensity: 0.35,
                metalness: 0.55,
                roughness: 0.35,
                wireframe: true,
                transparent: true,
                opacity: 0.32
            });

            const mainObject = new THREE.Mesh(
                geometry,
                material
            );

            scene.add(mainObject);

            /* Secondary geometric rings */

            const ringGeometry = new THREE.TorusGeometry(
                2.1,
                0.008,
                8,
                100
            );

            const ringMaterial = new THREE.MeshBasicMaterial({
                color: 0x6ee7b7,
                transparent: true,
                opacity: 0.23
            });

            const ring = new THREE.Mesh(
                ringGeometry,
                ringMaterial
            );

            ring.rotation.x = 0.85;
            ring.rotation.y = 0.35;

            scene.add(ring);

            /* Decorative particles */

            const particleCount = 180;
            const positions = new Float32Array(
                particleCount * 3
            );

            for (let i = 0; i < particleCount; i++) {
                const index = i * 3;

                positions[index] =
                    (Math.random() - 0.5) * 12;

                positions[index + 1] =
                    (Math.random() - 0.5) * 8;

                positions[index + 2] =
                    (Math.random() - 0.5) * 6;
            }

            const particleGeometry =
                new THREE.BufferGeometry();

            particleGeometry.setAttribute(
                "position",
                new THREE.BufferAttribute(positions, 3)
            );

            const particleMaterial =
                new THREE.PointsMaterial({
                    color: 0x6ee7b7,
                    size: 0.025,
                    transparent: true,
                    opacity: 0.5,
                    sizeAttenuation: true
                });

            const particles = new THREE.Points(
                particleGeometry,
                particleMaterial
            );

            scene.add(particles);

            this.state.scene = scene;
            this.state.camera = camera;
            this.state.renderer = renderer;

            this.state.objects = {
                mainObject,
                ring,
                particles
            };

            const resizeScene = () => {
                if (
                    this.state.isDestroyed ||
                    !this.state.renderer
                ) {
                    return;
                }

                const width =
                    canvas.clientWidth ||
                    canvas.parentElement?.clientWidth ||
                    window.innerWidth;

                const height =
                    canvas.clientHeight ||
                    canvas.parentElement?.clientHeight ||
                    400;

                if (width <= 0 || height <= 0) {
                    return;
                }

                camera.aspect = width / height;
                camera.updateProjectionMatrix();

                renderer.setSize(width, height, false);
            };

            this.state.resizeObserver =
                new ResizeObserver(resizeScene);

            this.state.resizeObserver.observe(canvas);

            if (canvas.parentElement) {
                this.state.resizeObserver.observe(
                    canvas.parentElement
                );
            }

            window.addEventListener(
                "resize",
                resizeScene,
                { passive: true }
            );

            this.state.resizeHandler = resizeScene;

            resizeScene();

            /* Automatic animation only.
               No cursor or mouse-position tracking. */

            const clock = new THREE.Clock();

            const animate = () => {
                if (
                    this.state.isDestroyed ||
                    !this.state.renderer
                ) {
                    return;
                }

                this.state.animationFrame =
                    window.requestAnimationFrame(animate);

                const elapsed = clock.getElapsedTime();

                mainObject.rotation.x = elapsed * 0.055;
                mainObject.rotation.y = elapsed * 0.075;

                ring.rotation.z = elapsed * 0.025;

                particles.rotation.y = elapsed * 0.008;

                renderer.render(scene, camera);
            };

            animate();
        },

        /* ================================================
           STOP THREE.JS ANIMATION
        ================================================ */

        stopThreeAnimation() {
            if (this.state.animationFrame !== null) {
                window.cancelAnimationFrame(
                    this.state.animationFrame
                );

                this.state.animationFrame = null;
            }

            if (
                this.state.renderer &&
                this.state.scene &&
                this.state.camera
            ) {
                this.state.renderer.render(
                    this.state.scene,
                    this.state.camera
                );
            }
        },

        /* ================================================
           CLEAN UP THREE.JS
        ================================================ */

        destroyThreeScene() {
            this.stopThreeAnimation();

            if (this.state.resizeObserver) {
                this.state.resizeObserver.disconnect();

                this.state.resizeObserver = null;
            }

            if (this.state.resizeHandler) {
                window.removeEventListener(
                    "resize",
                    this.state.resizeHandler
                );

                this.state.resizeHandler = null;
            }

            if (this.state.scene) {
                this.state.scene.traverse((object) => {
                    if (object.geometry) {
                        object.geometry.dispose();
                    }

                    if (object.material) {
                        const materials = Array.isArray(
                            object.material
                        )
                            ? object.material
                            : [object.material];

                        materials.forEach((material) => {
                            material.dispose();
                        });
                    }
                });
            }

            if (this.state.renderer) {
                this.state.renderer.dispose();
            }

            this.state.scene = null;
            this.state.camera = null;
            this.state.renderer = null;
            this.state.objects = null;
        }
    };

    /* Initialize after the DOM is ready */

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            () => ScholarTrack.init(),
            { once: true }
        );
    } else {
        ScholarTrack.init();
    }

    /* Expose utilities for later integration and testing */

    window.ScholarTrack = ScholarTrack;
})();