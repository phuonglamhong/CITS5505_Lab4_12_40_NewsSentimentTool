// Store chart instance globally so it can be updated safely
let chart;


// Filters competitor brand rows dynamically based on search input.
function filterBrands() {

    const query =
        document.getElementById('brand-search')
            .value
            .toLowerCase();

    document.querySelectorAll('.brand-row').forEach(row => {

        const name =
            row.dataset.brand.toLowerCase();

        row.style.display =
            name.includes(query)
                ? ''
                : 'none';
    });
}


// Dynamically creates competitor sentiment cards from API data.
function renderBrands(data) {

    const brandList =
        document.getElementById('brand-list');

    // Clear previous content
    brandList.innerHTML = '';

    data.forEach(brand => {

        brandList.innerHTML += `

            <div
                class="brand-row border rounded p-3 mb-3"
                data-brand="${brand.name}"
            >

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        <h5 class="mb-1">
                            ${brand.name}
                        </h5>

                        <small class="text-muted">
                            ${brand.articles} articles analysed
                        </small>

                    </div>

                    <span class="badge bg-primary">
                        Score ${brand.score}
                    </span>

                </div>

                <div class="mt-3">

                    <div class="mb-2">

                        <div class="d-flex justify-content-between">
                            <span>Positive</span>
                            <span>${brand.pos}%</span>
                        </div>

                        <div class="progress">
                            <div
                                class="progress-bar bg-success"
                                style="width:${brand.pos}%"
                            ></div>
                        </div>

                    </div>

                    <div class="mb-2">

                        <div class="d-flex justify-content-between">
                            <span>Neutral</span>
                            <span>${brand.neu}%</span>
                        </div>

                        <div class="progress">
                            <div
                                class="progress-bar bg-warning"
                                style="width:${brand.neu}%"
                            ></div>
                        </div>

                    </div>

                    <div>

                        <div class="d-flex justify-content-between">
                            <span>Negative</span>
                            <span>${brand.neg}%</span>
                        </div>

                        <div class="progress">
                            <div
                                class="progress-bar bg-danger"
                                style="width:${brand.neg}%"
                            ></div>
                        </div>

                    </div>

                </div>

            </div>
        `;
    });
}


// Creates and updates Chart.js bar chart for sentiment comparison.
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

    // Destroy old chart before re-rendering
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


// Displays competitor statistics inside summary table.
function renderSummary(data) {

    const summary =
        document.getElementById('summary-body');

    // Clear previous table rows
    summary.innerHTML = '';

    data.forEach(b => {

        summary.innerHTML += `

            <tr>

                <td>${b.name}</td>

                <td>${b.score}</td>

                <td>${b.articles}</td>

                <td>${b.neg}%</td>

            </tr>
        `;
    });
}


// Fetches competitor analysis data from Flask API endpoint.
function loadData() {

    fetch('/api/competitors')

        .then(response => response.json())

        .then(data => {

            renderBrands(data);

            renderSummary(data);

            loadChart(data);
        })

        .catch(err => {

            console.error(
                'Failed to load competitor data:',
                err
            );
        });
}


// Allows users to post collaboration discussion comments dynamically.
function addDiscussion() {

    const input =
        document.getElementById('discussion-input');

    const discussionList =
        document.getElementById('discussion-list');

    const text =
        input.value.trim();

    // Prevent empty submissions
    if (text === '') {

        alert('Please enter a discussion comment.');

        return;
    }

    // Create new discussion card
    const discussionItem =
        document.createElement('div');

    discussionItem.className =
        'discussion-item mb-3 p-3 border rounded';

    discussionItem.innerHTML = `

        <div class="d-flex justify-content-between">

            <strong>Team Member</strong>

            <span class="badge bg-primary">
                New Comment
            </span>

        </div>

        <p class="mt-2 mb-1">
            ${text}
        </p>

        <small class="text-muted">
            Just now
        </small>
    `;

    // Add newest comment at top
    discussionList.prepend(discussionItem);

    // Clear input after posting
    input.value = '';
}


// Loads competitor data when page finishes loading.
document.addEventListener(
    'DOMContentLoaded',
    loadData
);