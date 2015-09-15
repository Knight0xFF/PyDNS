#!/usr/bin/env python
# encoding: utf-8

import ConfigParser

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read("config.conf")

server = config.items("server")

hosts = config.items("hosts")
