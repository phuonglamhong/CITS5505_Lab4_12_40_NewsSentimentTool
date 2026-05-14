/*
Competitor dashboard functionality.

This file handles:
- Brand filtering
- API data fetching
- Dynamic summary rendering
- Dynamic chart rendering
*/

let chart;

// Filter displayed brands using search input.
function filterBrands() {
    const query = document.getElementById('brand-search').value.toLowerCase();
    document.querySelectorAll('.brand-row').forEach(row => {
        const name = row.dataset.brand.toLowerCase();
        row.style.display = name.includes(query) ? '' : 'none';
    });
}

// Render competitor sentiment chart.
function loadChart(data) {

    const ctx =
        document.getElementById('competitorChart');

    const labels =
        data.map(b => b.name);

    const positive =
        data.map(b => b.pos);

    const neutral =
        data.map(b => b.neu);

    const negative =
        data.map(b => b.neg);

    // Destroy existing chart before re-rendering
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {

        type: 'bar',

        data: {

            labels: labels,

            datasets: [

                {
                    label: 'Positive',
                    data: positive,
                    backgroundColor: 'green'
                },

                {
                    label: 'Neutral',
                    data: neutral,
                    backgroundColor: 'gold'
                },

                {
                    label: 'Negative',
                    data: negative,
                    backgroundColor: 'red'
                }

            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// Render brand comparison cards dynamically.

function renderBrands(data) {

    const brandList =
        document.getElementById('brand-list');

    brandList.innerHTML = '';

    data.forEach(b => {

        brandList.innerHTML += `

            <div class="brand-row mb-3"
                 data-brand="${b.name}">

                <div class="d-flex justify-content-between">

                    <strong>${b.name}</strong>

                    <span>
                        Score: ${b.score}
                    </span>

                </div>

                <div class="progress mt-2"
                     style="height: 22px;">

                    <div class="progress-bar bg-success"
                         style="width:${b.pos}%">

                        ${b.pos}%

                    </div>

                    <div class="progress-bar bg-warning text-dark"
                         style="width:${b.neu}%">

                        ${b.neu}%

                    </div>

                    <div class="progress-bar bg-danger"
                         style="width:${b.neg}%">

                        ${b.neg}%

                    </div>

                </div>

            </div>
        `;
    });
}


// Render summary table dynamically.
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

// Fetch competitor data from backend API.
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

// Load competitor data after page loads.
document.addEventListener(
    'DOMContentLoaded',
    loadData
);
