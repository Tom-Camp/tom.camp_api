# Tom.Camp API

A Django REST Framework for [Tom.Camp](https://tom.camp).

## Local development

- Clone the [tomcamp_ui](https://github.com/Tom-Camp/tomcamp_ui) repo at the same level as this repo
- Clone this repository.
- From this repo, copy the [docker-compose](docker-compose.yml.example) file from this repo up a directory and rename it to `docker-compose.yml`
- The file structure should be:
  - `docker-compose.yml`
  - `tom.camp_api`
  - `tomcamp_ui`

Run `docker-compose up --build`

The React site should build and should be available at <http://localhost:3001>, the API at <http://localhost:8000>

The terminal will continue to log events for both environments in real time. Changes will trigger a rebuild and will be reflected on the sites.

## License

[GNU General Public License v3.0](LICENSE)