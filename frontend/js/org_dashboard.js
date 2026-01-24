// ==================== CONFIG ====================
const CONFIG = {
    API_BASE: "http://127.0.0.1:8000/api",
    ENDPOINTS: {
        WORKSPACES: "/workspace/",
        MEMBERS: "/organization/membership/",
        LOGS: "/activities/activities/",
        ADD_MEMBER : "/organization/membership/"

    }
};

// ==================== STATE ====================
const state = {
    orgSlug: null,

    workspaces: [],
    members: [],
    logs: [],

    loading: false
};

// ==================== API HELPERS ====================

async function refreshAccessToken() {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) throw new Error("No refresh token");

    const res = await fetch(
        "http://127.0.0.1:8000/api/auth/refresh/",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh })
        }
    );

    if (!res.ok) {
        localStorage.clear();
        throw new Error("Session expired");
    }

    const data = await res.json();
    localStorage.setItem("access", data.access);
    if (data.refresh) {
        localStorage.setItem("refresh", data.refresh);
    }

    return data.access;
}


async function fetchJSON(url, headers = {}) {
    let res = await fetch(url, { headers });

    if (res.status === 401) {
        const newAccess = await refreshAccessToken();

        res = await fetch(url, {
            headers: {
                ...headers,
                Authorization: `Bearer ${newAccess}`
            }
        });
    }

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function postJSON(url, body) {
    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...authHeaders({ "X-ORG-SLUG": state.orgSlug })
        },
        body: JSON.stringify(body)
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

function authHeaders(extra = {}) {
    const token = localStorage.getItem("access");
    return token
        ? { Authorization: `Bearer ${token}`, ...extra }
        : extra;
}

// ==================== INIT ====================

async function initOrgDashboard() {
    state.orgSlug = localStorage.getItem("current_org");
    
    if (!state.orgSlug) {
        console.error("No current_org set");
        return;
    }
    
    setLoading(true);
    
    try {
        await Promise.all([
            loadWorkspaces(),
            loadMembers(),
            loadLogs()
        ]);
        
        renderWorkspaces();
        renderMembers();
        renderLogs();
        
    } catch (err) {
        console.error("Org dashboard load failed:", err);
    } finally {
        setLoading(false);
    }
}

// ==================== DATA LOADERS ====================
async function loadWorkspaces() {
    console.log("Fetching workspaces for org:", state.orgSlug);
    
    const res = await fetch(
        `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.WORKSPACES}`,
        {
            headers: authHeaders({ "X-ORG-SLUG": state.orgSlug })
        }
    );
    
    console.log("Workspace response status:", res.status);
    
    const data = await res.json();
    console.log("Workspace response data:", data);
    
    state.workspaces = data;
}


async function loadMembers() {
    state.members = await fetchJSON(
        `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.MEMBERS}`,
        authHeaders({ "X-ORG-SLUG": state.orgSlug })
    );
}

async function loadLogs() {
    state.logs = await fetchJSON(
        `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.LOGS}`,
        authHeaders({ "X-ORG-SLUG": state.orgSlug })
    );
}

// ==================== RENDERERS ====================
function renderWorkspaces() {
    const container = document.getElementById("workspace_container");
    if (!container) return;
    
    container.innerHTML = "";
    
    state.workspaces.forEach(ws => {
        const li = document.createElement("li");
        li.textContent = ws.name;
        li.dataset.slug = ws.slug;
        
        li.addEventListener("click", () => {
            localStorage.setItem("current_workspace", ws.slug);
            window.location.href = "../html/workspace.html";
        });
        
        container.appendChild(li);
    });
}

function renderMembers() {
    const tbody = document.getElementById("users-table-body");
    if (!tbody) return;
    
    tbody.innerHTML = "";
    
    state.members.forEach(user => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
        <td>${user.username}</td>
        <td>${user.email}</td>
        <td>${user.role}</td>
        <td>${user.status}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderLogs() {
    const container = document.getElementById("activity-feed");
    if (!container) return;
    
    container.innerHTML = "";
    
    state.logs.forEach(log => {
        const li = document.createElement("li");
        li.innerHTML = `
        <p>${log.action}</p>
        <span>${log.created_at}</span>
        `;
        container.appendChild(li);
    });
}

// ==================== CREATE WORKSPACE ====================
function setupCreateWorkspace() {
    const createBtn = document.getElementById("create-workspace-btn");
    const modal = document.getElementById("create-workspace-modal");
    const submitBtn = document.getElementById("create-workspace-submit");
    const cancelBtn = document.getElementById("create-workspace-cancel");
    const nameInput = document.getElementById("workspace-name-input");
    
    if (!createBtn || !modal) return;
    
    createBtn.addEventListener("click", () => {
        modal.style.display = "block";
        nameInput.value = "";
        nameInput.focus();
    });
    
    cancelBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });
    
    submitBtn.addEventListener("click", async () => {
        const name = nameInput.value.trim();
        if (!name) return alert("Workspace name required");
        
        submitBtn.disabled = true;
        
        try {
            await postJSON(
                `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.WORKSPACES}`,
                { name }
            );
            
            await loadWorkspaces();
            renderWorkspaces();
            
            modal.style.display = "none";
        } catch (err) {
            console.error("Create workspace failed:", err);
            alert("Failed to create workspace");
        } finally {
            submitBtn.disabled = false;
        }
    });
}
function setupAddMember() {
    const btn = document.getElementById("add-member-btn");
    const modal = document.getElementById("add-member-modal");
    const cancel = document.getElementById("add-member-cancel");
    const submit = document.getElementById("add-member-submit");

    const emailInput = document.getElementById("member-email-input");
    const roleInput = document.getElementById("member-role-input");

    if (!btn || !modal) return;

    btn.addEventListener("click", () => {
        modal.style.display = "block";
        emailInput.value = "";
        roleInput.value = "member";
        emailInput.focus();
    });

    cancel.addEventListener("click", () => {
        modal.style.display = "none";
    });

    modal.addEventListener("click", e => {
        if (e.target === modal) modal.style.display = "none";
    });

    submit.addEventListener("click", async () => {
        const email = emailInput.value.trim();
        const role = roleInput.value;

        if (!email) return alert("Email required");

        submit.disabled = true;

        try {
            await postJSON(
                `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.ADD_MEMBER}`,
                { email, role }
            );

            await loadMembers();
            renderMembers();

            modal.style.display = "none";
        } catch (err) {
            console.error("Add member failed:", err);
            alert("Failed to add member");
        } finally {
            submit.disabled = false;
        }
    });
}


// ==================== UI STATE ====================
function setLoading(isLoading) {
    state.loading = isLoading;
    document.body.classList.toggle("loading", isLoading);
}

document.addEventListener("DOMContentLoaded", () => {
    initOrgDashboard();
    setupCreateWorkspace();
     setupAddMember();

    //     // CREATE WORKSPACE
    // document.getElementById("create-workspace-submit")?.addEventListener("click", async () => {
    //     const input = document.getElementById("workspace-name-input");
    //     const name = input.value.trim();
    //     if (!name || !state.activeOrgSlug) return;

    //     await postJSON(
    //         `${CONFIG.API_BASE}${CONFIG.ENDPOINTS.WORKSPACE_CREATE}`,
    //         { name },
    //         authHeaders({ "X-ORG-SLUG": state.OrgSlug })
    //     );

    //     input.value = "";
    //     await loadWorkspaces();
    //     renderWorkspaces();
    // });
});

