function filterBrands() {

    const query = document
        .getElementById('brand-search')
        .value
        .toLowerCase();

    document.querySelectorAll('.brand-row').forEach(row => {

        const name = row.dataset.brand.toLowerCase();

        row.style.display =
            name.includes(query) ? '' : 'none';
    });
}

let chart;

function loadChart(data) {

    const ctx =
        document.getElementById('competitorChart');

    const labels = data.map(b => b.name);

    const positive = data.map(b => b.pos);
    const neutral = data.map(b => b.neu);
    const negative = data.map(b => b.neg);

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
        }
    });
}

function renderBrands(data) {

    const container =
        document.getElementById('brand-list');

    const summary =
        document.getElementById('summary-body');

    container.innerHTML = '';
    summary.innerHTML = '';

    data.forEach(b => {

        container.innerHTML += `

      <div class="brand-row" data-brand="${b.name}">

        <div class="brand-name">
          ${b.name}
        </div>

        <div class="brand-bar-wrap">

          <div class="d-flex"
               style="height:8px;border-radius:4px;overflow:hidden;">

            <div style="width:${b.pos}%;background:green;"></div>

            <div style="width:${b.neu}%;background:gold;"></div>

            <div style="width:${b.neg}%;background:red;"></div>

          </div>

        </div>

        <div class="brand-score">
          ${b.score}
        </div>

        <div>
          ${b.articles} arts
        </div>

      </div>
    `;

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

function loadData() {

    fetch('/api/competitors')

        .then(res => res.json())

        .then(data => {

            renderBrands(data);

            loadChart(data);
        });
}

document.addEventListener(
    'DOMContentLoaded',
    loadData
);