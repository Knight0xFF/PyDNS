#!/usr/bin/env python
# encoding: utf-8

from dnslib import DNSHeader, DNSRecord, RR, A
from gevent.server import DatagramServer
import re


class DnsCache():
    def __init__(self):
        self.cache = dict()

    def get(self, domain):
        return self.cache.get(domain, None)

    def set(self, domain, info):
        self.cache[domain] = info

    def delete(self, domain):
        self.cache.pop(domain, None)
cache = DnsCache()


class DnsQueryHandle():
    def __init__(self, data):
        self.data = data
        self.parse_request()

    def parse_request(self):
        self.query = DNSRecord.parse(self.data)
        self.qid = self.query.header.id
        self.qtype = self.query.q.qtype
        self.qname = self.query.q.qname

    def handle_response(self):
        self.handle_request()
        self.reply = DNSRecord(DNSHeader(id=self.qid, qr=1, aa=1, ra=1), q=self.query.q, a=RR(self.qname, rdata=A(self.iplist[0])))
        return self.reply.pack()

    def handle_request(self):
        next_query = DNSRecord.question(self.qname)
        next_reply = next_query.send("114.114.114.114")
        iplist = re.findall('\xC0.\x00\x01\x00\x01.{6}(.{4})', next_reply)
        self.iplist = ['.'.join(str(ord(x)) for x in s) for s in iplist]


class DnsServer(DatagramServer):
    def handle(self, data, address):
        query = DnsQueryHandle(data)
        self.socket.sendto(query.handle_response(), address)


if __name__ == "__main__":
    print "DnsServer running"
    DnsServer("127.0.0.1:53").serve_forever()