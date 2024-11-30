document.getElementById('upload-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('file-input');
    if (fileInput.files.length === 0) {
        alert('Selectează un fișier!');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/upload', { method: 'POST', body: formData });
    const result = await response.json();

    if (result.status === 'success') {
        document.getElementById('data-section').style.display = 'block';
        const table = document.getElementById('data-preview');
        table.innerHTML = '';
        for (const [col, values] of Object.entries(result.preview)) {
            const headerRow = table.insertRow(-1);
            headerRow.innerHTML = `<th>${col}</th>`;
            values.forEach(value => {
                const row = table.insertRow(-1);
                row.innerHTML = `<td>${value}</td>`;
            });
        }
        const columnSelect = document.getElementById('column-select');
        columnSelect.innerHTML = result.columns.map(col => `<option value="${col}">${col}</option>`).join('');
    } else {
        alert(result.message);
    }
});

document.getElementById('stats-btn').addEventListener('click', async () => {
    const response = await fetch('/statistics');
    const result = await response.json();
    if (result.status === 'success') {
        const statsDiv = document.getElementById('statistics');
        statsDiv.innerHTML = JSON.stringify(result.statistics, null, 2);
    } else {
        alert(result.message);
    }
});

document.getElementById('plot-btn').addEventListener('click', async () => {
    const column = document.getElementById('column-select').value;
    const response = await fetch('/plot', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column }) 
    });
    const result = await response.json();
    if (result.status === 'success') {
        const plotImage = document.getElementById('plot-image');
        plotImage.src = result.plot_url;
        plotImage.style.display = 'block';
    } else {
        alert(result.message);
    }
});
