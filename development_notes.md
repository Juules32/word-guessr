## Redis Setup
### Installation
[Instructions here](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

### Start a local server
```
sudo service redis-server start
```
Now, the server is active as long as the terminal is open.

### Connect through the cli 
```
redis-cli
```

## Architecture
Three layered architecture:
- Presentation Tier (Client Tier): `main.py`
- Application Tier (Business Logic Tier): `game_manager.py`
- Data Tier (Database Tier): `kv_manager.py`

## Other
Note: It's very important that the KV_URL for prod must start with: "rediss://" (note the double 's'), otherwise it doesn't work!
