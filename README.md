# HTTP JSON API that converts URLs to long unreadable string and back ...

... and sometimes behaves in not so expected way

## Development

Run `pip install -r requirements.txt` to install dependencies,
then `flask run` to start dev server


## Endpoints

- `POST /make_me_longer`
  Example:
  request: `POST /make_me_longer?url=http%3A%2F%2Flmgtfy.com%2F`
  response:

  `201 Created`

  ```json
  {"long_string": "aHR0cHM6Ly9sbWd0ZnkuY29tLw=="}
  ```

  Example with error:
  request: `POST /make_me_longer?url=fdklgsjdfsdfg`
  response:

  `400 Bad Request`

  ```json
  {"message": "Not a valid URL"}
  ```


- `GET /short_again/:long_string`
  Example
  request: `POST /short_again/aHR0cHM6Ly9sbWd0ZnkuY29tLw==`
  response:

  `200 Ok`

  ```json
  {"original_url": "https://lmgtfy.com/"}
  ```