#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Frederik “Freso” S. Olesen <https://freso.dk/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
""""""

# https://bitbucket.org/metabrainz/musicbrainz-server/pull-requests/1393/mbs-7913-allow-seeding-of-non-url-ars-when/diff
# https://bitbucket.org/metabrainz/musicbrainz-server/pull-requests/770/mbs-7285-cant-seed-external-links-to/diff
# https://github.com/metabrainz/picard-plugins/blob/master/plugins/addrelease/addrelease.py
# https://github.com/JonnyJD/musicbrainz-isrcsubmit


import json
from urllib.parse import urlparse
from collections import namedtuple


MUSICBRAINZ_SERVER = 'https://musicbrainz.org/'
SPOTIFY_MUSICBRAINZ_MAPPING = {
    'album': 'release',
    'artist': 'artist',
    'track': 'recording',
}


def make_spotify_tuple(url):
    """Take a Spotify URL string and turn it into a (named) tuple.

    >>> make_spotify_tuple('http://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL')
    SpotifyIdentifier(Type='album', ID='2QE5TZ3P547etzfMWgE8lL')
    >>> make_spotify_tuple('spotify:album:2QE5TZ3P547etzfMWgE8lL')
    SpotifyIdentifier(Type='album', ID='2QE5TZ3P547etzfMWgE8lL')
    >>> make_spotify_tuple('ftp://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL')
    Traceback (most recent call last):
        ...
    ValueError: ftp://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL is not a recognised Spotify URL.
    """
    SpotifyIdentifier = namedtuple('SpotifyIdentifier', ['Type', 'ID'])
    parsed_url = urlparse(url)

    if parsed_url.scheme in ('http', 'https'):
        return SpotifyIdentifier._make(parsed_url.path.strip('/').split('/'))
    elif parsed_url.scheme in ('spotify'):
        return SpotifyIdentifier._make(parsed_url.path.split(':'))
    else:
        raise ValueError('%s is not a recognised Spotify URL.' % url)


def make_spotify_url(spotify_id, spotify_type='album'):
    """Generate a Spotify URL from data.
    
    >>> make_spotify_url('2QE5TZ3P547etzfMWgE8lL')
    'http://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL'
    >>> make_spotify_url('2QE5TZ3P547etzfMWgE8lL', 'artist')
    'http://open.spotify.com/artist/2QE5TZ3P547etzfMWgE8lL'
    >>> make_spotify_url('Æøå')
    Traceback (most recent call last):
        ...
    ValueError: "Æøå" contains characters invalid in Spotify IDs.
    >>> make_spotify_url('2QE5TZ3P547etzfMWgE8lL', 'tinny word')
    Traceback (most recent call last):
        ...
    ValueError: "tinny word" is not a recognised Spotify entity type.
    """
    # TODO: Test if Spotify ID is valid.
    if spotify_type not in SPOTIFY_MUSICBRAINZ_MAPPING:
        raise ValueError('"%s" is not a recognised Spotify entity type.' % spotify_type)
    return 'http://open.spotify.com/{0}/{1}'.format(spotify_type, spotify_id)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
