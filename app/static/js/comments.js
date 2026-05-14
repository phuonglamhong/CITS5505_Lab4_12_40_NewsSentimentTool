//Toggle article body (collapse/expand)
function toggleArticle(articleId, header) {
  const body  = document.getElementById('article-body-' + articleId);
  const label = document.querySelector('.toggle-label-' + articleId);
  if (!body) return;

  const collapsed = body.style.display === 'none';
  body.style.display = collapsed ? '' : 'none';
  if (label) label.innerHTML = collapsed ? 'Hide &#9650;' : 'Show &#9660;';
}

//Toggle replies                       
function toggleReplies(commentId, btn) {
  const replies = document.getElementById('replies-' + commentId);
  if (!replies) return;
  const collapsed = replies.style.display === 'none';
  replies.style.display = collapsed ? '' : 'none';
  const count = replies.querySelectorAll('.comment-reply').length;
  btn.innerHTML = collapsed
    ? '&#9650; Hide replies'
    : '&#9660; Show ' + count + ' repl' + (count === 1 ? 'y' : 'ies');
}

//Reply trigger                       ─
document.querySelectorAll('.reply-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    const commentId = btn.dataset.id;
    const name      = btn.dataset.name;
    const articleId = btn.dataset.article;

    const form = document.querySelector('.comment-form[data-article-id="' + articleId + '"]');
    if (!form) return;

    form.querySelector('.form-parent-id').value = commentId;

    const hint   = document.getElementById('reply-hint-' + articleId);
    const nameEl = document.querySelector('.reply-to-name-' + articleId);
    if (hint)   hint.style.display = 'block';
    if (nameEl) nameEl.textContent = name;

    const textarea = form.querySelector('.comment-input');
    if (textarea) {
      textarea.placeholder = 'Replying to ' + name + '…';
      textarea.focus();
    }
  });
});

//Cancel reply                        
function cancelReply(e, articleId) {
  e.preventDefault();
  const form = document.querySelector('.comment-form[data-article-id="' + articleId + '"]');
  if (!form) return;
  form.querySelector('.form-parent-id').value = '';
  const hint = document.getElementById('reply-hint-' + articleId);
  if (hint) hint.style.display = 'none';
  const textarea = form.querySelector('.comment-input');
  if (textarea) textarea.placeholder = 'Share your thoughts…';
}

//Character counter                    
document.querySelectorAll('.comment-form').forEach(form => {
  const textarea  = form.querySelector('.comment-input');
  const charCount = form.querySelector('.char-count');
  if (!textarea || !charCount) return;
  textarea.addEventListener('input', () => {
    const len = textarea.value.length;
    charCount.textContent = len + ' / 1000';
    charCount.style.color = len > 900 ? '#b53b3b' : '#6c757d';
  });
});

// Clear form                         
function clearForm(btn) {
  const form      = btn.closest('.comment-form');
  const textarea  = form.querySelector('.comment-input');
  const charCount = form.querySelector('.char-count');
  if (textarea)  textarea.value = '';
  if (charCount) charCount.textContent = '0 / 1000';
  if (textarea)  textarea.focus();
}

//Like                            
document.querySelectorAll('.like-btn').forEach(btn => {
  btn.addEventListener('click', () => {
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

// Submit comment                       
document.querySelectorAll('.comment-form').forEach(form => {
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const textarea  = form.querySelector('.comment-input');
    const content   = textarea.value.trim();
    const parentId  = form.querySelector('.form-parent-id').value || null;
    const articleId = form.dataset.articleId;
    const csrf      = form.querySelector('input[name="csrf_token"]').value;

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
        window.location.reload();
      } else {
        alert(data.message);
      }
    } catch (err) {
      alert('Network error. Please try again.');
    }
  });
});
