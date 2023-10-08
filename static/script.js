document.getElementById('link-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const link = document.getElementById('link').value;  // Make sure to get the value from the input field
    fetch('/check', {
        method: 'POST',
        body: JSON.stringify({ urls: [link] }),  // Modify to pass an array of URLs
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.results[link];  // Access the correct property in the response
    });
});
