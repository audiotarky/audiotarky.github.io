# audiotarky.github.io

## Python & generating data

Set up a python venv & install `ilcli`:

```
python3 -m venv venv
pip install ilcli
source venv/bin/activate
```

You can then generate data with `gen.sh`

The templates are:

https://github.com/audiotarky/audiotarky.github.io/blob/master/makepost.py#L16-L58

fields with the same name have the same value for a given artist:ablum:track.
