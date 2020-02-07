# sfontmapper
Anti-Anti-Spider Font mapper

### Example

#### Download font files

```bash
python src/utils/fetch.py examples/a138ef96777ccaa13b08f56e8ed2a1fd.css
```

#### Generate mapping

```bash
python src/genmap.py examples/89579064.woff
python src/genmap.py examples/PingFang-SC-Regular.ttf
python src/mapper.py examples/89579064.pickle examples/PingFang-SC-Regular.pickle
```