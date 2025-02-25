# File Share Sync

A Progressive Web App built with Flask that allows users to securely share files across devices. The app features local authentication and is optimized for mobile access with PWA capabilities.

## Features

- 🔐 User Authentication (Login/Register)
- 📱 PWA Support (Install on mobile devices)
- 📂 File Upload/Download
- 🌙 Dark Mode Interface
- 📲 Responsive Design
- 💾 Local File Storage
- 🔄 Service Worker for Offline Capability

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5 (Dark Theme)
- **PWA Features**: Service Workers
- **File Handling**: Werkzeug

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tijnndev/file-share-sync.git
cd file-share-sync
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export SESSION_SECRET=your_secret_key
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Register a new account or login with existing credentials
2. Upload files using the upload button on the dashboard
3. View, download, or delete your uploaded files
4. Install as PWA on mobile devices for easier access

### Installing as PWA

1. On Android (Chrome):
   - Open the website
   - Tap the "Add to Home Screen" prompt or menu option

2. On iOS (Safari):
   - Open the website
   - Tap the share button
   - Select "Add to Home Screen"

## Development

To set up the development environment:

1. Install Python 3.11 or higher
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run in debug mode:
```bash
python main.py
```

## Project Structure

```
├── app.py                 # Main application file
├── main.py               # Entry point
├── models.py             # Database models
├── static/
│   ├── js/
│   │   ├── app.js       # Main JavaScript
│   │   └── sw.js        # Service Worker
│   └── manifest.json    # PWA manifest
├── templates/
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── files.html       # File management page
└── uploads/             # File storage directory
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- Files are stored locally in the `uploads` directory
- User passwords are hashed using Werkzeug's security functions
- Session management is handled by Flask-Login
- CSRF protection is enabled

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Tijnndev
