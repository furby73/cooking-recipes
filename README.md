# Cooking Recipes App
http://35.208.162.161/
https://www.youtube.com/watch?v=-5zU0QcI6rE
## Installation & Setup
   Start the application:
   ```bash
   docker-compose up --build
   ```

## Admin Panel Access
To manage recipes:
1. Visit `/admin/login` 
2. Enter password: `"yourpassword"`
3. You'll gain access to the recipe editing dashboard


## Technical highlights 
- **Services**: MinIO (s3 storage), Flask/Gunicorn (app), Nginx (reverse proxy)
- **Networking**:
  - Nginx handles port 80 traffic
  - MinIO console at :9001
- **Persistence**:
  - MinIO data volume
  - Sqlite database
- **Access**:
  - App: http://localhost
  - MinIO: http://localhost:9001 (minioadmin/minioadmin)
