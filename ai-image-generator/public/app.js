const inputTxt = document.getElementById("input");
const image = document.getElementById("image");
const button = document.getElementById("btn");

button.addEventListener('click', async function() {
    const response = await fetch('/generate-image', {
        method: 'POST',
        headers: { 
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: inputTxt.value,
        }),
    });

    if (response.ok) {
        const data = await response.json();
        image.src = '/' + data.path;
    } else {
        console.error('Error generating image:', response.statusText);
    }
});
