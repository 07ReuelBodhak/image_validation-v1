const express = require('express');
const app = express();
const path = require('path');
const multer = require('multer');
const infoModel = require('./models/Info'); 
const mongoose = require('mongoose')

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

mongoose.connect('mongodb://127.0.0.1:27017/employee')

app.get('/new', async (req, res) => {
    res.render('add.ejs', { name: null });
});

app.post('/new', upload.single('image_path'), async (req, res) => {
    const user = req.body.user;
    const fileName = req.body.file_name;

    console.log('User Name:', user);
    console.log('File Name:', fileName);

    const existingFile = await infoModel.findOne({ filename: fileName });

    if (existingFile) {
        console.log('file already exist')
        return res.status(400).json({ error: 'Filename already exists.' });
    }
    const newFile = new infoModel({
        filename: fileName,
        name: user
    });

    try {
        const savedFile = await newFile.save();
        res.json({ key: 'success' });
        console.log('File saved:', savedFile);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error during image upload.' });
    }
});


app.listen(3030, () => {
    console.log('Server running on http://localhost:3030');
});
