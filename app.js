const inputTxt = document.getElementById('input');
const image = document.getElementById('image');
const button = document.getElementById('btn');

async function query() {
    const response = await fetch('/generate-image', {
        headers: { 
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            prompt: inputTxt.value,
        }),
    });

    if (!response.ok) {
        const errorDetail = await response.json();
        console.error('Error:', errorDetail);
        throw new Error('Failed to fetch the image');
    }

    const result = await response.json();
    return result.imageUrl;
}

button.addEventListener('click', async function() {
    try {
        const imageUrl = await query();
        image.src = imageUrl;
    } catch (error) {
        console.error('Error generating image:', error);
    }
});
