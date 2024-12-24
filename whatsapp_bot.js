const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const { MongoClient } = require('mongodb');

// MongoDB Connection
const mongoUrl = "mongodb+srv://dnRNNJffpUcy948:wBWvTI3xgOXBjAVO@cluster0.cdzla.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const clientDB = new MongoClient(mongoUrl);
const dbName = "whatsapp_data";
const usersCollection = clientDB.db(dbName).collection("users");

let currentFile = '';
let currentMessage = '';

// Initialize WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('authenticated', () => {
    console.log('Authenticated successfully!');
});

client.on('ready', () => {
    console.log('WhatsApp bot is ready!');
});

client.on('message', async (message) => {
    const user = await usersCollection.findOne({ user_id: message.from });

    if (user) {
        console.log("Message already sent to this user!");
    } else {
        if (currentFile) {
            const media = MessageMedia.fromFilePath(currentFile);
            await message.reply(currentMessage);
            await message.reply(media, undefined, { caption: 'Here is the file!' });

            await usersCollection.insertOne({ user_id: message.from, message: currentMessage, file: currentFile });
        } else {
            await message.reply("No file has been set yet!");
        }
    }
});

// Initialize the client
client.initialize();
