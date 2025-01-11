![](https://img.shields.io/github/license/wh1isper/bedway)
![](https://img.shields.io/github/v/release/wh1isper/bedway)
![](https://img.shields.io/docker/image-size/wh1isper/bedway)
![](https://img.shields.io/pypi/dm/bedway)
![](https://img.shields.io/github/last-commit/wh1isper/bedway)
![](https://img.shields.io/pypi/pyversions/bedway)

# bedway

Self-host and maintained [bedrock-access-gateway](https://github.com/aws-samples/bedrock-access-gateway), which is under [MIT No Attribution License](https://github.com/aws-samples/bedrock-access-gateway/blob/093c6fa586be04964820baaf1e3dca431f1fe823/LICENSE)

Why this project:

- No AWS infrastructure needed
- Improved performance
- More features
- Easy to deploy
- Quick response to community requests

## Install

`pip install bedway`

Or use docker image

`docker pull wh1isper/bedway`

## Usage

```bash
docker run --name bedway \
-p 9128:9128 \
-e "AWS_ACCESS_KEY_ID=<access_key_id>" \
-e "AWS_SECRET_ACCESS_KEY=<secret_access_key>" \
-e "API_KEY=<api_key_for_this_service>" \
wh1isper/bedway
```

## Develop

Install pre-commit before commit

```
pip install pre-commit
pre-commit install
```

### Unittest

Install package locally

```
pip install -e .[test]
```

TODO: Write some test..

```
pytest -v
```
