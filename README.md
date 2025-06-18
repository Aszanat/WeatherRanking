# WeatherRanking
Where in Europe should you teleport to experience the best weather possible?

## How do I run this thing?
First, you need docker installed, and also docker-buildx.

If you don't want to read about the latter, just skip the "buildx" in the command.

Don't mind the warnings about traditional docker build being deprecated.

`docker buildx build -t weather-ranking .`
`docker run -it --rm --name weather-ranking-cont weather-ranking`
