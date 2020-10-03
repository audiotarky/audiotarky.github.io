#! /usr/bin/env python3

import datetime
import hashlib
import pathlib
import re
import sys

from enum import Enum

import ilcli


PATH = pathlib.Path(__file__).absolute().parents[0]

ARTIST_TEMPLATE = '''---
layout: artist
id: {id}
name: {name}
ilp: {ilp}
slug: {slug}
---'''

ALBUM_TEMPLATE = '''---
layout: album
id: {id}
name: {name}
artist: {artist}
categories:
  - {artist}
slug: {slug}
---'''

TRACK_TEMPLATE = '''---
layout: track
id: {id}
name: {name}
artist: {artist}
album: {album}
categories:
  - {artist}
  - {album}
slug: {slug}
track_number: 0
license: {license}
wm_only: false
no_embed: false
---'''

PAYID_TEMPLATE = '''---
name: {name}
slug: {slug}
ilp: {ilp}
layout: payid
categories:
  - payid
---
'''


class Templates(Enum):
    artist = ARTIST_TEMPLATE
    payid = PAYID_TEMPLATE
    album = ALBUM_TEMPLATE
    track = TRACK_TEMPLATE


def get_layouts():
    path = pathlib.Path(__file__).absolute().parents[0]
    layouts = path.joinpath('_layouts')
    return [x.name.replace('.html', '') for x in layouts.glob('*.html')]


def get_file(ptype, **kwargs):
    ext = kwargs.get('extension', 'md')
    if 'slug' in kwargs:
        slug = kwargs['slug']
    else:
        slug = re.sub('[^\w\-_\.]', '-', kwargs['name'])
        slug = re.sub('-{2,}', '-', slug).lower()
    filename = f'{slug}.{ext}'
    existing = PATH.glob(f'data/_{ptype}/*-{filename}')
    existing = list(existing)
    if len(existing) > 1:
        raise ValueError(f'many files found: {existing}')
    elif len(existing) == 1:
        post = existing[0]
    else:
        d = datetime.date.today().isoformat()
        post = PATH.joinpath(f'data/_{ptype}/{d}-{filename}')
    return post, slug


def exists(itemtype, name):
    post, _ = get_file(itemtype, name=name)
    return post.exists()


class artist(ilcli.Command):
    name = 'artist'
    restricted_names = ['audiotarky']

    def _init_arguments(self):
        self.add_argument('artist', help='Artist name')
        self.add_argument('ilp', help='Artist ilp', default='not set')

    def _validate_arguments(self, args):
        if args.artist in self.restricted_names:
            self.err(f'{args.artist} is a restricted name, exiting')
            return 1

    def _run(self, args):
        self.render(name=args.artist, ilp=args.ilp)

    @classmethod
    def render(cls, **kwargs):
        render(cls.name, name=kwargs['name'], ilp=kwargs['ilp'])
        if kwargs['ilp'] != 'not set':
            render('payid',
                   name=kwargs['name'],
                   ilp=kwargs['ilp'],
                   extension='json',
                   slug=f'pay{kwargs["name"].title().replace(" ", "")}'
                   )


class album(ilcli.Command):
    name = 'album'

    def _init_arguments(self):
        # TODO: make these choices?
        self.add_argument('artist', help='Artist name')
        self.add_argument('album', help='Album title')

    def _run(self, args):
        self.render(name=args.album, artist=args.artist)

    @classmethod
    def render(cls, **kwargs):
        render(cls.name, name=kwargs['name'], artist=kwargs['artist'])
        if not exists('artist', kwargs['artist']):
            artist.render(name=kwargs['artist'], ilp='not set')


class track(ilcli.Command):
    name = 'track'

    def _init_arguments(self):
        # TODO: make these choices?
        self.add_argument('artist', help='Artist name')
        self.add_argument('album', help='Album title')
        self.add_argument('track', help='Track title')
        self.add_argument(
            '-l', '--license',
            help='Track license',
            default='CC BY-NC-SA',
            choices=['CC BY', 'CC BY-SA', 'CC BY-NC', 'CC BY-NC-SA', 'CC BY-ND', 'CC BY-NC-ND'])

    def _run(self, args):
        self.render(name=args.track, artist=args.artist,
                    album=args.album, license=args.license)

    @classmethod
    def render(cls, **kwargs):
        render(cls.name, name=kwargs['name'], license=kwargs['license'],
               artist=kwargs['artist'], album=kwargs['album'])
        if not exists('album', kwargs['album']):
            album.render(name=kwargs['album'], artist=kwargs['artist'])


class audiotarky(ilcli.Command):
    subcommands = [artist, album, track]


def render(ptype, **kwargs):
    post, slug = get_file(ptype, **kwargs)
    if 'slug' in kwargs:
        del kwargs['slug']
    item_id = hashlib.md5()
    for k, v in kwargs.items():
        item_id.update(bytes(k, 'utf8'))
        item_id.update(bytes(v, 'utf8'))

    with post.open('w') as file:
        file.write(
            Templates[ptype].value.format(
                id=item_id.hexdigest(),
                slug=slug,
                **kwargs
            )
        )
    print(f'now edit {post.relative_to(PATH)}')


if __name__ == "__main__":
    cli = audiotarky()

    sys.exit(cli.run())
