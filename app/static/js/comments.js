// ── Collapse / expand news body or any section ────────────────
function toggleSection(sectionId, header) {
  const section = document.getElementById(sectionId);
  const icon    = header.querySelector('.toggle-icon');
  if (!section) return;
  const collapsed = section.style.display === 'none';
  section.style.display = collapsed ? '' : 'none';
  if (icon) icon.innerHTML = collapsed ? '&#9650; Collapse' : '&#9660; Expand';
}

// ── Show / hide remaining comments ───────────────────────────
function toggleRest(btn) {
  const rest = document.getElementById('rest-comments');
  if (!rest) return;
  const collapsed = rest.style.display === 'none';
  rest.style.display = collapsed ? '' : 'none';
  const count = rest.querySelectorAll('.comment-block').length;
  btn.innerHTML = collapsed
    ? '&#9650; Hide extra comments'
    : '&#9660; Show ' + count + ' more comment' + (count > 1 ? 's' : '');
}

// ── Show / hide replies for one comment ──────────────────────
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

// ── Enter reply mode ──────────────────────────────────────────
document.querySelectorAll('.reply-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    const parentId = btn.dataset.id;
    const name     = btn.dataset.name;
    document.getElementById('form-parent-id').value = parentId;
    const hint   = document.getElementById('reply-hint');
    const nameEl = document.getElementById('reply-to-name');
    if (hint)   hint.style.display = 'block';
    if (nameEl) nameEl.textContent = name;
    const textarea = document.getElementById('comment-input');
    if (textarea) {
      textarea.placeholder = 'Replying to ' + name + '…';
      textarea.focus();
      document.querySelector('.card:last-child')
        .scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── Cancel reply mode ─────────────────────────────────────────
function cancelReply(e) {
  e.preventDefault();
  document.getElementById('form-parent-id').value = '';
  const hint = document.getElementById('reply-hint');
  if (hint) hint.style.display = 'none';
  const textarea = document.getElementById('comment-input');
  if (textarea) textarea.placeholder = 'Share your thoughts on this article…';
}

// ── Character counter ─────────────────────────────────────────
const textarea  = document.getElementById('comment-input');
const charCount = document.getElementById('char-count');
if (textarea && charCount) {
  textarea.addEventListener('input', () => {
    const len = textarea.value.length;
    charCount.textContent = len + ' / 1000';
    charCount.style.color = len > 900 ? '#b53b3b' : '#6c757d';
  });
}
function clearComment() {
  if (textarea) {
    textarea.value = '';
    if (charCount) charCount.textContent = '0 / 1000';
    textarea.focus();
  }
}

// ── Like — POST to backend, update DB, show new count ─────────
document.querySelectorAll('.like-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.dataset.liked) return;   // prevent double-click
    const commentId = btn.dataset.id;
    fetch('/comments/' + commentId + '/like', { method: 'POST' })
      .then(r => r.json())
      .then(data => {
        btn.querySelector('.like-num').textContent = data.likes;
        btn.dataset.liked = '1';
        btn.style.color = 'var(--primary)';
      });
  });
});
