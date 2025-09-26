// Gestione tema scuro/chiaro
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeNavigation();
    initializeFlashMessages();
    initializeModals();
    initializeTooltips();
    initializeCharts();
});

// === GESTIONE TEMA ===
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.querySelector('.theme-toggle-icon');

    if (!themeToggle) return;

    // Carica tema salvato
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const themeIcon = document.querySelector('.theme-toggle-icon');
    if (themeIcon) {
        themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// === GESTIONE NAVIGAZIONE MOBILE ===
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (!hamburger || !navMenu) return;

    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Chiudi menu quando si clicca su un link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Chiudi menu quando si clicca fuori
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navMenu.contains(event.target);
        const isClickOnHamburger = hamburger.contains(event.target);

        if (!isClickInsideNav && !isClickOnHamburger && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
}

// === GESTIONE MESSAGGI FLASH ===
function initializeFlashMessages() {
    // Auto-chiudi messaggi dopo 5 secondi
    document.querySelectorAll('.flash-message').forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.opacity = '0';
                message.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });

    // Gestione click su pulsante chiudi
    document.querySelectorAll('.flash-close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });
}

// === GESTIONE MODAL ===
function initializeModals() {
    // Chiudi modal con tasto ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeAllModals();
        }
    });

    // Chiudi modal cliccando fuori
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal(modal.id);
            }
        });
    });

    // Chiudi modal con pulsante X
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                closeModal(modal.id);
            }
        });
    });
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// === GESTIONE TOOLTIP ===
function initializeTooltips() {
    // Aggiungi tooltip per elementi con data-tooltip
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltipText = element.getAttribute('data-tooltip');

    if (!tooltipText) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.cssText = `
        position: absolute;
        background-color: var(--text-primary);
        color: var(--background);
        padding: 0.5rem;
        border-radius: var(--radius);
        font-size: 0.875rem;
        z-index: 1000;
        white-space: nowrap;
        pointer-events: none;
    `;

    document.body.appendChild(tooltip);

    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';

    element._tooltip = tooltip;
}

function hideTooltip(event) {
    const element = event.target;
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// === GESTIONE GRAFICI (semplici) ===
function initializeCharts() {
    // Crea grafici semplici senza librerie esterne
    createSpendingChart();
    createMaintenanceFrequencyChart();
}

function createSpendingChart() {
    const chartContainer = document.getElementById('spendingChart');
    if (!chartContainer) return;

    // Ottieni dati dalle API o dal DOM
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.spese_per_mese && Object.keys(data.spese_per_mese).length > 0) {
                renderSimpleChart(chartContainer, data.spese_per_mese, 'Spese per mese');
            }
        })
        .catch(error => console.error('Errore nel caricamento dei dati:', error));
}

function createMaintenanceFrequencyChart() {
    const chartContainer = document.getElementById('maintenanceChart');
    if (!chartContainer) return;

    // Simula dati di frequenza manutenzioni
    const maintenanceData = getMaintenanceFrequencyData();
    if (Object.keys(maintenanceData).length > 0) {
        renderSimpleChart(chartContainer, maintenanceData, 'Manutenzioni per tipo');
    }
}

function getMaintenanceFrequencyData() {
    const maintenanceItems = document.querySelectorAll('.maintenance-item');
    const frequencyData = {};

    maintenanceItems.forEach(item => {
        const tipo = item.querySelector('.maintenance-title h3')?.textContent;
        if (tipo) {
            frequencyData[tipo] = (frequencyData[tipo] || 0) + 1;
        }
    });

    return frequencyData;
}

function renderSimpleChart(container, data, title) {
    const maxValue = Math.max(...Object.values(data));
    const entries = Object.entries(data);

    container.innerHTML = `
        <div class="chart-title">${title}</div>
        <div class="chart-bars">
            ${entries.map(([label, value]) => `
                <div class="chart-bar-container">
                    <div class="chart-bar" style="height: ${(value / maxValue) * 100}%">
                        <span class="chart-value">${typeof value === 'number' ?
                            (value % 1 === 0 ? value : value.toFixed(2)) : value}</span>
                    </div>
                    <div class="chart-label">${label}</div>
                </div>
            `).join('')}
        </div>
    `;

    // Aggiungi stili per il grafico
    const style = document.createElement('style');
    style.textContent = `
        .chart-title {
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }
        .chart-bars {
            display: flex;
            gap: 1rem;
            align-items: flex-end;
            height: 200px;
        }
        .chart-bar-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100%;
        }
        .chart-bar {
            background-color: var(--primary-color);
            width: 100%;
            min-height: 20px;
            border-radius: var(--radius) var(--radius) 0 0;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            position: relative;
            transition: background-color 0.2s;
        }
        .chart-bar:hover {
            background-color: var(--primary-hover);
        }
        .chart-value {
            color: white;
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.25rem;
        }
        .chart-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-align: center;
            margin-top: 0.5rem;
            word-break: break-word;
        }
    `;

    if (!document.getElementById('chart-styles')) {
        style.id = 'chart-styles';
        document.head.appendChild(style);
    }
}

// === UTILITÀ PER API ===
function fetchWithErrorHandling(url, options = {}) {
    return fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .catch(error => {
        console.error('Fetch error:', error);
        showNotification('Errore di connessione', 'error');
        throw error;
    });
}

// === NOTIFICHE ===
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    // Stili per le notifiche
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: var(--radius);
        color: white;
        font-weight: 500;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 1rem;
        min-width: 300px;
        max-width: 500px;
        box-shadow: var(--shadow-lg);
        animation: slideInRight 0.3s ease-out;
    `;

    switch (type) {
        case 'success':
            notification.style.backgroundColor = 'var(--success-color)';
            break;
        case 'error':
            notification.style.backgroundColor = 'var(--danger-color)';
            break;
        case 'warning':
            notification.style.backgroundColor = 'var(--warning-color)';
            break;
        default:
            notification.style.backgroundColor = 'var(--primary-color)';
    }

    document.body.appendChild(notification);

    // Rimuovi automaticamente dopo il tempo specificato
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
}

// === VALIDAZIONE FORM ===
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    const errors = [];

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            errors.push(`Il campo "${field.labels[0]?.textContent || field.name}" è obbligatorio`);
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });

    // Validazioni specifiche
    const emailFields = formElement.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            isValid = false;
            errors.push('Inserisci un indirizzo email valido');
            field.classList.add('error');
        }
    });

    const numberFields = formElement.querySelectorAll('input[type="number"]');
    numberFields.forEach(field => {
        if (field.value && isNaN(field.value)) {
            isValid = false;
            errors.push(`Il campo "${field.labels[0]?.textContent || field.name}" deve essere un numero`);
            field.classList.add('error');
        }
    });

    if (!isValid) {
        errors.forEach(error => showNotification(error, 'error'));
    }

    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// === GESTIONE RICERCA E FILTRI ===
function setupSearch(inputSelector, itemsSelector, searchableSelector) {
    const searchInput = document.querySelector(inputSelector);
    const items = document.querySelectorAll(itemsSelector);

    if (!searchInput || !items.length) return;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();

        items.forEach(item => {
            const searchableElements = item.querySelectorAll(searchableSelector);
            const text = Array.from(searchableElements)
                .map(el => el.textContent.toLowerCase())
                .join(' ');

            if (text.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });

        // Aggiorna contatori se presenti
        updateSearchResults(items, searchTerm);
    });
}

function updateSearchResults(items, searchTerm) {
    const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
    const resultCounter = document.querySelector('.search-results-count');

    if (resultCounter) {
        resultCounter.textContent = `${visibleItems.length} risultati`;
    }

    // Evidenzia termini di ricerca
    if (searchTerm) {
        highlightSearchTerms(visibleItems, searchTerm);
    } else {
        removeHighlights();
    }
}

function highlightSearchTerms(items, term) {
    const regex = new RegExp(`(${term})`, 'gi');

    items.forEach(item => {
        const textNodes = getTextNodes(item);
        textNodes.forEach(node => {
            if (node.nodeValue.toLowerCase().includes(term)) {
                const highlightedHTML = node.nodeValue.replace(regex, '<mark>$1</mark>');
                const wrapper = document.createElement('span');
                wrapper.innerHTML = highlightedHTML;
                node.parentNode.replaceChild(wrapper, node);
            }
        });
    });
}

function removeHighlights() {
    document.querySelectorAll('mark').forEach(mark => {
        mark.replaceWith(mark.textContent);
    });
}

function getTextNodes(element) {
    const textNodes = [];
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    while (walker.nextNode()) {
        textNodes.push(walker.currentNode);
    }

    return textNodes;
}

// === GESTIONE ORDINAMENTO ===
function setupSorting(tableSelector, sortableColumns) {
    const table = document.querySelector(tableSelector);
    if (!table) return;

    sortableColumns.forEach(column => {
        const header = table.querySelector(`th[data-sort="${column}"]`);
        if (header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => sortTable(table, column));
        }
    });
}

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelector(`th[data-sort="${column}"]`);

    const isAscending = !header.classList.contains('sort-asc');

    // Reset altri header
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Aggiungi classe al header corrente
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    rows.sort((a, b) => {
        const aValue = a.querySelector(`td[data-sort="${column}"]`)?.textContent || '';
        const bValue = b.querySelector(`td[data-sort="${column}"]`)?.textContent || '';

        if (isNumeric(aValue) && isNumeric(bValue)) {
            return isAscending ?
                parseFloat(aValue) - parseFloat(bValue) :
                parseFloat(bValue) - parseFloat(aValue);
        }

        return isAscending ?
            aValue.localeCompare(bValue) :
            bValue.localeCompare(aValue);
    });

    // Riordina le righe
    rows.forEach(row => tbody.appendChild(row));
}

function isNumeric(str) {
    return !isNaN(str) && !isNaN(parseFloat(str));
}

// === GESTIONE STORAGE LOCALE ===
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Errore nel salvataggio in localStorage:', error);
    }
}

function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : defaultValue;
    } catch (error) {
        console.error('Errore nel caricamento da localStorage:', error);
        return defaultValue;
    }
}

// === UTILITÀ PER FORMATTAZIONE ===
function formatCurrency(amount) {
    return new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatKilometers(km) {
    return new Intl.NumberFormat('it-IT').format(km) + ' km';
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('it-IT');
}

// === GESTIONE ERRORI GLOBALI ===
window.addEventListener('error', function(event) {
    console.error('Errore JavaScript:', event.error);
    showNotification('Si è verificato un errore. Ricarica la pagina se il problema persiste.', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Promise rejection non gestita:', event.reason);
    showNotification('Errore di connessione. Controlla la tua connessione internet.', 'error');
});

// === ANIMAZIONI CSS PERSONALIZZATE ===
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .form-input.error,
    .form-select.error,
    .form-textarea.error {
        border-color: var(--danger-color);
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
    }

    .notification-close {
        background: none;
        border: none;
        color: inherit;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0;
    }

    th.sort-asc::after {
        content: ' ▲';
        color: var(--primary-color);
    }

    th.sort-desc::after {
        content: ' ▼';
        color: var(--primary-color);
    }

    mark {
        background-color: var(--warning-color);
        color: white;
        padding: 0.125rem 0.25rem;
        border-radius: 2px;
    }
`;

if (!document.getElementById('script-styles')) {
    style.id = 'script-styles';
    document.head.appendChild(style);
}

// === ESPORTA FUNZIONI GLOBALI ===
window.MaintenanceApp = {
    showNotification,
    validateForm,
    formatCurrency,
    formatKilometers,
    formatDate,
    saveToLocalStorage,
    loadFromLocalStorage,
    setupSearch,
    setupSorting
};