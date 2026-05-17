// Deselect all brands
function selectNone() {
    document.querySelectorAll('.brand-checkbox').forEach(function(cb) {
        cb.checked = false;
    });
}

// Store chart instance globally
let chart;

// Filter brand rows by search input
function filterBrands() {
    var query = document.getElementById('brand-search').value.toLowerCase();
    var rows = document.querySelectorAll('.brand-row');
    rows.forEach(function(row) {
        var name = row.dataset.brand.toLowerCase();
        row.style.display = name.includes(query) ? '' : 'none';
    });
}

// Select all brand checkboxes
function selectAll() {
    document.querySelectorAll('.brand-checkbox').forEach(function(cb) {
        cb.checked = true;
    });
    applyFilter();
}

// Apply selected brands filter and reload data
function applyFilter() {
    var selected = [];
    document.querySelectorAll('.brand-checkbox:checked').forEach(function(cb) {
        selected.push(cb.value);
    });
    loadData(selected);
}

// Render brand sentiment cards
function renderBrands(data) {
    var brandList = document.getElementById('brand-list');
    if (!brandList) return;
    brandList.innerHTML = '';

    if (data.length === 0) {
        brandList.innerHTML = '<p class="text-muted text-center p-3">No brands selected.</p>';
        return;
    }

    data.forEach(function(brand) {
        var card = document.createElement('div');
        card.className = 'brand-row border rounded p-3 mb-3';
        card.dataset.brand = brand.name;

        var header = document.createElement('div');
        header.className = 'd-flex justify-content-between align-items-center';

        var info = document.createElement('div');
        var title = document.createElement('h5');
        title.className = 'mb-1';
        title.textContent = brand.name;
        var subtitle = document.createElement('small');
        subtitle.className = 'text-muted';
        subtitle.textContent = brand.articles + ' articles analysed';
        info.appendChild(title);
        info.appendChild(subtitle);

        var scoreBadge = document.createElement('span');
        scoreBadge.className = 'badge bg-primary';
        scoreBadge.textContent = 'Score ' + brand.score;

        header.appendChild(info);
        header.appendChild(scoreBadge);

        var bars = document.createElement('div');
        bars.className = 'mt-3';

        var sentiments = [
            { label: 'Positive', value: brand.pos, color: 'bg-success' },
            { label: 'Neutral',  value: brand.neu, color: 'bg-warning' },
            { label: 'Negative', value: brand.neg, color: 'bg-danger'  }
        ];

        sentiments.forEach(function(s) {
            var wrapper = document.createElement('div');
            wrapper.className = 'mb-2';

            var labelRow = document.createElement('div');
            labelRow.className = 'd-flex justify-content-between';
            var labelLeft = document.createElement('span');
            labelLeft.textContent = s.label;
            var labelRight = document.createElement('span');
            labelRight.textContent = s.value + '%';
            labelRow.appendChild(labelLeft);
            labelRow.appendChild(labelRight);

            var progress = document.createElement('div');
            progress.className = 'progress';
            var bar = document.createElement('div');
            bar.className = 'progress-bar ' + s.color;
            bar.style.width = s.value + '%';
            progress.appendChild(bar);

            wrapper.appendChild(labelRow);
            wrapper.appendChild(progress);
            bars.appendChild(wrapper);
        });

        card.appendChild(header);
        card.appendChild(bars);
        brandList.appendChild(card);
    });
}

// Render summary table
function renderSummary(data) {
    var summary = document.getElementById('summary-body');
    if (!summary) return;
    summary.innerHTML = '';

    data.forEach(function(b) {
        var row = document.createElement('tr');
        var cells = [b.name, b.score, b.articles, b.neg + '%'];
        cells.forEach(function(val) {
            var td = document.createElement('td');
            td.textContent = val;
            row.appendChild(td);
        });
        summary.appendChild(row);
    });
}

// Render bar chart
function loadChart(data) {
    var ctx = document.getElementById('competitorChart');
    if (!ctx) return;

    var labels   = data.map(function(b) { return b.name; });
    var positive = data.map(function(b) { return b.pos; });
    var neutral  = data.map(function(b) { return b.neu; });
    var negative = data.map(function(b) { return b.neg; });

    if (chart) { chart.destroy(); }

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Positive', data: positive, backgroundColor: 'green' },
                { label: 'Neutral',  data: neutral,  backgroundColor: 'gold'  },
                { label: 'Negative', data: negative, backgroundColor: 'red'   }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Fetch data from API with optional brand filter
function loadData(selectedBrands) {
    var url = '/api/competitors';
    if (selectedBrands && selectedBrands.length > 0) {
        var params = selectedBrands.map(function(b) {
            return 'brands=' + encodeURIComponent(b);
        }).join('&');
        url += '?' + params;
    }

    fetch(url)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            renderBrands(data);
            renderSummary(data);
            loadChart(data);
        })
        .catch(function(err) {
            console.error('Failed to load competitor data:', err);
        });
}

// Add discussion comment
function addDiscussion() {
    var input = document.getElementById('discussion-input');
    var discussionList = document.getElementById('discussion-list');
    var text = input.value.trim();

    if (text === '') {
        alert('Please enter a discussion comment.');
        return;
    }

    var item = document.createElement('div');
    item.className = 'discussion-item mb-3 p-3 border rounded';

    var header = document.createElement('div');
    header.className = 'd-flex justify-content-between';
    var name = document.createElement('strong');
    name.textContent = 'Team Member';
    var badge = document.createElement('span');
    badge.className = 'badge bg-primary';
    badge.textContent = 'New Comment';
    header.appendChild(name);
    header.appendChild(badge);

    var content = document.createElement('p');
    content.className = 'mt-2 mb-1';
    content.textContent = text;

    var time = document.createElement('small');
    time.className = 'text-muted';
    time.textContent = 'Just now';

    item.appendChild(header);
    item.appendChild(content);
    item.appendChild(time);

    discussionList.prepend(item);
    input.value = '';
}

// Load all brands on page load
document.addEventListener('DOMContentLoaded', function() {
    loadData([]);
});
