const primaryPalette = ['#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff', '#9333ea', '#7e22ce'];
let chartsInitialized = false;

function initCharts() {
    if (chartsInitialized) return;
    chartsInitialized = true;

    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { boxWidth: 12, padding: 14, font: { size: 12 }, usePointStyle: true, pointStyle: 'circle' }
            },
            tooltip: {
                backgroundColor: '#111827', padding: 10,
                titleFont: { size: 12, weight: '600' }, bodyFont: { size: 12 },
                cornerRadius: 6, displayColors: true, boxWidth: 8, boxHeight: 8, usePointStyle: true
            }
        }
    };

    const projectsStatus = JSON.parse(document.getElementById('data-projects-status').textContent);
    new Chart(document.getElementById('chartProjectsStatus'), {
        type: 'doughnut',
        data: { labels: projectsStatus.labels, datasets: [{ data: projectsStatus.values, backgroundColor: primaryPalette, borderWidth: 0 }] },
        options: { ...chartDefaults, cutout: '60%' }
    });

    const tasksPriority = JSON.parse(document.getElementById('data-tasks-priority').textContent);
    new Chart(document.getElementById('chartTasksPriority'), {
        type: 'radar',
        data: {
            labels: tasksPriority.labels,
            datasets: [{
                label: window.__i18n.tasks,
                data: tasksPriority.values,
                borderColor: '#9333ea',
                backgroundColor: 'rgba(168, 85, 247, 0.25)',
                pointBackgroundColor: '#9333ea',
                pointBorderColor: '#ffffff',
                pointRadius: 5, pointHoverRadius: 7, borderWidth: 2
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, padding: 14, font: { size: 12 }, usePointStyle: true, pointStyle: 'circle' } },
                tooltip: { backgroundColor: '#111827', padding: 10, titleFont: { size: 12, weight: '600' }, bodyFont: { size: 12 }, cornerRadius: 6, displayColors: false }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: { precision: 0, backdropColor: 'transparent', color: '#9ca3af', font: { size: 10 } },
                    grid: { color: '#e5e7eb' },
                    angleLines: { color: '#e5e7eb' },
                    pointLabels: { color: '#374151', font: { size: 12, weight: '500' } }
                }
            }
        }
    });

    const tasksStatus = JSON.parse(document.getElementById('data-tasks-status').textContent);
    new Chart(document.getElementById('chartTasksStatus'), {
        type: 'polarArea',
        data: {
            labels: tasksStatus.labels,
            datasets: [{
                label: window.__i18n.tasks,
                data: tasksStatus.values,
                backgroundColor: ['rgba(107, 114, 128, 0.75)', 'rgba(59, 130, 246, 0.75)', 'rgba(168, 85, 247, 0.75)', 'rgba(22, 163, 74, 0.75)'],
                borderColor: '#ffffff', borderWidth: 2
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, padding: 14, font: { size: 12 }, usePointStyle: true, pointStyle: 'circle' } },
                tooltip: { backgroundColor: '#111827', padding: 10, titleFont: { size: 12, weight: '600' }, bodyFont: { size: 12 }, cornerRadius: 6, displayColors: false }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: { precision: 0, backdropColor: 'transparent', color: '#9ca3af', font: { size: 10 } },
                    grid: { color: '#e5e7eb' }, angleLines: { color: '#e5e7eb' }
                }
            }
        }
    });

    const projectsTimeline = JSON.parse(document.getElementById('data-projects-timeline').textContent);
    new Chart(document.getElementById('chartProjectsTimeline'), {
        type: 'line',
        data: {
            labels: projectsTimeline.labels,
            datasets: [{
                label: window.__i18n.projects,
                data: projectsTimeline.values,
                borderColor: '#9333ea',
                backgroundColor: 'rgba(168, 85, 247, 0.15)',
                fill: true, tension: 0.4,
                pointBackgroundColor: '#9333ea', pointRadius: 5, pointHoverRadius: 7
            }]
        },
        options: {
            ...chartDefaults,
            plugins: { ...chartDefaults.plugins, legend: { ...chartDefaults.plugins.legend, display: true } },
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#f3f4f6' } },
                x: { grid: { display: false } }
            }
        }
    });
}

document.addEventListener('alpine:init', () => {
    Alpine.data('statsSection', () => ({
        open: false,
        toggle() {
            this.open = !this.open;
            if (this.open) {
                setTimeout(initCharts, 100);
            }
        }
    }));
});