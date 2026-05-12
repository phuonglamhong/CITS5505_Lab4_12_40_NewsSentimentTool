function filterBrands() {
    const query = document.getElementById('brand-search').value.toLowerCase();
    document.querySelectorAll('.brand-row').forEach(row => {
        const name = row.dataset.brand.toLowerCase();
        row.style.display = name.includes(query) ? '' : 'none';
    });
}

let chart;

function renderBrands(data) {
    const container = document.getElementById('brand-list');
    container.innerHTML = '';
    data.forEach(b => {
        container.innerHTML += `
        <div class="brand-row mb-3" data-brand="${b.name}">
            <div class="d-flex justify-content-between mb-1">
                <strong>${b.name}</strong>
                <span class="text-muted" style="font-size:0.85rem;">Score: ${b.score}</span>
            </div>
            <div class="progress mb-1" style="height:8px;">
                <div class="progress-bar bg-success" style="width:${b.pos}%" title="Positive"></div>
            </div>
            <div class="progress mb-1" style="height:8px;">
                <div class="progress-bar bg-warning" style="width:${b.neu}%" title="Neutral"></div>
            </div>
            <div class="progress mb-1" style="height:8px;">
                <div class="progress-bar bg-danger" style="width:${b.neg}%" title="Negative"></div>
            </div>
            <div class="d-flex gap-3 mt-1" style="font-size:0.78rem; color:#666;">
                <span>✅ ${b.pos}% Positive</span>
                <span>⚡ ${b.neu}% Neutral</span>
                <span>❌ ${b.neg}% Negative</span>
            </div>
        </div>`;
    });
}

function loadChart(data) {
    const ctx      = document.getElementById('competitorChart');
    const labels   = data.map(b => b.name);
    const positive = data.map(b => b.pos);
    const neutral  = data.map(b => b.neu);
    const negative = data.map(b => b.neg);

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Positive', data: positive, backgroundColor: '#2e7d50' },
                { label: 'Neutral',  data: neutral,  backgroundColor: '#c88a1a' },
                { label: 'Negative', data: negative, backgroundColor: '#b53b3b' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function renderSummary(data) {
    const summary = document.getElementById('summary-body');
    summary.innerHTML = '';
    data.forEach(b => {
        summary.innerHTML += `
        <tr>
            <td>${b.name}</td>
            <td>${b.score}</td>
            <td>${b.articles}</td>
            <td>${b.neg}%</td>
        </tr>`;
    });
}

function loadData() {
    fetch('/api/competitors')
        .then(response => response.json())
        .then(data => {
            renderBrands(data);
            renderSummary(data);
            loadChart(data);
        })
        .catch(err => console.error('Failed to load competitor data:', err));
}

document.addEventListener('DOMContentLoaded', loadData);
