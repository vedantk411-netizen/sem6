// State to track current role
let currentRole = 'photographer';

// DOM Elements
const btnPhotographer = document.getElementById('btn-photographer');
const btnAdmin = document.getElementById('btn-admin');
const formTitle = document.getElementById('form-title');
const authForm = document.getElementById('authForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

// Register Elements
const registerForm = document.getElementById('registerForm');
const showRegisterBtn = document.getElementById('show-register');
const showLoginBtn = document.getElementById('show-login');
const regNameInput = document.getElementById('reg-name');
const regEmailInput = document.getElementById('reg-email');
const regPasswordInput = document.getElementById('reg-password');

// Registration Link Container (to hide/show)
const registerLinkContainer = showRegisterBtn ? showRegisterBtn.parentElement : null;

// Function to switch roles
function setRole(role) {
    currentRole = role;

    if (role === 'photographer') {
        if (btnPhotographer) btnPhotographer.classList.add('active');
        if (btnAdmin) btnAdmin.classList.remove('active');
        if (formTitle) formTitle.innerText = 'Photographer Login';
        document.documentElement.style.setProperty('--primary-color', '#f1c40f'); // Gold
        
        // Show registration link
        if (registerLinkContainer) registerLinkContainer.style.display = 'block';
    } else {
        if (btnAdmin) btnAdmin.classList.add('active');
        if (btnPhotographer) btnPhotographer.classList.remove('active');
        if (formTitle) formTitle.innerText = 'Admin Console Login';
        document.documentElement.style.setProperty('--primary-color', '#e74c3c'); // Red for Admin
        
        // Hide registration link (Admins cannot register)
        if (registerLinkContainer) registerLinkContainer.style.display = 'none';
        
        // Ensure we are on login form
        if (authForm) authForm.style.display = 'block';
        if (registerForm) registerForm.style.display = 'none';
    }
}

// Toggle between Login and Register
if (showRegisterBtn && showLoginBtn) {
    showRegisterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        authForm.style.display = 'none';
        registerForm.style.display = 'block';
    });

    showLoginBtn.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.style.display = 'none';
        authForm.style.display = 'block';
    });
}

// Handle Login Submission
if (authForm) {
    authForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = emailInput.value;
    const password = passwordInput.value;

    console.log('Logging in with:', { email, password });

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, role: currentRole })
        });

        const data = await response.json();

        if (response.ok) {
                // Set login state
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('userName', data.user.name);
                alert(`Welcome back, ${data.user.name}!`);
                
                // Redirect to the dashboard
                window.location.href = data.redirect;
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Server error. Is the backend running?');
    }
});
}

// Handle Register Submission
if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = regNameInput.value;
        const email = regEmailInput.value;
        const password = regPasswordInput.value;

        // Get preferences
        const experience_level = document.getElementById('reg-experience').value;
        const specialization = Array.from(document.querySelectorAll('input[name="specialization"]:checked'))
            .map(el => el.value);
        const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked'))
            .map(el => el.value);

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    name, 
                    email, 
                    password, 
                    role: currentRole,
                    experience_level,
                    specialization,
                    equipment
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert('Registration successful! Please login.');
                registerForm.style.display = 'none';
                authForm.style.display = 'block';
                // Clear the form
                e.target.reset();
            } else {
                alert(data.error || 'Registration failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Server error. Is the backend running?');
        }
    });
}

// --- Chatbot Logic ---
document.addEventListener('DOMContentLoaded', () => {
    // Inject styles for dedicated chatbot page
    if (window.location.pathname === '/chatbot') {
        const style = document.createElement('style');
        style.textContent = `
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            #chatbot-container {
                width: 100%;
                max-width: 1000px;
                height: 90vh;
                background: #1e1e1e;
                border-radius: 16px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 1px solid #333;
            }
            .chat-header {
                background: #252525;
                color: #fff;
                padding: 20px 30px;
                font-size: 1.3em;
                font-weight: 600;
                border-bottom: 1px solid #333;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .chat-header i {
                color: #f1c40f; /* Gold accent */
            }
            .chat-messages {
                flex: 1;
                padding: 40px;
                overflow-y: auto;
                background: #121212;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .chat-msg {
                padding: 15px 22px;
                border-radius: 20px;
                max-width: 80%;
                line-height: 1.6;
                font-size: 1.05rem;
                position: relative;
                word-wrap: break-word;
            }
            .chat-msg.user {
                align-self: flex-end;
                background: #f1c40f; /* Gold */
                color: #000;
                border-bottom-right-radius: 4px;
                font-weight: 500;
            }
            .chat-msg.bot {
                align-self: flex-start;
                background: #2c2c2c;
                color: #e0e0e0;
                border-bottom-left-radius: 4px;
                border: 1px solid #333;
            }
            .chat-input-area {
                padding: 25px;
                background: #1e1e1e;
                border-top: 1px solid #333;
                display: flex;
                gap: 15px;
                align-items: center;
            }
            #chat-input {
                flex: 1;
                padding: 18px 25px;
                border: 1px solid #333;
                border-radius: 30px;
                outline: none;
                font-size: 1rem;
                background: #2c2c2c;
                color: #fff;
                transition: all 0.3s;
            }
            #chat-input:focus {
                border-color: #f1c40f;
                background: #333;
            }
            #chat-send-btn {
                background: #f1c40f;
                color: #000;
                border: none;
                width: 56px;
                height: 56px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
            }
            #chat-send-btn:hover {
                background: #d4ac0d;
                transform: scale(1.05);
            }
            #chatbot-close-btn {
                display: none;
            }
            /* Scrollbar */
            .chat-messages::-webkit-scrollbar {
                width: 8px;
            }
            .chat-messages::-webkit-scrollbar-track {
                background: #121212;
            }
            .chat-messages::-webkit-scrollbar-thumb {
                background: #333;
                border-radius: 4px;
            }
            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: #444;
            }
        `;
        document.head.appendChild(style);
    }

    // Inject Chatbot Widget if missing (e.g. on Dashboard)
    if (!document.getElementById('chatbot-container') && window.location.pathname !== '/chatbot') {
        const widgetHTML = `
            <div id="chatbot-toggle-btn" style="position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: #f1c40f; border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.4); z-index: 9999; transition: transform 0.3s;">
                <i class="fas fa-comment" style="font-size: 24px; color: #121212;"></i>
            </div>
            <div id="chatbot-container" style="display: none; position: fixed; bottom: 100px; right: 30px; width: 350px; height: 500px; background: #1e1e1e; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); flex-direction: column; overflow: hidden; z-index: 9999; border: 1px solid #333;">
                <div class="chat-header" style="background: #252525; color: #fff; padding: 15px 20px; font-weight: 600; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-robot" style="color: #f1c40f;"></i>
                        <span>PhotoMind AI</span>
                    </div>
                    <i id="chatbot-close-btn" class="fas fa-times" style="cursor: pointer; color: #aaa; transition: color 0.2s;"></i>
                </div>
                <div id="chat-messages" class="chat-messages" style="flex: 1; padding: 20px; overflow-y: auto; background: #121212; display: flex; flex-direction: column; gap: 15px;">
                    <div class="chat-msg bot" style="align-self: flex-start; background: #2c2c2c; color: #e0e0e0; padding: 10px 15px; border-radius: 10px 10px 10px 0; max-width: 85%; border: 1px solid #333; font-size: 0.95rem; line-height: 1.5;">
                        Hello! I'm your AI photography assistant. Ask me about lighting, poses, or camera settings!
                    </div>
                </div>
                <div class="chat-input-area" style="padding: 15px; background: #1e1e1e; border-top: 1px solid #333; display: flex; gap: 10px; align-items: center;">
                    <input type="text" id="chat-input" placeholder="Type a message..." style="flex: 1; padding: 12px 15px; border-radius: 25px; border: 1px solid #333; background: #2c2c2c; color: #fff; outline: none; font-size: 0.95rem;">
                    <button id="chat-send-btn" style="background: #f1c40f; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; display: flex; justify-content: center; align-items: center; transition: background 0.2s;">
                        <i class="fas fa-paper-plane" style="color: #121212; font-size: 1rem;"></i>
                    </button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', widgetHTML);

        // Inject styles for the widget messages
        const style = document.createElement('style');
        style.textContent = `
            .chat-msg { padding: 10px 15px; border-radius: 10px; max-width: 85%; font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px; word-wrap: break-word; }
            .chat-msg.user { align-self: flex-end; background: #f1c40f; color: #121212; border-bottom-right-radius: 2px; font-weight: 500; }
            .chat-msg.bot { align-self: flex-start; background: #2c2c2c; color: #e0e0e0; border-bottom-left-radius: 2px; border: 1px solid #333; }
            .chat-messages::-webkit-scrollbar { width: 6px; }
            .chat-messages::-webkit-scrollbar-track { background: #121212; }
            .chat-messages::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
        `;
        document.head.appendChild(style);
    }

    // Inject AI Features in Navbar (Home Page)
    const loginBtn = document.getElementById('login-trigger');
    if (loginBtn && (window.location.pathname === '/' || window.location.pathname === '/index.html')) {
        const navContainer = loginBtn.parentElement;
        
        // Helper to create nav link
        const createNavLink = (id, href, icon, text) => {
            if (document.getElementById(id)) return null;
            const link = document.createElement('a');
            link.id = id;
            link.href = href;
            link.style.marginRight = '25px';
            link.style.textDecoration = 'none';
            link.style.color = 'inherit';
            link.style.cursor = 'pointer';
            link.style.fontWeight = '600';
            link.style.display = 'inline-flex';
            link.style.alignItems = 'center';
            link.style.gap = '8px';
            link.innerHTML = `<i class="${icon}"></i> ${text}`;
            return link;
        };

        const cameraLink = createNavLink('nav-ai-camera', '/camera_ui', 'fas fa-camera', 'AI Camera');

        if (cameraLink) navContainer.insertBefore(cameraLink, loginBtn);
    }

    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotToggleBtn = document.getElementById('chatbot-toggle-btn');
    const chatbotCloseBtn = document.getElementById('chatbot-close-btn');

    // Toggle Logic
    if (chatbotToggleBtn && chatbotContainer) {
        chatbotToggleBtn.addEventListener('click', () => {
            // Check if user is logged in
            const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
            
            if (!isLoggedIn) {
                alert("Please login to use the AI Chat.");
                const modal = document.getElementById('login-modal');
                if (modal) modal.classList.add('active');
                return;
            }

            chatbotContainer.style.display = 'flex';
            chatbotToggleBtn.style.display = 'none';
        });
    }

    if (chatbotCloseBtn && chatbotContainer) {
        chatbotCloseBtn.addEventListener('click', () => {
            chatbotContainer.style.display = 'none';
            chatbotToggleBtn.style.display = 'flex';
        });
    }

    if (!chatInput || !chatSendBtn || !chatMessages) {
        // Chatbot elements not found on this page (e.g. login page)
        return;
    }

    console.log("Chatbot initialized.");

    async function sendChatMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Get selected shoot type (if available)
        const shootTypeSelect = document.getElementById('shootTypeSelect');
        const shootType = shootTypeSelect ? shootTypeSelect.value : null;
        
        // NEW: Get environment from localStorage (set by selectShootType: 'indoor' or 'outdoor')
        // OR from environmentSelector dropdown if it exists
        let environment = null;
        const environmentSelector = document.getElementById('environmentSelector');
        if (environmentSelector) {
            environment = environmentSelector.value;
        } else {
            // Check localStorage for selectedCategory (set when user clicks Indoor/Outdoor)
            environment = localStorage.getItem('selectedCategory');
        }

        // Display User Message
        chatMessages.innerHTML += `<div class="chat-msg user"><strong>You:</strong> ${message}</div>`;
        chatInput.value = '';
        
        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        chatMessages.innerHTML += `<div id="${loadingId}" class="chat-msg bot"><em>Thinking...</em></div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: message,
                    shoot_type: shootType,
                    environment: environment  // NEW: Include environment
                })
            });
            const data = await response.json();
            
            // Remove loading indicator
            const loadingEl = document.getElementById(loadingId);
            if (loadingEl) loadingEl.remove();

            // Display Bot Response
            chatMessages.innerHTML += `<div class="chat-msg bot"><strong>Guide:</strong> ${data.response}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight; // Auto scroll
        } catch (error) {
            console.error('Chat Error:', error);
            const loadingEl = document.getElementById(loadingId);
            if (loadingEl) loadingEl.remove();
            chatMessages.innerHTML += `<div class="chat-msg bot text-danger">Error connecting to guide.</div>`;
        }
    }

    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
});

// Check for user greeting on dashboard
const userGreeting = document.getElementById('user-greeting');
if (userGreeting) {
    const storedName = localStorage.getItem('userName');
    if (storedName) {
        userGreeting.innerText = `Welcome, ${storedName}`;
    }
}

// --- Modal Logic ---
const loginModal = document.getElementById('login-modal');
const loginBtn = document.getElementById('login-trigger');
const closeBtn = document.querySelector('.close-btn');

// Open Modal
if (loginBtn) {
    loginBtn.addEventListener('click', () => {
        loginModal.classList.add('active');
    });
}

// Close Modal
if (closeBtn) {
    closeBtn.addEventListener('click', () => {
        loginModal.classList.remove('active');
    });
}

// Close when clicking outside the container
window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.classList.remove('active');
    }
});

// --- Dashboard Logic (Category and Shoot Selection) ---
// Populate shoot types based on selected category
function populateShootTypes(category) {
    const outdoorTypes = ['outdoor', 'event', 'landscape', 'sports'];
    const indoorTypes = ['wedding', 'portrait', 'product', 'fashion', 'night'];
    
    const gridContainer = document.getElementById('shoot-grid-container');
    if (!gridContainer) return;
    
    // Clear existing content
    gridContainer.innerHTML = '';
    
    // Filter shoot types
    const filteredTypes = shootTypesData.filter(type => {
        const typeName = type.name.toLowerCase();
        if (category === 'outdoor') {
            return outdoorTypes.includes(typeName);
        } else if (category === 'indoor') {
            return indoorTypes.includes(typeName);
        }
        return false;
    });
    
    // Render filtered shoot types
    filteredTypes.forEach(type => {
        const card = document.createElement('div');
        card.className = 'shoot-card';
        card.onclick = () => showShootOptions(type.name, card);
        card.innerHTML = `
            <i class="${type.icon}"></i>
            <h3>${type.name}</h3>
            <p>${type.description || ''}</p>
        `;
        gridContainer.appendChild(card);
    });
    
    console.log(`Populated ${filteredTypes.length} shoot types for ${category} category`);
}

// Populate all shoot types (show everything on dashboard)
function populateAllShootTypes() {
    const gridContainer = document.getElementById('shoot-grid-container');
    if (!gridContainer) return;
    gridContainer.innerHTML = '';

    shootTypesData.forEach(type => {
        const card = document.createElement('div');
        card.className = 'shoot-card';
        card.onclick = () => showShootOptions(type.name, card);
        card.innerHTML = `
            <i class="${type.icon}"></i>
            <h3>${type.name}</h3>
            <p>${type.description || ''}</p>
        `;
        gridContainer.appendChild(card);
    });

    console.log(`Populated ${shootTypesData.length} shoot types (all)`);
}

// Show inline options (Outdoor / Indoor) for a selected shoot type
function showShootOptions(typeName, cardElement) {
    // Remove existing options panels
    document.querySelectorAll('.shoot-options-panel').forEach(el => el.remove());

    const panel = document.createElement('div');
    panel.className = 'shoot-options-panel';
    panel.innerHTML = `
        <button class="env-btn env-btn--outdoor" aria-label="Outdoor Shoot" title="Outdoor" onclick="selectShootType('${typeName}','outdoor')">
            <i class="fas fa-tree"></i>
        </button>
        <button class="env-btn env-btn--indoor" aria-label="Indoor Shoot" title="Indoor" onclick="selectShootType('${typeName}','indoor')">
            <i class="fas fa-home"></i>
        </button>
        <button class="env-btn env-btn--close" aria-label="Close options" title="Close" onclick="this.closest('.shoot-options-panel').remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Insert panel after the clicked card
    cardElement.appendChild(panel);
}

function selectShootType(type, variant) {
    console.log(`Shoot type selected: ${type} (variant: ${variant})`);

    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    if (!isLoggedIn) {
        alert("Please login or register to access AI suggestions.");
        if(loginModal) loginModal.classList.add('active');
        return;
    }

    // Save the selection to LocalStorage
    localStorage.setItem('selectedShootType', type);
    if (variant) localStorage.setItem('selectedCategory', variant);

    // Redirect to the workspace with optional variant param
    const variantParam = variant ? `&variant=${encodeURIComponent(variant)}` : '';
    window.location.href = `/workspace.html?type=${encodeURIComponent(type)}${variantParam}`;
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'index.html';
}

// --- Workspace Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const workspaceTitle = document.getElementById('workspace-title');
    const portfolioGrid = document.getElementById('portfolio-grid');
    
    // Only run this if we are on the workspace page
    if (workspaceTitle) {
        const urlParams = new URLSearchParams(window.location.search);
        const type = urlParams.get('type') || localStorage.getItem('selectedShootType');
        
        if (!type) {
            // If no type selected, go back to dashboard
            window.location.href = '/dashboard.html';
            return;
        }
        
        workspaceTitle.textContent = `${type} Photography Workspace`;
        loadWorkspaceData(type);
    }

    // Only run this if we are on the portfolio page
    if (portfolioGrid) {
        loadPortfolio();
    }
});

async function loadWorkspaceData(type) {
    try {
        const response = await fetch(`/api/workspace-data?type=${encodeURIComponent(type)}`);
        
        if (response.status === 401) {
            alert("Session expired. Please login again to access the workspace.");
            window.location.href = '/';
            return;
        }

        const data = await response.json();

        // Render Rules
        const rulesContainer = document.getElementById('rules-container');
        rulesContainer.innerHTML = '';
        if (data.rules && data.rules.length > 0) {
            data.rules.forEach(rule => {
                rulesContainer.innerHTML += `<div class="rule-card">${rule.rule}</div>`;
            });
        } else {
            rulesContainer.innerHTML = '<p class="text-muted">No specific rules found for this category.</p>';
        }

        // Render Poses
        const posesContainer = document.getElementById('poses-container');
        posesContainer.innerHTML = '';
        if (data.poses && data.poses.length > 0) {
            data.poses.forEach(pose => {
                // Determine image source: Local path or Remote URL
                let imgSrc = pose.image_path ? `/static/${pose.image_path}` : pose.image_url;
                let isFolder = false;

                // Check if it is a Google Drive Folder link
                if (imgSrc && imgSrc.includes('drive.google.com/drive/folders')) {
                    isFolder = true;
                    // Use a generic folder icon for folder links
                    imgSrc = 'https://ssl.gstatic.com/images/branding/product/1x/drive_2020q4_48dp.png';
                }

                posesContainer.innerHTML += `
                    <div class="col-6 mb-3">
                        <div class="card bg-dark text-white">
                            <img src="${imgSrc}" class="pose-img" alt="${pose.name}" style="${isFolder ? 'padding: 20px; object-fit: contain;' : ''}" referrerpolicy="no-referrer" onerror="console.error('Failed to load:', '${imgSrc}'); this.onerror=null; this.src='https://placehold.co/600x400?text=Check+Drive+Permissions'; this.style.opacity='0.5';">
                            <div class="card-footer p-2 text-center small">
                                ${pose.name}
                                ${isFolder ? `<br><a href="${pose.image_url}" target="_blank" class="text-warning">Open Drive Folder</a>` : ''}
                            </div>
                        </div>
                    </div>`;
            });
        } else {
            posesContainer.innerHTML = '<p class="text-muted">No poses uploaded yet for this category.</p>';
        }

    } catch (error) {
        console.error('Error loading workspace data:', error);
    }
}

async function loadPortfolio() {
    const grid = document.getElementById('portfolio-grid');
    try {
        const response = await fetch('/api/poses');
        const poses = await response.json();

        grid.innerHTML = '';

        if (poses.length === 0) {
            grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">No portfolio items found.</p>';
            return;
        }

        poses.forEach(pose => {
            // Determine image source: Local path or Remote URL
            let imgSrc = pose.image_path ? `/static/${pose.image_path}` : pose.image_url;
            let isFolder = false;

            // Check if it is a Google Drive Folder link
            if (imgSrc && imgSrc.includes('drive.google.com/drive/folders')) {
                isFolder = true;
                imgSrc = 'https://ssl.gstatic.com/images/branding/product/1x/drive_2020q4_48dp.png';
            }

            const card = document.createElement('div');
            card.className = 'shoot-card';
            card.innerHTML = `
                <img src="${imgSrc}" class="pose-img" alt="${pose.name}" style="${isFolder ? 'padding: 20px; object-fit: contain;' : ''}" referrerpolicy="no-referrer" onerror="console.error('Failed to load:', '${imgSrc}'); this.onerror=null; this.src='https://placehold.co/600x400?text=Check+Drive+Permissions'; this.style.opacity='0.5';">
                <h3>${pose.name}</h3>
                <p>${pose.shoot_type || 'Portfolio'}</p>
                ${isFolder ? `<a href="${pose.image_url}" target="_blank" style="display:block; text-align:center; margin-bottom:10px; color:var(--primary-color);">Open Drive Folder</a>` : ''}
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading portfolio:', error);
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: red;">Failed to load portfolio items.</p>';
    }
}

// --- Admin Logic (Add Shoot Type) ---
const addShootTypeForm = document.getElementById('add-shoot-type-form');
if (addShootTypeForm) {
    addShootTypeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const typeInput = document.getElementById('new-shoot-type-name');
        const typeName = typeInput.value.trim();

        if (!typeName) {
            alert('Please enter a shoot type name.');
            return;
        }

        try {
            const response = await fetch('/api/shoot-types', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: typeName })
            });

            const data = await response.json();

            if (response.ok) {
                alert(`Shoot type "${typeName}" created successfully!`);
                typeInput.value = '';
                // Refresh the page to show the new type if it's listed
                window.location.reload();
            } else {
                alert(data.error || 'Failed to create shoot type.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Server error while adding shoot type.');
        }
    });
}

// --- Protect AI Features (Camera & Chat) ---
document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    // Check if link points to AI Camera or AI Chat
    if (href && (href.indexOf('camera_ui') !== -1 || href.indexOf('chatbot') !== -1)) {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        
        if (!isLoggedIn) {
            e.preventDefault(); // Prevent navigation
            alert("Please login to access AI features.");
            if (loginModal) {
                loginModal.classList.add('active');
            }
        }
    }
});