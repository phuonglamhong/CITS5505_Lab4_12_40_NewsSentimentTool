// COMMENT UI SCRIPT — Handles article interactions, replies, likes, and submissions

// Shows or hides full article body and updates toggle label accordingly.
function toggleArticle(articleId, header) {
  const body = document.getElementById('article-body-' + articleId);
  const label = document.querySelector('.toggle-label-' + articleId);
  if (!body) return;

  const collapsed = body.style.display === 'none';
  // Toggle visibility
  body.style.display = collapsed ? '' : 'none';
  // Update UI label to reflect current state
  if (label) label.innerHTML = collapsed ? 'Hide &#9650;' : 'Show &#9660;';
}

// Expands or collapses replies under a comment and updates button text.                    
function toggleReplies(commentId, btn) {
  const replies = document.getElementById('replies-' + commentId);
  if (!replies) return;
  const collapsed = replies.style.display === 'none';
  replies.style.display = collapsed ? '' : 'none';
  // Count replies for dynamic label
  const count = replies.querySelectorAll('.comment-reply').length;
  btn.innerHTML = collapsed
    ? '&#9650; Hide replies'
    : '&#9660; Show ' + count + ' repl' + (count === 1 ? 'y' : 'ies');
}

// When user clicks 'Reply', sets parent comment ID, updates UI hint and focuses input field.                     ─
document.querySelectorAll('.reply-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    const commentId = btn.dataset.id;
    const name = btn.dataset.name;
    const articleId = btn.dataset.article;

    const form = document.querySelector('.comment-form[data-article-id="' + articleId + '"]');
    if (!form) return;

    // Set parent comment ID for threaded reply
    form.querySelector('.form-parent-id').value = commentId;

    // Show "replying to" UI hint
    const hint = document.getElementById('reply-hint-' + articleId);
    const nameEl = document.querySelector('.reply-to-name-' + articleId);
    if (hint) hint.style.display = 'block';
    if (nameEl) nameEl.textContent = name;

    // Update textarea UX
    const textarea = form.querySelector('.comment-input');
    if (textarea) {
      textarea.placeholder = 'Replying to ' + name + '…';
      textarea.focus();
    }
  });
});

// Clears reply state and restores normal comment mode.                      
function cancelReply(e, articleId) {
  e.preventDefault();
  const form = document.querySelector('.comment-form[data-article-id="' + articleId + '"]');
  if (!form) return;
  // Reset parent comment reference
  form.querySelector('.form-parent-id').value = '';
  // Hide reply UI hint
  const hint = document.getElementById('reply-hint-' + articleId);
  if (hint) hint.style.display = 'none';
  // Reset placeholder
  const textarea = form.querySelector('.comment-input');
  if (textarea) textarea.placeholder = 'Share your thoughts…';
}

// Updates live character count and highlights when near limit.                  
document.querySelectorAll('.comment-form').forEach(form => {
  const textarea = form.querySelector('.comment-input');
  const charCount = form.querySelector('.char-count');
  if (!textarea || !charCount) return;
  textarea.addEventListener('input', () => {
    const len = textarea.value.length;
    charCount.textContent = len + ' / 1000';
    // Warning color when approaching limit
    charCount.style.color = len > 900 ? '#b53b3b' : '#6c757d';
  });
});

// Resets textarea and character counter.                        
function clearForm(btn) {
  const form = btn.closest('.comment-form');
  const textarea = form.querySelector('.comment-input');
  const charCount = form.querySelector('.char-count');
  if (textarea) textarea.value = '';
  if (charCount) charCount.textContent = '0 / 1000';
  if (textarea) textarea.focus();
}

// Sends like request once per session and updates UI dynamically.                           
document.querySelectorAll('.like-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    // Prevent multiple likes from same client session
    if (btn.dataset.liked) return;
    const commentId = btn.dataset.id;
    const csrf = document.getElementById('csrf-global')?.value || '';
    fetch('/comment/' + commentId + '/like', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrf }
    })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          btn.querySelector('.like-num').textContent = data.likes;
          btn.dataset.liked = '1';
          btn.style.color = 'var(--accent)';
        }
      });
  });
});

// Sends comment or reply to backend and reloads page on success.                      
document.querySelectorAll('.comment-form').forEach(form => {
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const textarea = form.querySelector('.comment-input');
    const content = textarea.value.trim();
    const parentId = form.querySelector('.form-parent-id').value || null;
    const articleId = form.dataset.articleId;
    const csrf = form.querySelector('input[name="csrf_token"]').value;

    // Prevent empty submissions
    if (!content) return;

    try {
      const res = await fetch('/article/' + articleId + '/comment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf
        },
        body: JSON.stringify({ content, parent_id: parentId })
      });
      const data = await res.json();
      if (data.status === 'success') {
        // Simple refresh to reflect new comment tree
        window.location.reload();
      } else {
        alert(data.message);
      }
    } catch (err) {
      alert('Network error. Please try again.');
    }
  });
});
