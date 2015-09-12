#!/usr/bin/env python
__author__ = 'byt3smith'
#
# Wildfire API Tool
#

import requests, argparse
import xml.etree.ElementTree as et

class Wildfire():
  def __init__(self):
    self.apikey = '<--Insert-Wildfire-API-Key-->'
    self.base = 'https://wildfire.paloaltonetworks.com/publicapi/'
    self.type_err = '[-] Incorrect type. Those values are hardcoded.. so quit your shenanigans'

  def download(self, md5, type):
    if type == 'file':
      # Options specific to File downloads
      f = "%s.exe" % md5
      url = self.base + "get/sample" # URL for sample download (see Wildfire API documentation)
      result = '\n[+] Sample saved as: ' + f
    
    elif type == 'pcap':
      # Options specific to PCAP downloads
      f = "%s.pcap" % md5
      url = self.base + 'get/pcap'
      result = '\n[+] PCAP saved as: ' + f 
    else:
      print self.type_err

    # Build and send the HTTP POST request
    params = {'hash':md5,'apikey':self.apikey} # HTTP POST parameters
    r = requests.post(url, data=params) # Create request
    if r.raise_for_status() == None: # Error checking by HTTP status code
      with open(f, 'wb') as fd:
        fd.write(r.content) # Write downloaded content to file
        print result

  def submit(self, item, type):
    if type == 'file':
      # Options specific to File scanning
      url = self.base + "submit/file" # URL for sample download (see Wildfire API documentation)
      params = {'apikey':self.apikey} # HTTP POST parameters
      files = {'file': ('sample', open(item, 'rb'))}
      result = '[+] %s has been submitted for analysis! A report should be available in 5-10 minutes' % item
      
      # Build and send the HTTP POST request
      r = requests.post(url, data=params, files=files) # Create request
      if r.raise_for_status() == None: # Error checking by HTTP status code
        response = et.fromstring(r.text)
        print result
        for info in response.findall('upload-file-info'):
          s256 = info.find('sha256').text
          size = info.find('size').text
          ftype = info.find('filetype').text
          print '\n[i] Uploaded File Info:\nSHA256: %s\nSize: %s\nFiletype: %s' % (s256, size, ftype)

    elif type == 'url':
      # Options specific to URL scanning   
      url = self.base + 'submit/url'
      params = {'url':item,'apikey':self.apikey} # HTTP POST parameters
      result = '\n[+] URL has been submitted for analysis!'
      # Build and send the HTTP POST request
      r = requests.post(url, data=params) # Create request
      if r.raise_for_status() == None: # Error checking by HTTP status code
        print result

    else:
      print self.type_err


  def report(self, md5, format):
    if format == 'pdf':
      # Options specific to File downloads
      f = "%s.pdf" % md5
      result = '\n[+] PDF report saved as: ' + f

    elif format == 'xml':
      # Options specific to PCAP downloads
      f = "%s.xml" % md5
      result = '\n[+] XML report saved as: ' + f
    else:
      print self.type_err

    # Build and send the HTTP POST request
    url = self.base + 'get/report'
    params = {'hash':md5,'apikey':self.apikey, 'format':format} # HTTP POST parameters
    r = requests.post(url, data=params) # Create request
    if r.raise_for_status() == None: # Error checking by HTTP status code
      with open(f, 'wb') as fd:
        fd.write(r.content) # Write downloaded content to file
        print result


if __name__ == '__main__':
  wf = Wildfire()
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('-d', nargs=2, metavar=('[F/P]', 'MD5'), help='Download File or PCAP [F or P] by MD5')
  parser.add_argument('-s', nargs=2, metavar=('[F/U]', '<Item to analyze>'), help='Submit File or URL [F or U] for analysis')
  parser.add_argument('-r', nargs=2, metavar=('[P/X]', 'MD5'), help='Query for a PDF or XML [P or X] report by MD5')
  args = parser.parse_args()

  if args.d:
    if args.d[0] == 'F':
      print '[*] Downloading %s' % args.d[1]
      wf.download(args.d[1], 'file')
    elif args.d[0] == 'P':
      print '[*] Downloading PCAP for %s' % args.d[1]
      wf.download(args.d[1], 'pcap')
    elif args.d[0] != 'P' or args.d[0] != 'F':
      print '[-] Download Error: Must specify either F [for File], or P [for PCAP]'

  elif args.s:
    if args.s[0] == 'F':
      print '[*] Submitting file %s for analysis' % args.s[1]
      wf.submit(args.s[1], 'file')
    elif args.s[0] == 'U':
      print '[*] Retrieving URL for analysis'
      wf.submit(args.s[1], 'url')
    elif args.s[0] != 'F' or args.s[0] != 'U':
      print '[-] Submit Error: Must specify either F [for File], or U [for URL]'

  elif args.r:
    if args.r[0] == 'P':
      print '[*] Requesting PDF report of %s' % args.r[1] 
      wf.report(args.r[1], 'pdf')
    elif args.r[0] == 'X':
      print '[*] Requesting XML report of %s' % args.r[1]
      wf.report(args.r[1], 'xml')
    elif args.r[0] != 'P' or args.r[0] != 'X':
      print '[-] Report Error: Must specify either P [for PDF] or X [for XML]'

  else:
    parser.print_help()
