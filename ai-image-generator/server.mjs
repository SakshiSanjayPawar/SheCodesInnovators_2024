import express from 'express';
import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';

const app = express();

const token = "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";

app.use(express.json());
app.use(express.static('public')); // Serve static files from the 'public' folder

// Ensure the public/images directory exists
const imagesDir = path.join(path.resolve(), 'public', 'images');
if (!fs.existsSync(imagesDir)){
    fs.mkdirSync(imagesDir, { recursive: true });
}

// Route to handle image generation
app.post('/generate-image', async (req, res) => {
    try {
        const response = await fetch(
            "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            {
                method: 'POST',
                headers: { 
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    inputs: req.body.prompt,
                }),
            }
        );

        if (!response.ok) {
            const errorDetail = await response.json();
            console.error('Error:', errorDetail);
            throw new Error('Failed to fetch the image');
        }

        const imagePath = path.join(imagesDir, 'generated_image.png');
        const buffer = await response.arrayBuffer();
        fs.writeFileSync(imagePath, Buffer.from(buffer));
        res.json({ message: 'Image saved successfully', path: 'images/generated_image.png' });
    } catch (error) {
        console.error('Error generating image:', error);
        res.status(500).json({ error: 'Failed to generate image' });
    }
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
