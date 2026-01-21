// API Configuration
const API_BASE_URL = "http://127.0.0.1:8000";

const API_ENDPOINTS = {
    auth: {
        login: '/api/auth/login',
        signup: '/api/auth/signup',
        refresh: '/api/auth/refresh',
        verify: (uidb64, token) => `/api/auth/verify/${uidb64}/${token}`
    },
    organizations: {
        list: '/api/organization/list',
        create: '/api/organization/create',
        update: '/api/organization/update',
        delete: (orgId) => `/api/organization/delete/${orgId}`,
        archive: '/api/organization/archive'
    },
    workspaces: {
        list: '/api/workspace/',
        create: '/api/workspace/'
    },
    boards: {
        list: (workspaceId) => `/api/board/workspaces/${workspaceId}/boards/`,
        create: (workspaceId) => `/api/board/workspaces/${workspaceId}/boards/`
    },
    cards: {
        list: (boardId) => `/api/card/boards/${boardId}/cards/`,
        create: (boardId) => `/api/card/boards/${boardId}/cards/`
    },
    activities: {
        org: '/api/activities/activities/',
        entity: (entityId) => `/api/activities/entities/${entityId}/activities/`
    },
    invitations: {
        invite: '/invites/invite',
        accept: '/invites/accept'
    }
};

// Token Management
class TokenManager {
    static getAccessToken() {
        return localStorage.getItem('access_token');
    }

    static getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    static setTokens(accessToken, refreshToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
    }

    static clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('current_org_slug');
    }

    static isAuthenticated() {
        return !!this.getAccessToken();
    }
}

// Organization Management
class OrganizationManager {
    static getCurrentOrg() {
        return localStorage.getItem('current_org_slug');
    }

    static setCurrentOrg(orgSlug) {
        localStorage.setItem('current_org_slug', orgSlug);
    }

    static clearCurrentOrg() {
        localStorage.removeItem('current_org_slug');
    }
}

// API Client
class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = TokenManager.getAccessToken();
        const orgSlug = OrganizationManager.getCurrentOrg();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        if (orgSlug) {
            headers['X-ORG-SLUG'] = orgSlug;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);
            
            // Handle token refresh on 401
            if (response.status === 401 && token) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    // Retry original request with new token
                    headers['Authorization'] = `Bearer ${TokenManager.getAccessToken()}`;
                    return fetch(url, { ...config, headers });
                } else {
                    // Redirect to login
                    window.location.href = '/login.html';
                    return response;
                }
            }

            return response;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    async refreshToken() {
        const refreshToken = TokenManager.getRefreshToken();
        if (!refreshToken) {
            return false;
        }

        try {
            const response = await fetch(`${this.baseURL}${API_ENDPOINTS.auth.refresh}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                TokenManager.setTokens(data.access, data.refresh);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Token refresh error:', error);
            return false;
        }
    }

    async get(endpoint) {
        const response = await this.request(endpoint, { method: 'GET' });
        return this.handleResponse(response);
    }

    async post(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    async put(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    async delete(endpoint) {
        const response = await this.request(endpoint, { method: 'DELETE' });
        return this.handleResponse(response);
    }

    async handleResponse(response) {
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || data.detail || 'Request failed');
            }
            return data;
        } else {
            if (!response.ok) {
                throw new Error('Request failed');
            }
            return null;
        }
    }
}

// Create global API client instance
const api = new APIClient();

// Auth API
const authAPI = {
    async login(email, password) {
        const data = await api.post(API_ENDPOINTS.auth.login, { email, password });
        TokenManager.setTokens(data.access, data.refresh);
        return data;
    },

    async signup(username, email, password) {
        return await api.post(API_ENDPOINTS.auth.signup, { username, email, password });
    },

    async verifyEmail(uidb64, token) {
        return await api.get(API_ENDPOINTS.auth.verify(uidb64, token));
    },

    logout() {
        TokenManager.clearTokens();
        OrganizationManager.clearCurrentOrg();
        window.location.href = '/login.html';
    }
};

// Organizations API
const orgAPI = {
    async list() {
        return await api.get(API_ENDPOINTS.organizations.list);
    },

    async create(name, type) {
        return await api.post(API_ENDPOINTS.organizations.create, { name, type });
    },

    async update(slug, name) {
        return await api.put(API_ENDPOINTS.organizations.update, { slug, name });
    },

    async delete(orgId) {
        return await api.delete(API_ENDPOINTS.organizations.delete(orgId));
    },

    async archive(slug) {
        return await api.put(API_ENDPOINTS.organizations.archive, { slug });
    }
};

// Workspaces API
const workspaceAPI = {
    async list() {
        return await api.get(API_ENDPOINTS.workspaces.list);
    },

    async create(name) {
        return await api.post(API_ENDPOINTS.workspaces.create, { name });
    }
};

// Boards API
const boardAPI = {
    async list(workspaceId) {
        return await api.get(API_ENDPOINTS.boards.list(workspaceId));
    },

    async create(workspaceId, name) {
        return await api.post(API_ENDPOINTS.boards.create(workspaceId), { name });
    }
};

// Cards API
const cardAPI = {
    async list(boardId) {
        return await api.get(API_ENDPOINTS.cards.list(boardId));
    },

    async create(boardId, title, description = '') {
        return await api.post(API_ENDPOINTS.cards.create(boardId), { title, description });
    }
};

// Activities API
const activityAPI = {
    async listOrg(limit = 50) {
        return await api.get(`${API_ENDPOINTS.activities.org}?limit=${limit}`);
    },

    async listEntity(entityId, limit = 50) {
        return await api.get(`${API_ENDPOINTS.activities.entity(entityId)}?limit=${limit}`);
    }
};

// Invitations API
const invitationAPI = {
    async invite(email, role) {
        return await api.post(API_ENDPOINTS.invitations.invite, { email, role });
    },

    async accept(token) {
        return await api.post(API_ENDPOINTS.invitations.accept, { token });
    }
};

// Utility Functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function showLoading(element) {
    element.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';
}

function hideLoading(element) {
    // Remove loading state
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { api, authAPI, orgAPI, workspaceAPI, boardAPI, cardAPI, activityAPI, invitationAPI, TokenManager, OrganizationManager, showAlert, formatDate };
}


