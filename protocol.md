# This draft file describes Frontend/Backend endpoints for actions 

# frontend/backend

- GET /conferences -> return list of conferences 
- POST /conferences -> post a new commitee 
- PATCH and DELETE follows
- GET /{conference_id}/dashboard -> return dashboard with various actions that will be described below
- GET /{conference_id}/committees -> return list of committees of a conference 
- POST /{conference_id}/committees -> post a new committee (via admin)
- PATCH and DELETE follows

- GET /{conference_id}/{commitee_id}/session -> open session of committee, probably then connect via websocket here

# backend 
- CONNECTION ws://{backend_api_url}/ws/{commitee_id} -> open a new websocket connection to the backend by using commitee path parameter 
- This can be connected to a single ConnectionManager in the backend while using a path parameter for a simpler backend logging and etc 
