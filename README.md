# WeatherRanking
Where in Europe should you teleport to experience the best weather possible?

## How do I run this thing?
First, you need docker installed, and also docker-compose. They should do the rest for you. Pun not intended.

**First time?**

`docker-compose up --build`

**Mamma mia, here we go again...**

`docker-compose up`

Go to `http://127.0.0.1:7890/` for the user-friendly weather ranking.

Go to `http://127.0.0.1:7890/docs` for programmer-friendly ranking.

Go to `http://127.0.0.1:7890/api/v1/cities-scores` for no-one friendly ranking.

`Ctrl + C` to quit.
