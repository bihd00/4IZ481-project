# Cover Generator

- Course Project @[Prague University of Economics and Business - DAB](https://fis.vse.cz/magisterske-studium/magisterske-programy/program-data-a-analytika-pro-business/)
- each directory has its own readme file with relevant info

## Info

- small web application intended for use by music artits to generate song/album covers
- users can insert texts of their song(s), then generate covers based on the text contents
- texts are summarized to a length of about 2 sentences
- summaries are then used to generate covers
- both summary and cover generation rely on OpenAPI APIs
- since OpenAI does not provide persistent storage for generated images (they exist only for 2hours),<br>these are stored using Google Cloud Storage
- most of the application is based on Google's services, it is a serverless application