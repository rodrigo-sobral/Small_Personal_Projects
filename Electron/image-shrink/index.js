const path = require('path');
const os = require('os');
const { app, BrowserWindow, Menu, ipcMain, shell } = require('electron');
const imagemin = require('imagemin');
const imageminMozjpeg = require('imagemin-mozjpeg');
const imageminPngquant = require('imagemin-pngquant');
const slash = require('slash');
const log = require('electron-log');

// Set Environment
process.env.NODE_ENV = 'production';

// const isDev = !app.isPackaged;
const isDev = process.env.NODE_ENV !== 'production';
const isMac = process.platform === 'darwin';

let mainWindow;
function createMainWindow() {
    mainWindow = new BrowserWindow({
        title: 'ImageShrink',
        width: isDev ? 1200 : 400,
        height: 600,
        icon: './assets/icons/Icon_256x256.png',
        resizable: isDev,
        backgroundColor: 'white',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });
    
    if (isDev) {
        mainWindow.webContents.openDevTools();
    }
    mainWindow.loadFile(`./app/index.html`);
}

let aboutWindow;
function createAboutWindow() {
    aboutWindow = new BrowserWindow({
        title: 'About ImageShrink',
        width: isDev ? 800 : 400,
        height: 600,
        icon: './assets/icons/Icon_256x256.png',
        resizable: false,
        backgroundColor: 'white',
    });
    
    aboutWindow.loadFile(`./app/about.html`);
    app.on("close", () => aboutWindow)
}

const menu = [
    ...(isMac
      ? [{
            label: app.name,
            submenu: [{label: 'About', click: createAboutWindow}],
        }]
    : []),
    {role: 'fileMenu',},
    ...(!isMac ? [{
            label: 'Help',
            submenu: [{label: 'About', click: createAboutWindow}],
        }]
    : []),
    ...(isDev
      ? [{
            label: 'Developer',
            submenu: [
                { role: 'reload' },
                { role: 'forcereload' },
                { type: 'separator' },
                { role: 'toggledevtools' },
            ],
        }]
    : []),
];

ipcMain.on("image:minimize", (e, options) => {
    options.dest = path.join(os.homedir(), 'imageshrink');
    shrinkImage(options)
});

async function shrinkImage({ imgPath, quality, dest }) {
    try {
        const pngQuality = parseFloat(quality) / 100;
        const files = await imagemin([slash(imgPath)], {
            destination: dest,
            plugins: [
                imageminMozjpeg({ quality: parseInt(quality) }),
                imageminPngquant({
                    quality: [pngQuality, pngQuality]
                })
            ]
        });
        log.info("Image minimized successfully:", files);
        shell.openPath(dest);
        mainWindow.webContents.send("image:minimize:response", { success: true });
    } catch (error) {
        mainWindow.webContents.send("image:minimize:response", { success: false, error: error.message });
        log.error("Error minimizing image:", error);
    }
}

app.on("window-all-closed", () => {
    if (!isMac) {
        app.quit();
    }
})

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createMainWindow();
    }
})

app.whenReady().then(() => {
    createMainWindow();

    const mainMenu = Menu.buildFromTemplate(menu);
    Menu.setApplicationMenu(mainMenu);

    mainWindow.on("ready", () => mainWindow = null);
});
