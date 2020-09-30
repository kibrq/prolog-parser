#!/usr/bin/env python3

import plex
import parser as ps

def test_parser_accept():
    text = 'f :- g.'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'f :- \n g.'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'abracadabra :- f,g.'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'f :- f;g.'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'f :- f,g;c.'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'f :- g,(f;c).'
    assert ps.parse(plex.token_list_from_text(text))
    text = 'f :- g. g:-t. \n\n\n h :- q.'
    assert ps.parse(plex.token_list_from_text(text))

def test_parser_reject():
    text = 'f :- .'
    assert not ps.parse(plex.token_list_from_text(text))
    text = 'f :- g'
    assert not ps.parse(plex.token_list_from_text(text))
    text = ':- g.'
    assert not ps.parse(plex.token_list_from_text(text))
    text = ':-g'
    assert not ps.parse(plex.token_list_from_text(text))
    text = 'f :- (g.'
    assert not ps.parse(plex.token_list_from_text(text))
    text = 'f :- g).'
    assert not ps.parse(plex.token_list_from_text(text))
    text = 'f :- (g)).'
    assert not ps.parse(plex.token_list_from_text(text))
    text = 'f :- g g.'
    assert not ps.parse(plex.token_list_from_text(text))
