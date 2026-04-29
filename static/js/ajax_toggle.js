function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    // Set initial button colors based on data-present attribute
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        const isPresent = btn.dataset.present === 'True';
        setButtonState(btn, isPresent);
    });

    // Attach click handlers
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const pid = btn.dataset.pid;
            const sid = btn.dataset.sid;

            fetch(`/attend/${pid}/${sid}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                setButtonState(btn, data.present);
                btn.dataset.present = data.present ? 'True' : 'False';
            })
            .catch(err => {
                console.error('Toggle failed:', err);
                btn.textContent = 'Error';
                btn.className = 'toggle-btn btn btn-sm btn-danger';
            });
        });
    });
});

function setButtonState(btn, isPresent) {
    if (isPresent) {
        btn.textContent = 'Present';
        btn.className = 'toggle-btn btn btn-sm btn-success';
    } else {
        btn.textContent = 'Absent';
        btn.className = 'toggle-btn btn btn-sm btn-outline-secondary';
    }
}