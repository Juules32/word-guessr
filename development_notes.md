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
(Loosely) Three layered architecture:
- Presentation Tier (Client Tier): `main.py`
- Application Tier (Business Logic Tier): `game_manager.py`
- Data Tier (Database Tier): `kv_manager.py`

## Other
Note: It's very important that the KV_URL for prod must start with: "rediss://" (note the double 's'), otherwise it doesn't work!

## Deployment to Vercel
[Great video explanation](https://www.youtube.com/watch?v=8R-cetf_sZ4)

- Download vercel cli with: `npm i -g vercel`
- Login: `vercel login`
- Load the project: `vercel .`
- When asked to link to existing project, say yes if you've already set up a project, otherwise give it a name
- To deploy to prod manually: `vercel --prod`
- (Optional) To enable continuous deployment, enable it on the project page

### Enable redis connection
The project needs access to a hosted redis database, which you can set up fairly easily on vercel.

Once set up, don't connect the redis database to the project! Instead, copy the KV_URL environment variable and (importantly) change "redis://<connection_string>" to "rediss://<connection_string>". Now set an environment variable under the project settings with that key and value.

The reason I don't connect the database to the project, is that I think the @vercel/kv api is obsolete. Instead I use the redis library in python.

### Notes about deployment to Vercel
The `vercel.json` file is configured to deploy a python project. All the details behind are taken care of automatically.
