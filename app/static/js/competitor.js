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



document.addEventListener(
    'DOMContentLoaded',
    loadData
);