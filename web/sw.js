/**
 * O-Nakala Core Service Worker
 * Enables offline functionality and caching for mobile field research
 */

const CACHE_NAME = 'o-nakala-v4.0.0';
const STATIC_CACHE = 'o-nakala-static-v4.0.0';
const DYNAMIC_CACHE = 'o-nakala-dynamic-v4.0.0';

// Files to cache for offline functionality
const STATIC_FILES = [
    '/',
    '/index.html',
    '/template-designer.html',
    '/styles.css',
    '/template-designer.css',
    '/app.js',
    '/template-designer.js',
    '/manifest.json',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.min.js',
    'https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js'
];

// API endpoints that should be cached
const API_CACHE_PATTERNS = [
    /\/api\/v1\/templates/,
    /\/api\/v1\/analytics/,
    /\/api\/v1\/suggestions/
];

// Install event - cache static files
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('Service Worker: Caching static files');
                return cache.addAll(STATIC_FILES.map(url => new Request(url, { mode: 'no-cors' })));
            })
            .catch((error) => {
                console.warn('Service Worker: Cache failed for some files', error);
                // Continue installation even if some files fail to cache
                return Promise.resolve();
            })
    );
    
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                        console.log('Service Worker: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    self.clients.claim();
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Handle different types of requests
    if (isStaticFile(request.url)) {
        event.respondWith(handleStaticFile(request));
    } else if (isAPIRequest(request.url)) {
        event.respondWith(handleAPIRequest(request));
    } else if (isImage(request.url)) {
        event.respondWith(handleImage(request));
    } else {
        event.respondWith(handleOther(request));
    }
});

// Handle static files - cache first strategy
async function handleStaticFile(request) {
    try {
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        
        const response = await fetch(request);
        const cache = await caches.open(STATIC_CACHE);
        cache.put(request, response.clone());
        return response;
    } catch (error) {
        console.warn('Service Worker: Static file failed', error);
        return new Response('Offline', { status: 503 });
    }
}

// Handle API requests - network first with cache fallback
async function handleAPIRequest(request) {
    try {
        const response = await fetch(request);
        
        // Cache successful responses
        if (response.ok && shouldCacheAPI(request.url)) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, response.clone());
        }
        
        return response;
    } catch (error) {
        console.log('Service Worker: API request failed, trying cache');
        
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        
        // Return offline response for failed API requests
        return new Response(JSON.stringify({
            error: 'Offline',
            message: 'This request requires an internet connection',
            offline: true
        }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Handle images - cache with fallback
async function handleImage(request) {
    try {
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        // Return placeholder image for failed image requests
        return new Response(
            '<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#f3f4f6"/><text x="100" y="100" text-anchor="middle" fill="#9ca3af">Image Offline</text></svg>',
            { headers: { 'Content-Type': 'image/svg+xml' } }
        );
    }
}

// Handle other requests - network first
async function handleOther(request) {
    try {
        return await fetch(request);
    } catch (error) {
        const cached = await caches.match(request);
        return cached || new Response('Offline', { status: 503 });
    }
}

// Helper functions
function isStaticFile(url) {
    return STATIC_FILES.some(file => url.includes(file)) ||
           url.includes('.css') ||
           url.includes('.js') ||
           url.includes('.html');
}

function isAPIRequest(url) {
    return url.includes('/api/') || url.includes('localhost:8000');
}

function isImage(url) {
    return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url);
}

function shouldCacheAPI(url) {
    return API_CACHE_PATTERNS.some(pattern => pattern.test(url));
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    console.log('Service Worker: Background sync triggered', event.tag);
    
    if (event.tag === 'background-sync-nakala') {
        event.waitUntil(syncOfflineData());
    }
});

async function syncOfflineData() {
    try {
        // Get offline data from IndexedDB or localStorage
        const offlineActions = await getOfflineActions();
        
        for (const action of offlineActions) {
            try {
                await processOfflineAction(action);
                await removeOfflineAction(action.id);
            } catch (error) {
                console.warn('Failed to sync offline action:', action, error);
            }
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

async function getOfflineActions() {
    // In a real implementation, this would use IndexedDB
    const stored = localStorage.getItem('nakala_offline_actions');
    return stored ? JSON.parse(stored) : [];
}

async function processOfflineAction(action) {
    // Process different types of offline actions
    switch (action.type) {
        case 'template_save':
            return await fetch('/api/v1/templates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(action.data)
            });
        case 'metadata_generation':
            return await fetch('/api/v1/autonomous/generate', {
                method: 'POST',
                body: action.formData
            });
        default:
            console.warn('Unknown offline action type:', action.type);
    }
}

async function removeOfflineAction(actionId) {
    const stored = localStorage.getItem('nakala_offline_actions');
    if (stored) {
        const actions = JSON.parse(stored);
        const filtered = actions.filter(action => action.id !== actionId);
        localStorage.setItem('nakala_offline_actions', JSON.stringify(filtered));
    }
}

// Push notifications for research teams
self.addEventListener('push', (event) => {
    if (!event.data) return;
    
    const data = event.data.json();
    const title = data.title || 'O-Nakala Core';
    const options = {
        body: data.body || 'New update available',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/icon-72x72.png',
        tag: 'nakala-notification',
        requireInteraction: false,
        actions: [
            {
                action: 'view',
                title: 'View',
                icon: '/icons/icon-72x72.png'
            },
            {
                action: 'dismiss',
                title: 'Dismiss'
            }
        ],
        data: data.url || '/'
    };
    
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'view' || !event.action) {
        const url = event.notification.data || '/';
        event.waitUntil(
            clients.openWindow(url)
        );
    }
});

// Handle share target (when files are shared to the app)
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    if (url.pathname === '/' && url.searchParams.has('tab') && event.request.method === 'POST') {
        event.respondWith(handleSharedFile(event.request));
    }
});

async function handleSharedFile(request) {
    const formData = await request.formData();
    const file = formData.get('file');
    
    if (file) {
        // Store the shared file in cache for processing
        const cache = await caches.open(DYNAMIC_CACHE);
        const fileResponse = new Response(file);
        await cache.put('/shared-file-temp', fileResponse);
        
        // Redirect to autonomous generation tab
        return Response.redirect('/?tab=autonomous&shared=true', 302);
    }
    
    return Response.redirect('/', 302);
}

// Periodic background sync for research data
self.addEventListener('periodicsync', (event) => {
    if (event.tag === 'research-data-sync') {
        event.waitUntil(syncResearchData());
    }
});

async function syncResearchData() {
    // Sync research data in background for field researchers
    console.log('Syncing research data in background...');
    
    try {
        // Check for pending uploads
        const pendingUploads = await getPendingUploads();
        
        for (const upload of pendingUploads) {
            await processUpload(upload);
        }
        
        // Update local cache with latest templates
        await updateTemplateCache();
        
    } catch (error) {
        console.error('Research data sync failed:', error);
    }
}

async function getPendingUploads() {
    // Return list of pending uploads from local storage
    const stored = localStorage.getItem('nakala_pending_uploads');
    return stored ? JSON.parse(stored) : [];
}

async function processUpload(upload) {
    // Process individual upload when back online
    console.log('Processing pending upload:', upload.filename);
}

async function updateTemplateCache() {
    // Update template cache with latest data
    try {
        const response = await fetch('/api/v1/templates');
        if (response.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put('/api/v1/templates', response);
        }
    } catch (error) {
        console.warn('Failed to update template cache:', error);
    }
}