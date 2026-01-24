    /**
     * ==========================================
     * SECTION 1: MANDATORY EXISTING LOGIC
     * ⚠️ DO NOT MODIFY THIS BLOCK ⚠️
     * ==========================================
     */

    // Mocking fetchJSON for demonstration since API is not reachable here.
    // In production, this wrapper is likely provided by the environment.
    // I am assuming fetchJSON exists globally or is imported. 
    // If not, this polyfill ensures the code runs for verification.

    const API_BASE = "http://127.0.0.1:8000/api";
    const workspaceSlug = localStorage.getItem("current_workspace");
const orgSlug = localStorage.getItem("current_org");
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

    function fetchNotes() {
    return fetchJSON(`${API_BASE}/notes/workspaces/${workspaceSlug}/notes/`);
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
        li.dataset.slug = note.slug
        list.appendChild(li);
    });
}

    /**
     * ==========================================
     * SECTION 2: SAFE UI ENHANCEMENTS
     * Additive logic to handle Split View interactions
     * ==========================================
     */

    document.addEventListener("DOMContentLoaded", () => {
        
        // 1. Initialize data
        initNotesPage();

        // 2. Set up Event Delegation
        // We listen on the parent #notes-list because renderNotes() wipes the children.
        const notesListEl = document.getElementById("notes-list");
        
        notesListEl.addEventListener("click", (e) => {
            // Find the closest list item clicked
            const li = e.target.closest("li");
            
            // Validation: Must be an LI and must have data (ignore "No notes found")
            if (!li || !li.dataset.slug) return;

            handleNoteSelection(li);
        });
    });

    async function initNotesPage() {
        try {
            const notes = await fetchNotes();
            renderNotes(notes);
            
            // Optional: Auto-select first note if available (UX improvement)
            const firstNote = document.querySelector("#notes-list li[data-slug]");
            if(firstNote) {
                // Uncomment line below to auto-open first note
                // handleNoteSelection(firstNote);
            }
        } catch (error) {
            console.error("Failed to load notes", error);
            document.getElementById("notes-list").innerHTML = "<li style='color:red; padding:12px;'>Error loading notes.</li>";
        }
    }

    function handleNoteSelection(liElement) {
        // A. Visual Selection Logic
        // Remove active class from all items
        document.querySelectorAll("#notes-list li").forEach(el => el.classList.remove("active-note"));
        // Add active class to clicked item
        liElement.classList.add("active-note");

        // B. Data Extraction Logic
        // Since we cannot modify the Note Object logic, we parse the rendered DOM 
        // which serves as our source of truth here.
        
        const titleEl = liElement.querySelector("strong");
        // We get the HTML content. 
        // Note: The existing logic puts Title + <br> + Content in the LI.
        // We need to carefully extract just the content part to avoid duplicating the title in the view.
        
        const rawHTML = liElement.innerHTML;
        const titleText = titleEl ? titleEl.innerText : "Untitled";
        
        // Split on the first <br> to separate Title from Content roughly, 
        // or just use the full innerHTML minus the strong tag.
        // A robust way using DOM nodes:
        const clone = liElement.cloneNode(true);
        const strongInClone = clone.querySelector("strong");
        if(strongInClone) strongInClone.remove(); // Remove title from body content
        
        // Clean up leading <br> tags left over from the original template
        let contentHtml = clone.innerHTML.trim();
        while(contentHtml.startsWith("<br>")) {
            contentHtml = contentHtml.substring(4).trim();
        }

        // C. Populate View Pane
        const viewContainer = document.getElementById("active-note-view");
        const emptyState = document.getElementById("empty-state");
        const displayTitle = document.getElementById("note-display-title");
        const displayBody = document.getElementById("note-display-body");

        // Toggle visibility
        emptyState.classList.add("hidden");
        viewContainer.classList.remove("hidden");

        // Inject Content
        displayTitle.innerText = titleText;
        displayBody.innerHTML = contentHtml;
    }
    