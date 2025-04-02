/**
 * Luphonix - Custom Animation Script
 * Provides animations and interactive elements for the Luphonix website
 */

const { default: firebase } = require("firebase/compat/app");

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initInfinityAnimation();
    initNavbarAnimation();
    initScrollAnimations();
    initInteractiveElements();
    initPageTransitions();
});

/**
 * Initializes the infinity symbol background animation
 */
function initInfinityAnimation() {
    const infinitySymbol = document.querySelector('.infinity-symbol');
    if (!infinitySymbol) return;
    
    // Set initial properties
    gsapSetup();
    
    // Clear any previous animation and CSS animation
    infinitySymbol.style.animation = 'none';
    
    // Center it absolutely on the screen
    infinitySymbol.style.position = 'absolute';
    infinitySymbol.style.left = '50%';
    infinitySymbol.style.top = '50%';
    infinitySymbol.style.transform = 'translate(-50%, -50%) scale(1.2)';
    infinitySymbol.style.maxWidth = '60%';
    infinitySymbol.style.opacity = '0.15';
    
    // Add glow effect
    infinitySymbol.style.filter = 'drop-shadow(0 0 20px rgba(0, 195, 255, 0.5))';
    
    // Create a timeline for more complex animation sequence
    const tl = gsap.timeline({repeat: -1});
    
    // First rotation with slight scale up
    tl.to(infinitySymbol, {
        rotation: 180,
        scale: 1.3,
        duration: 30,
        ease: "sine.inOut"
    });
    
    // Second rotation with scale down
    tl.to(infinitySymbol, {
        rotation: 360,
        scale: 1.2,
        duration: 30,
        ease: "sine.inOut"
    });
    
    // Add floating movement
    gsap.to(infinitySymbol, {
        y: 30,
        duration: 10,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });
    
    // Add subtle pulse effect to opacity
    gsap.to(infinitySymbol, {
        opacity: 0.25,
        duration: 8,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });
}

/**
 * Sets up GSAP if it's not already available
 */
function gsapSetup() {
    // If GSAP is not available, create a more advanced fallback
    if (typeof gsap === 'undefined') {
        window.gsap = {
            to: function(element, options) {
                // Basic animation fallback using CSS transitions
                if (element) {
                    element.style.transition = `all ${options.duration || 1}s`;
                    
                    // Apply transform properties
                    let transform = '';
                    
                    if (options.rotation) {
                        transform += ` rotate(${options.rotation}deg)`;
                    }
                    
                    if (options.y) {
                        transform += ` translateY(${options.y}px)`;
                    }
                    
                    if (options.scale) {
                        transform += ` scale(${options.scale})`;
                    }
                    
                    // Apply transform if there are any transform properties
                    if (transform) {
                        element.style.transform = transform.trim();
                    }
                    
                    // Apply other style properties
                    if (options.opacity !== undefined) {
                        element.style.opacity = options.opacity;
                    }
                    
                    if (options.filter) {
                        element.style.filter = options.filter;
                    }
                }
                
                // Return a simple object to prevent errors
                return {
                    pause: function() {},
                    play: function() {},
                    reverse: function() {}
                };
            },
            timeline: function(options) {
                // Return a simplified timeline object that just calls 'to'
                return {
                    to: this.to,
                    pause: function() {},
                    play: function() {},
                    reverse: function() {}
                };
            }
        };
    }
}

/**
 * Initializes navbar animations and behavior
 */
function initNavbarAnimation() {
    const navbar = document.getElementById('mainNav');
    if (!navbar) return;
    
    // Change navbar on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.padding = '0.5rem 1rem';
            navbar.style.backgroundColor = 'rgba(17, 24, 39, 0.95)';
        } else {
            navbar.style.padding = '1rem';
            navbar.style.backgroundColor = 'rgba(17, 24, 39, 0.8)';
        }
    });
    
    // Handle navbar links active state
    const navLinks = navbar.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // If it's a page link (not a section link), let it navigate normally
            if (this.getAttribute('href').startsWith('/') || 
                this.getAttribute('href').startsWith('http')) {
                return;
            }
            
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Smooth scroll to target
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const yOffset = -80; // Navbar height with some padding
                const y = targetElement.getBoundingClientRect().top + window.pageYOffset + yOffset;
                
                window.scrollTo({
                    top: y,
                    behavior: 'smooth'
                });
                
                // Close the mobile menu if open
                const navbarToggler = navbar.querySelector('.navbar-toggler');
                const navbarCollapse = navbar.querySelector('.navbar-collapse');
                
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
    });
}

/**
 * Initializes scroll-based animations
 */
function initScrollAnimations() {
    // Add scroll reveal animations if ScrollReveal is available
    if (typeof ScrollReveal !== 'undefined') {
        // Configure ScrollReveal
        const sr = ScrollReveal({
            distance: '50px',
            duration: 1000,
            easing: 'ease-in-out',
            origin: 'bottom',
            reset: false
        });
        
        // Apply to various elements
        sr.reveal('.hero-content', { delay: 200 });
        sr.reveal('.section-title', { delay: 100 });
        sr.reveal('.section-description', { delay: 200 });
        sr.reveal('.team-card', { interval: 200 });
        sr.reveal('.tech-card', { interval: 150 });
        sr.reveal('.project-card', { interval: 200 });
    }
    
    // Disable the parallax effect on the background to maintain centered infinity symbol
    // We'll keep it centered regardless of scroll position
}

/**
 * Initializes interactive UI elements
 */
function initInteractiveElements() {
    // Add hover effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add particle effect to the hero section if canvas is supported
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && typeof document.createElement('canvas').getContext === 'function') {
        createParticleEffect(heroSection);
    }
}

/**
 * Creates a particle effect in the specified container
 * @param {HTMLElement} container - The container for the particle effect
 */
function createParticleEffect(container) {
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.className = 'particle-canvas';
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '0';
    
    // Insert canvas as the first child of the container
    container.insertBefore(canvas, container.firstChild);
    
    // Set canvas size
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
    
    // Initialize particles
    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 50;
    
    // Create particles
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2 + 1,
            color: 'rgba(0, 195, 255, ' + (Math.random() * 0.3 + 0.2) + ')',
            speedX: Math.random() * 0.5 - 0.25,
            speedY: Math.random() * 0.5 - 0.25
        });
    }
    
    // Animation loop
    function animate() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Update and draw particles
        for (let i = 0; i < particleCount; i++) {
            const p = particles[i];
            
            // Move particles
            p.x += p.speedX;
            p.y += p.speedY;
            
            // Bounce off edges
            if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
            if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;
            
            // Draw particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
            
            // Draw connections
            for (let j = i + 1; j < particleCount; j++) {
                const p2 = particles[j];
                const distance = Math.sqrt(
                    Math.pow(p.x - p2.x, 2) + 
                    Math.pow(p.y - p2.y, 2)
                );
                
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = 'rgba(0, 195, 255, ' + (0.2 - distance/500) + ')';
                    ctx.stroke();
                }
            }
        }
        
        // Request next frame
        requestAnimationFrame(animate);
    }
    
    // Start animation
    animate();
    
    // Update canvas size on window resize
    window.addEventListener('resize', function() {
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
    });
}

/**
 * Handles fading transitions between pages
 */
function initPageTransitions() {
    // Add transition overlay
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = '#111827';
    overlay.style.zIndex = '9999';
    overlay.style.opacity = '1';
    overlay.style.transition = 'opacity 0.5s ease-in-out';
    document.body.appendChild(overlay);
    
    // Fade out overlay when page is loaded
    setTimeout(function() {
        overlay.style.opacity = '0';
        setTimeout(function() {
            overlay.remove();
        }, 500);
    }, 300);
    
    // Capture link clicks for transition effect
    document.querySelectorAll('a').forEach(link => {
        // Skip non-page links
        if (!link.getAttribute('href') || 
            link.getAttribute('href').startsWith('#') || 
            link.getAttribute('href') === '' ||
            link.getAttribute('target') === '_blank' ||
            link.classList.contains('no-transition')) {
            return;
        }
        
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if modified click or non-navigational
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
                return;
            }
            
            e.preventDefault();
            
            // Show transition overlay
            const transitionOverlay = document.createElement('div');
            transitionOverlay.className = 'page-transition-overlay';
            transitionOverlay.style.position = 'fixed';
            transitionOverlay.style.top = '0';
            transitionOverlay.style.left = '0';
            transitionOverlay.style.width = '100%';
            transitionOverlay.style.height = '100%';
            transitionOverlay.style.backgroundColor = '#111827';
            transitionOverlay.style.zIndex = '9999';
            transitionOverlay.style.opacity = '0';
            transitionOverlay.style.transition = 'opacity 0.5s ease-in-out';
            document.body.appendChild(transitionOverlay);
            
            // Fade in overlay and navigate
            setTimeout(function() {
                transitionOverlay.style.opacity = '1';
                setTimeout(function() {
                    window.location.href = href;
                }, 500);
            }, 10);
        });
    });
}

// Firebase Authentication functionality
function initFirebaseAuth() {
    // Check if Firebase is available
    if (typeof firebase !== 'undefined' && firebase.auth) {
        // Auth state change observer
        firebase.auth().onAuthStateChanged(function(user) {
            const userStatusElements = document.querySelectorAll('.user-status');
            
            if (user) {
                // User is signed in
                console.log('User is signed in:', user.displayName);
                
                // Update UI elements that show user status
                userStatusElements.forEach(element => {
                    if (element.dataset.signedIn) {
                        element.innerHTML = element.dataset.signedIn
                            .replace('{name}', user.displayName || 'User')
                            .replace('{email}', user.email || '');
                        element.classList.remove('d-none');
                    } else {
                        element.classList.add('d-none');
                    }
                });
                
                // Show sign-out buttons
                document.querySelectorAll('.sign-out-btn').forEach(btn => {
                    btn.classList.remove('d-none');
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        firebase.auth().signOut();
                    });
                });
                
                // Hide sign-in buttons
                document.querySelectorAll('.sign-in-btn').forEach(btn => {
                    btn.classList.add('d-none');
                });
            } else {
                // User is signed out
                console.log('User is signed out');
                
                // Update UI elements that show user status
                userStatusElements.forEach(element => {
                    if (element.dataset.signedOut) {
                        element.innerHTML = element.dataset.signedOut;
                        element.classList.remove('d-none');
                    } else {
                        element.classList.add('d-none');
                    }
                });
                
                // Hide sign-out buttons
                document.querySelectorAll('.sign-out-btn').forEach(btn => {
                    btn.classList.add('d-none');
                });
                
                // Show sign-in buttons
                document.querySelectorAll('.sign-in-btn').forEach(btn => {
                    btn.classList.remove('d-none');
                });
            }
        });
    }
}

// Handle Firebase redirect result
function handleFirebaseRedirect() {
    // Check if Firebase is available
    if (typeof firebase !== 'undefined' && firebase.auth) {
        firebase.auth().getRedirectResult()
            .then((result) => {
                if (result.credential) {
                    // This gives you a Google Access Token. You can use it to access Google APIs.
                    const credential = result.credential;
                    const token = credential.accessToken;
                    console.log('Successfully signed in with redirect');
                }
                // The signed-in user info.
                const user = result.user;
            })
            .catch((error) => {
                // Handle Errors here.
                console.error('Firebase redirect error:', error);
                const errorCode = error.code;
                const errorMessage = error.message;
                // The email of the user's account used.
                const email = error.email;
                // The AuthCredential type that was used.
                const credential = firebase.auth.GoogleAuthProvider.credentialFromError(error);
                
                // Display error to user
                const errorContainer = document.getElementById('auth-error');
                if (errorContainer) {
                    errorContainer.textContent = errorMessage;
                    errorContainer.classList.remove('d-none');
                }
            });
    }
}

// Function to sign in with Google
function signInWithGoogle() {
    // Check if Firebase is available
    if (typeof firebase !== 'undefined' && firebase.auth) {
        const provider = new firebase.auth.GoogleAuthProvider();
        firebase.auth().signInWithRedirect(provider);
    } else {
        console.error('Firebase not available');
    }
}

// Initialize Firebase Auth when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    initFirebaseAuth();
    handleFirebaseRedirect();
    
    // Add event listeners to sign-in buttons
    document.querySelectorAll('.google-sign-in').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            signInWithGoogle();
        });
    });
});