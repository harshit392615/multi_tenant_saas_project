// ---------------- CONFIG ----------------
const API_BASE = "http://127.0.0.1:8000/api";

// ---------------- STATE ----------------
const workspaceSlug = localStorage.getItem("current_workspace");
const orgSlug = localStorage.getItem("current_org");

// ---------------- HELPERS ----------------
function getHeaders() {
    const token = localStorage.getItem("access");

    if (!token || !orgSlug) {
        throw new Error("Missing auth or org context");
    }

    return {
        "Authorization": `Bearer ${token}`,
        "X-ORG-SLUG": orgSlug
    };
}

async function fetchJSON(url) {
    const response = await fetch(url, {
        headers: getHeaders()
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
}

async function postJSON(url, body) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getHeaders()
        },
        body: JSON.stringify(body)
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
}


// ---------------- FETCH FUNCTIONS ----------------
function fetchBoards() {
    return fetchJSON(`${API_BASE}/board/workspaces/${workspaceSlug}/boards/`);
}

function fetchNotes() {
    return fetchJSON(`${API_BASE}/notes/workspaces/${workspaceSlug}/notes/`);
}

function createBoard(name) {
    return postJSON(
        `${API_BASE}/board/workspaces/${workspaceSlug}/boards/`,
        { name }
    );
}

function createNote(title, content) {
    return postJSON(
        `${API_BASE}/notes/workspaces/${workspaceSlug}/notes/`,
        { title, content }
    );
}


// ---------------- RENDER FUNCTIONS ----------------
function renderBoards(boards) {
    const list = document.getElementById("boards-list");
    list.innerHTML = "";

    if (!boards.length) {
        list.innerHTML = "<li>No boards found</li>";
        return;
    }

    boards.forEach(board => {
        const li = document.createElement("li");
        li.textContent = board.name;
        list.appendChild(li);
    });
}

function renderNotes(notes) {
    const list = document.getElementById("notes-list");
    list.innerHTML = "";

    if (!notes.length) {
        list.innerHTML = "<li>No notes found</li>";
        return;
    }

    notes.forEach(note => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${note.title}</strong><br>
            ${note.content}
        `;
        list.appendChild(li);
    });
}

// ---------------- INIT ----------------
async function initWorkspaceDashboard() {
    if (!workspaceSlug) {
        alert("No workspace selected");
        return;
    }

    try {
        const [boards, notes] = await Promise.all([
            fetchBoards(),
            fetchNotes()
        ]);

        renderBoards(boards);
        renderNotes(notes);

        setupCreateBoard();
        setupCreateNote();

    } catch (err) {
        console.error("Workspace load failed:", err);
        alert("Failed to load workspace data");
    }
}


function setupCreateBoard() {
    const input = document.getElementById("board-name-input");
    const btn = document.getElementById("create-board-btn");

    if (!input || !btn) return;

    btn.addEventListener("click", async () => {
        const name = input.value.trim();
        if (!name) return alert("Board name required");

        btn.disabled = true;

        try {
            await createBoard(name);
            input.value = "";

            const boards = await fetchBoards();
            renderBoards(boards);

        } catch (err) {
            console.error("Create board failed:", err);
            alert("Failed to create board");
        } finally {
            btn.disabled = false;
        }
    });
}

function setupCreateNote() {
    const titleInput = document.getElementById("note-title-input");
    const contentInput = document.getElementById("note-content-input");
    const btn = document.getElementById("create-note-btn");

    if (!titleInput || !contentInput || !btn) return;

    btn.addEventListener("click", async () => {
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();

        if (!title || !content) {
            return alert("Title and content required");
        }

        btn.disabled = true;

        try {
            await createNote(title, content);

            titleInput.value = "";
            contentInput.value = "";

            const notes = await fetchNotes();
            renderNotes(notes);

        } catch (err) {
            console.error("Create note failed:", err);
            alert("Failed to create note");
        } finally {
            btn.disabled = false;
        }
    });
}

document.addEventListener("DOMContentLoaded", initWorkspaceDashboard());
